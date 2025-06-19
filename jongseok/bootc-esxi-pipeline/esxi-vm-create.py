#!/usr/bin/env python3
import argparse
import paramiko
import logging
import sys
import re
from pathlib import Path

# 기본 설정
DEFAULT_CONFIG = {
    'LOG': '/var/log/esxi-vm.log',
    'DISK_FORMAT': 'thin',
    'VIRTUAL_HW_VERSION': '17',
    'SCSI_CONTROLLER': 'lsisas1068'  # LSI Logic SAS 사용
}

def setup_logging(log_path):
    """로깅 시스템 초기화"""
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def validate_mac(mac):
    """MAC 주소 유효성 검사"""
    if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac):
        raise ValueError(f"잘못된 MAC 주소: {mac}")
    return mac.replace('-', ':')

def create_vmx_config(args):
    """VMX 설정 생성 (ESXi 7.0 최적화)"""
    vmx = [
        'config.version = "8"',
        f'virtualHW.version = "{DEFAULT_CONFIG["VIRTUAL_HW_VERSION"]}"',
        'vmci0.present = "TRUE"',
        f'displayName = "{args.name}"',
        'floppy0.present = "FALSE"',

        # PCI 브리지 설정 (PCI 슬롯 충돌 방지)
        'pciBridge0.present = "TRUE"',
        'pciBridge4.present = "TRUE"',
        'pciBridge4.virtualDev = "pcieRootPort"',
        'pciBridge4.functions = "8"',
        'pciBridge5.present = "TRUE"',
        'pciBridge5.virtualDev = "pcieRootPort"',
        'pciBridge5.functions = "8"',

        # SCSI 컨트롤러 설정 (LSI Logic SAS)
        'scsi0.present = "TRUE"',
        f'scsi0.virtualDev = "{DEFAULT_CONFIG["SCSI_CONTROLLER"]}"',
        'scsi0.pciSlotNumber = "100"',  # 고정 슬롯 할당

        # CPU/메모리
        f'numvcpus = "{args.cpu}"',
        f'memsize = "{args.mem * 1024}"',

        # 디스크 설정 (명시적 활성화)
        'scsi0:0.present = "TRUE"',
        f'scsi0:0.fileName = "{args.name}.vmdk"',
        'scsi0:0.deviceType = "scsi-hardDisk"',

        # 게스트 OS
        f'guestOS = "{args.guestos}"'
    ]

    # CD-ROM 설정
    if args.iso:
        vmx.extend([
            'ide1:0.present = "TRUE"',
            f'ide1:0.fileName = "{args.iso}"',
            'ide1:0.deviceType = "cdrom-image"',
            'ide1:0.startConnected = "TRUE"'
        ])
    else:
        vmx.extend([
            'ide1:0.present = "FALSE"'
        ])

    # 네트워크 설정
    if args.net != "None":
        vmx.extend([
            'ethernet0.virtualDev = "vmxnet3"',
            'ethernet0.present = "TRUE"',
            f'ethernet0.networkName = "{args.net}"',
            'ethernet0.addressType = "generated"'
        ])

    # 사용자 정의 옵션
    for opt in args.vmxopts:
        if '=' not in opt:
            logging.warning(f"무시된 VMX 옵션: {opt}")
            continue
        key, value = opt.split('=', 1)
        vmx.append(f'{key.strip()} = "{value.strip()}"')

    return vmx

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(
        description='ESXi VM 생성 도구 (완전한 버전)',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # 필수 인자
    parser.add_argument('-H', '--host', required=True, help='ESXi 호스트 IP')
    parser.add_argument('-U', '--user', default='root', help='ESXi 사용자명')
    parser.add_argument('-P', '--password', required=True, help='ESXi 비밀번호')
    parser.add_argument('-n', '--name', required=True, help='VM 이름')
    parser.add_argument('-S', '--store', required=True, help='데이터스토어 이름')
    
    # 선택 인자
    parser.add_argument('-c', '--cpu', type=int, default=2, help='vCPU 개수')
    parser.add_argument('-m', '--mem', type=int, default=4, help='메모리(GB)')
    parser.add_argument('-v', '--hdisk', type=int, default=40, help='디스크 크기(GB)')
    parser.add_argument('-i', '--iso', help='ISO 파일 경로')
    parser.add_argument('-N', '--net', default='VM Network', help='네트워크 이름')
    parser.add_argument('-M', '--mac', help='MAC 주소', type=validate_mac)
    parser.add_argument('-g', '--guestos', default='centos8-64', help='게스트 OS 타입')
    parser.add_argument('-o', '--vmxopts', nargs='*', default=[], help='추가 VMX 옵션')
    
    # 인자 파싱 ✅
    args = parser.parse_args()
    setup_logging(DEFAULT_CONFIG['LOG'])

    try:
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                args.host,
                username=args.user,
                password=args.password,
                timeout=15,
                banner_timeout=200
            )

            # 데이터스토어 확인
            stdin, stdout, stderr = ssh.exec_command(f"esxcli storage filesystem list | grep '{args.store}'")
            if not stdout.read().decode().strip():
                raise Exception(f"데이터스토어 {args.store}를 찾을 수 없음")

            # VM 폴더 생성
            vm_path = f"/vmfs/volumes/{args.store}/{args.name}"
            stdin, stdout, stderr = ssh.exec_command(f"mkdir -p '{vm_path}'")
            if stderr.channel.recv_exit_status() != 0:
                raise Exception(f"VM 폴더 생성 실패: {stderr.read().decode()}")

            # VMDK 생성 (Thin Provisioning)
            stdin, stdout, stderr = ssh.exec_command(
                f"vmkfstools -c {args.hdisk}G -d {DEFAULT_CONFIG['DISK_FORMAT']} '{vm_path}/{args.name}.vmdk'"
            )
            if stderr.channel.recv_exit_status() != 0:
                raise Exception(f"VMDK 생성 실패: {stderr.read().decode()}")

            # VMX 파일 생성
            vmx_content = '\n'.join(create_vmx_config(args))
            stdin, stdout, stderr = ssh.exec_command(f"echo '{vmx_content}' > '{vm_path}/{args.name}.vmx'")
            if stderr.channel.recv_exit_status() != 0:
                raise Exception(f"VMX 파일 생성 실패: {stderr.read().decode()}")

            # VM 등록
            stdin, stdout, stderr = ssh.exec_command(f"vim-cmd solo/registervm '{vm_path}/{args.name}.vmx'")
            vm_id = stdout.read().decode().strip()
            if not vm_id.isdigit():
                raise Exception(f"VM 등록 실패: {stderr.read().decode()}")

            # 전원 켜기
            stdin, stdout, stderr = ssh.exec_command(f"vim-cmd vmsvc/power.on {vm_id}")
            if stderr.channel.recv_exit_status() != 0:
                raise Exception(f"전원 켜기 실패: {stderr.read().decode()}")

            logging.info(f"[성공] VM {args.name} 생성 완료 (ID: {vm_id})")
            print(f"""
            ██████  ███    ███      ██████ ███████ ██████  
           ██    ██ ████  ████     ██      ██      ██   ██ 
           ██    ██ ██ ████ ██     ██      █████   ██████  
           ██    ██ ██  ██  ██     ██      ██      ██   ██ 
            ██████  ██      ██      ██████ ███████ ██   ██ 
            VM 생성 성공! 다음 단계:
            1. ESXi 웹 UI에서 VM 확인: https://{args.host}
            2. 콘솔 접속 후 OS 설치 진행
            """)

    except Exception as e:
        logging.error(f"[실패] {str(e)}")
        print(f"""
        ███████ ██████  ██████   ██████ ███████ 
        ██      ██   ██ ██   ██ ██      ██      
        █████   ██████  ██████  ██      █████   
        ██      ██   ██ ██   ██ ██      ██      
        ███████ ██   ██ ██   ██  ██████ ███████ 
        에러 발생: {str(e)}
        """)
        sys.exit(1)

if __name__ == "__main__":
    main()  # ✅ 메인 함수 실행 필수