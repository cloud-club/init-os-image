## 컨셉
- Github Action을 이용한 ESXi VM 자동화 파이프라인 형성

- Containerfile에는 **서비스 개념보단 OS에 초점을 맞춤**

- KISA의 리눅스 취약점 분석 평가 가이드 중 **'계정의 wheel 그룹 권한'** 과 **'파일 경로에 따른 권한 변경 불가'** 에 초점을 두었음

- wheel 그룹에 속하지 않은 일반 사용자는 su나 sudo 같은 명령어로 root 권한을 얻을 수 없게 제한할 수 있음

- /usr, /bin, /etc 등 주요 시스템 디렉터리는 운영체제의 핵심 파일이 위치한 경로로 bootc는 /usr, /bin을 읽기 전용으로 마운트 함

- 과연 컨테이너 파일에 **KISA 취약점 분석 가이드를 반영한 뒤, 생성한 OS에 대해 사용자가 설정을 바꾸면 바뀔까?**

- Hypervisor는 ESXi로 선택하여 원격지에서 python 코드로 VM 생성하는 Git을 참고  
<img src="IMAGES/Screenshot_20250615_183810_Samsung Notes.jpg" width="1000"/>



---

## 구성
**CreateVM-bootcISO-ESXi.yml**
- 컨테이너 파일을 ISO로 빌드하고 파이썬 코드를 이용하여 ESXi VM 자동 생성 

![alt text](IMAGES/image.png)

  (1) Build ISO
  ```
  
  아래 KISA 취약점 진단 가이드를 포함한 컨테이너 파일을 Bootc-Server를 Github Action Self-Runner로 만들어 ISO 파일을 /output 하위에 생성한다.  
  
  # Containerfile
  ---
  wheel 그룹 설정    +            패스워드 정책              +            계정 잠금 임계값            +       SUID/SGID 관련 보안 설정
   ( /etc/pam.d )     ( /etc/security/pwquality.conf )          ( /etc/security/faillock.conf )             ( /usr/bin/ )
  ```
  (2) Downlaod ISO
  ```
  Self-Runner는 ESXi로 SSH로 접근하고 wget을 통해 Bootc(Self-Runner)로 접근하여 ISO 파일을 다운로드 한다.

  * scp로 ISO 2.6GB를 넘기려했으나 3시간 이상이 소요되어 방법을 바꾸었고 8초로 단축 
  ```
  (3) Create VM
  ```
  esxi-vm-create.py를 이용하여 VM을 원격지에서 생성 가능하며 필요한 정보는 다음과 같음

  (1) ESXi 정보 (아이디/비밀번호/주소)
  (2) Datastore 경로
  (3) VM Name
  (4) VM CPU/MEM
  (5) VM DISK (Thin/Think 할당 방식도)
  (6) VM Geust OS 
  (7) VM Network
  ```


**Update-bootc-Client.yml**
- Harbor 레지스트리에 컨테이너 이미지를 관리하여 bootC 클라이언트 업데이트 

![alt text](IMAGES/image-1.png)

(1) Build ISO
  ```
  빌드된 이미지는 Bootc-Server의 Harbor 저장
  ```
  (2) Downlaod ISO
  ```
  기존 컨테이너 이미지 Push/Pull과 동일
  ```
