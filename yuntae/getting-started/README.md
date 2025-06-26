# Getting Started - bootc

## Index

## What is libostree?

- Reference: [libostree](https://ostreedev.github.io/ostree/)
- Git과 유사한 방식으로 파일 시스템 트리를 관리하는 라이브러리.
- 운영 체제 전체를 하나의 변경 불가능한 이미지로 관리
- 업데이트가 성공적으로 완료되거나 완전히 롤백되어 시스템 일관성을 보장
- 파일 시스템의 변경 사항만 추적하고 저장하여 저장 공간을 절약 (hard link 사용)
- OS(Kernel 포함)에 속하는 파일들을 읽기 전용으로 만들어 시스템의 안정성과 보안을 강화
- OS 단위로 Rollback 가능
  - Git과 유사하게 libostree는 커밋을 가지며, 최초 커밋 기준으로 하드링크를 사용하기 때문에 Repository에는 변경된 파일만 저장되고 이를 통해 Rollback이 가능

## rpm-ostree?
 
```bash
                         +-----------------------------------------+
                         |                                         |
                         |       rpm-ostree (daemon + CLI)         |
                  +------>                                         <---------+
                  |      |     status, upgrade, rollback,          |         |
                  |      |     pkg layering, initramfs --enable    |         |
                  |      |                                         |         |
                  |      +-----------------------------------------+         |
                  |                                                          |
                  |                                                          |
                  |                                                          |
+-----------------|-------------------------+        +-----------------------|-----------------+
|                                           |        |                                         |
|         libostree (image system)          |        |            libdnf (pkg system)          |
|                                           |        |                                         |
|   C API, hardlink fs trees, system repo,  |        |    ties together libsolv (SAT solver)   |
|   commits, atomic bootloader swap         |        |    with librepo (RPM repo downloads)    |
|                                           |        |                                         |
+-------------------------------------------+        +-----------------------------------------+
```

- Reference: [rpm-ostree](https://coreos.github.io/rpm-ostree/)
- libostree + rpm package manager

## What is bootc?

![concept](https://developers.redhat.com/sites/default/files/styles/article_floated/public/image1_62.png.webp?itok=c0vYglLs)

- Reference: [bootc](https://bootc-dev.github.io/bootc/)
- OCI (Open Container Initiative) 이미지 포맷을 사용하여 컨테이너를 부팅 가능한 OS로 변환하는 도구
- libostree를 가진 이미지를 base로 사용.

### OverlayFS + libostree?

- libostree의 경우 Containerfile 빌드 스텝 마지막에 커밋을 생성.
- 즉 Container의 OverlayFS는 이미지 빌드 스텝 + 캐싱에서 유의미
- OCI 이미지 생성 이후에는 libostree가 파일 시스템 트리 + 파일 단위로 정확하게 변경사항을 추적.

### Registry?

- OCI Registry에 bootc 이미지를 push/pull 가능. bootc 이미지 배포 전까지는 일반 OCI 이미지와 동일. (Runtime에서도 문제가 없음)

### Advantages

- Docs에서 말하는 것처럼 Container를 많은 사람들이 사용하기 때문에 러닝커브가 낮음
  - > The original Docker container model of using "layers" to model applications has been extremely successful. This project aims to apply the same technique for bootable host systems - using standard OCI/Docker containers as a transport and delivery format for base operating system updates.
  - 기존 Container Image Building과 동일한 방식으로 OS 이미지를 구성 가능
- libostree를 통해 이미지의 변경사항을 git과 유사하게 파일 단위로 추적할 수 있기 때문에 쉽게 Rollback, Update 가능
- OS 배포 시에는 /usr이 변경되지 않기 때문에 safety 관점에서 유리
- "내 컴퓨터에서는 됐어요"를 커널 단부터 방지 가능.

### Note

- /usr, /var, /etc는 configuration. (/usr for general, /etc for specific machine)

## Getting Started

### Goal

- libostree를 지닌 image을 base로 OCI buildfile을 작성하여 OCI image를 생성
- OCI image를 bootc를 통해 bootable image로 변환
- bootc bootable image를 flash
- 설치
- 새 버전 이미지 생성
- bootc update
- bootc rollback

### Base Containerfile

[Reference](https://gitlab.com/fedora/bootc/examples/-/tree/main/tailscale)

1. OCI image build

```dockerfile
FROM quay.io/centos-bootc/centos-bootc:stream9

RUN dnf config-manager --add-repo https://pkgs.tailscale.com/stable/centos/9/tailscale.repo && \
    dnf -y install tailscale && \
    dnf clean all && \
    ln -s ../tailscaled.service /usr/lib/systemd/system/default.target.wants

```

`podman build`

2. config.json

```json
{
  "blueprint": {
    "customizations": {
      "user": [
        {
          "name": "alice",
          "key": "ssh-rsa AAA ... user@email.com",
          "groups": [
            "wheel"
          ]
        }
      ]
    }
  }
}
```

3. [bootc image builder](https://github.com/osbuild/bootc-image-builder)

```bash
# Ensure the image is fetched
sudo podman pull quay.io/centos-bootc/centos-bootc:stream9
mkdir output
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
	--use-librepo=True \
    quay.io/centos-bootc/centos-bootc:stream9
```

4. flash with [balenaEtcher](https://etcher.balena.io/)
5. boot with USB
6. check `systemctl status tailscaled`
    - 기본적으로 bootc는 일반 OS와 같이 systemd를 사용하여 서비스가 자동으로 등록되도록 동작
7. add `RUN dnf install -y curl` to test new version of bootc image
8. bootc update/rollback
    - Registry 사용 (임시로 로컬 harbor 사용)

## Question

1. bootc image를 update해서 registry에서 pull할 때, libostree 컨셉과 동일하게 파일 변경사항을 추적하여 가져오는지. 아니면 layer만 가져오는지
