# Start Bootc

bootc 초기 실행하기

## 이미지 빌드하기

Containerfile
``` Containerfile
FROM quay.io/centos-bootc/centos-bootc:stream9

RUN dnf install -y httpd nginx && \
    systemctl enable httpd && \
    systemctl enable nginx
```

``` shell
# podman desktop 사용 또는 아래 명령어로 빌드
podman build -t <IMAGE> .

# 명령어를 사용해서 빌드시 아래 명령어로 이미지 확인
podman images

# podman desktop으로 빌드 후 내보낼 시 .tar로 나온다면 아래 명령어 실행, 편의상 docker 사용했음
# docker save로 생성한 .tar도 동일한 명령어로 해체 가능
docker load -i my-bootc.tar

# tag 및 registry에 push
docker tag <IMAGE> <REGISTRY-URL>/<NAMESPACE>/<IMAGE>:<TAG>
docker push <IMAGE> <REGISTRY-URL>/<NAMESPACE>/<IMAGE>:<TAG>
```

### 유저를 추가하는 방법들

#### cloud-init 활용 동적 사용자 설정
1. cloud-init 설치
    - 이미지 빌드 시 cloud-init 패키지 포함
    - Dockerfile: `dnf install -y cloud-init && systemctl enable cloud-init.service`
2. user-data 주입
    - VM 생성 시 YAML로 사용자 설정 전달
    - SSH 키, 그룹, 패스워드 등 지정 가능
- 한계점: OS를 가상머신에서 사용하거나 클라우드 환경에 인스턴스로 올리는 것이 아니라면 애로사항이 있음

#### bootc-image-builder에서 config.toml 통한 정적 사용자 구성

- config.toml 구조
    - 사용자 정보, 그룹, 해시 패스워드, SSH 키, UID 등 설정
- 한계점: 정적이며 변경하려면 config.toml을 바꾸어 새로 빌드하고 올리는 과정이 필요함

#### Containerfile에서 사용자 추가

- Containerfile에서  계정 생성
    - `useradd` 명령어를 사용하여 계정 생성 과정 실행
    - ARG, 환경 변수로 ssh 키 주입 및 권한 설정
- 한계점: 이미지 빌드 과정에서 신경써야 할 것이 늘어남

#### 결론?
- config.toml을 사용해서 사용자를 추가하는 방법이 여러모로 편함 ~~초기세팅 이후에 사용자 추가할 일이 있긴 할까?~~
- 사용한 config.toml 파일은 아래와 같음

config.toml
``` toml
[[customizations.user]]
name = "user"           
password = "password"   
groups = ["wheel"]      
```

## Method 1: OS 이미지 파일 생성 후 직접 설치하기

**주의**
- 아래 실행 방법은 bootc를 사용해 OS 이미지 파일을 생성하기 때문에 OS 이미지를 설치할 머신이 아니더라도 상관없음.

``` shell
# docker는 단순 레지스트리 접근용
sudo dnf install podman bootc docker

dnf podman machine start --rootful
```

``` shell
sudo podman run \
  --rm \
  -it \
  --privileged \
  --pull=newer \
  --security-opt label=type:unconfined_t \
  -v /var/lib/containers/storage:/var/lib/containers/storage \
  -v ./config.toml:/config.toml \
  -v ./output:/output \
  registry.redhat.io/rhel9/bootc-image-builder:latest \
  --type iso \
  --config /config.toml \
  <REGISTRY-URL>/<namespace>/<image>:<tag>

```

- 생성한 iso 파일은 일반적인 os 설치 방법을 사용해 설치해 사용하면 됨
- iso 이외에도 vmdk, qcow, vhd 등의 이미지를 빌드 가능능

## Method 2: OS가 설치되어 있는 디바이스에서 다른 디스크에 직접 설치하기

**주의**
- 아래 실행 환경은
    1. 디스크가 2개 이상 설치되어 있는 머신 (가상머신도 무관)
    2. 디스크 2개 중 1개에는 ```podman run```을 위한 os가 설치되어 있어야 함
    3. 기존에 os가 설치되어 있는 디스크가 우선적으로 부팅 디스크로 선택되기 때문에 bootc를 사용해 빌드한 os를 설치한 디스크를 최우선적으로 부팅 디스크로 사용하도록 순서 변경이 필요함함

사전준비 (fedora server 42 기준)
``` shell
# docker는 단순 레지스트리 접근용
sudo dnf install podman bootc docker

dnf podman machine start --rootful
```

podman run 실행하여 디스크에 이미지 설치
``` shell
podman run --rm --privileged --pid=host \
  -v /var/lib/containers:/var/lib/containers \
  -v /dev:/dev \
  -v ./config.toml:/config.toml:ro \
  --security-opt label=type:unconfined_t \
  <REGISTRY-URL>/<NAMESPACE>/<IMAGE>:<TAG> \
  bootc install to-disk /dev/<DISK_NAME>
```

<details>
<summary>리눅스에서서 디스크를 찾고 초기화하기</summary>
<div markdown="1">

disk 목록 보기
``` shell
sudo fdisk -l # 실행 후 비어있는 디스크 선택
```

disk 삭제하기
``` shell
sudo fdisk <DISK_NAME>

d

<PARTITION_NUMBER>
```

</div>
</details>