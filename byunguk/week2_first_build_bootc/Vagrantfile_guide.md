Vagrant를 사용하여 Ubuntu 이미지를 기반으로 bootC 웹서버 빌드 환경을 자동화하는 Vagrantfile을 작성해 드리겠습니다. 이 파일은 VirtualBox에 Ubuntu를 설치하고, bootC 이미지 빌드에 필요한 도구들을 설치한 후, 웹서버 파일을 준비하는 단계까지 자동화합니다.

제가 작성한 Vagrantfile은 가이드에 명시된 모든 단계를 자동화하여 bootC 웹서버 구축을 위한 환경을 준비해줍니다. 이 파일을 사용하면 다음과 같은 작업이 자동으로 수행됩니다:

1. Ubuntu 22.04 LTS 가상머신 생성 및 설정 (4GB 메모리 할당)
2. 필요한 도구(podman, git, curl, qemu-utils) 설치
3. bootC 이미지 빌드 환경 준비
4. CentOS Stream 9 bootC 기본 이미지 다운로드
5. 웹서버를 포함하는 Containerfile 자동 생성
6. 웹페이지 파일(index.html) 생성

## 사용 방법

### 1. Vagrantfile을 새 디렉토리에 저장합니다.

```bash
# Vagrantfile이 있는 디렉토리에서
vagrant up
```

### 2. VM에 SSH로 접속

```bash
vagrant ssh
```

### 3. bootC 이미지 빌드하기

```bash
cd ~/bootc-webserver
sudo podman build -t my-bootc-webserver .
```

### 4. bootC 이미지를 디스크 이미지로 변환하기

먼저 사용자 설정 파일을 생성합니다:

```bash
cat > config.toml << 'EOL'
[[customizations.user]]
name = "admin"
password = "bootcpassword"
groups = ["wheel"]
EOL
```

그런 다음 이미지를 QCOW2 형식으로 변환합니다:

```bash
sudo podman run \
  --rm \
  -it \
  --privileged \
  --pull=newer \
  --security-opt label=type:unconfined_t \
  -v ./config.toml:/config.toml:ro \
  -v ./output:/output \
  -v /var/lib/containers/storage:/var/lib/containers/storage \
  quay.io/centos-bootc/bootc-image-builder:latest \
  --type qcow2 \
  --output /output \
  localhost/my-bootc-webserver
```

### 5. VirtualBox에서 사용하기 위해 QCOW2를 VDI로 변환 (필요한 경우)

```bash
qemu-img convert -f qcow2 -O vdi output/qcow2/disk.qcow2 output/bootc-webserver.vdi
```

### 6. 디스크 이미지를 호스트로 복사하기

새 터미널에서 Vagrant 디렉토리로 이동하여 다음 명령어 실행:

```bash
vagrant plugin install vagrant-scp
vagrant scp default:/home/vagrant/bootc-webserver/output/bootc-webserver.vdi ./
```

이제 `bootc-webserver.vdi` 파일을 VirtualBox에서 새 VM의 하드 디스크로 사용할 수 있습니다.

## VM 종료하기

작업을 마치면 VM을 종료할 수 있습니다:

```bash
# 일시 중지
vagrant suspend

# 또는 완전히 종료
vagrant halt

# 또는 VM 삭제
vagrant destroy
```

## 추가 정보

bootC 관련 추가 정보는 다음 리소스를 참조하세요:
- [bootC GitHub 저장소](https://github.com/containers/bootc)
- [CentOS bootC 이미지](https://quay.io/centos-bootc/centos-bootc)
- [Fedora bootC 문서](https://docs.fedoraproject.org/en-US/bootc/)