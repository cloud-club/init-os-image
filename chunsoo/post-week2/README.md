# post-week2
week2 이후 시도해 본 것들

## 인상깊었던 발표 내용

- 기업에서는 [SAN(storage area network)](https://www.hpe.com/kr/ko/what-is/san-storage.html)를 사용함
- ostree에 대해서 찾아볼 필요가 있음

## bootc 실행 프로세스 (시도중)

### 참고자료
[redhat의 소개자료 및 핸즈온](https://developers.redhat.com/articles/2024/09/24/bootc-getting-started-bootable-containers#get_started_with_bootc_with_video_demos)

[podman-bootc](https://github.com/containers/podman-bootc)

### 기본 이미지

```
# Containerfile
FROM quay.io/centos-bootc/centos-bootc:stream9
RUN dnf -y install httpd cloud-init plymouth vim && \
    systemctl enable httpd && \
    systemctl enable cloud-init.service
EXPOSE 80
```

빌드
```shell
podman build -t bootc .
```

### 이미지 태깅 및 푸시

#### general
```shell
# 이미지 태깅
podman tag localhost/bootc:latest quay.io/your-repo/your-os:tag

# 레지스트리에 푸시
podman push quay.io/your-repo/your-os:tag
```
#### mine
```shell
podman tag localhost/bootc:latest docker.io/DOCKER-ID/bootc:latest

podman login docker.io

podman push docker.io/DOCKER-ID/bootc:latest
```

### 이미지 설치 및 실행행

#### general
검증 안됨 (AI들과 머리를 맞대고 시도해봤는데 실패함함)
```shell
# 디스크에 직접 설치
podman run --rm --privileged --pid=host -v /var/lib/containers:/var/lib/containers -v /dev:/dev \
  --security-opt label=type:unconfined_t <image> bootc install to-disk /path/to/disk
  

# 기존 파일시스템에 설치
podman run --rm --privileged -v /:/target \
  --pid=host --security-opt label=type:unconfined_t \
  quay.io/centos-bootc/centos-bootc-cloud:stream9 \
  bootc install to-filesystem --replace=alongside /target


# 가상머신용 디스크 이미지 생성
truncate -s 10G myimage.raw
podman run --rm --privileged --pid=host --security-opt label=type:unconfined_t \
  -v /dev:/dev -v /var/lib/containers:/var/lib/containers -v .:/output <yourimage> \
  bootc install to-disk --generic-image --via-loopback /output/myimage.raw

```

#### mine
```shell
podman pull docker.io/DOCKER-ID/bootc:latest

# 여기부터 실패함
# root 권한 아닐시 sudo 붙여야함
podman run --rm --privileged -v /:/target \
  --pid=host --security-opt label=type:unconfined_t \
  docker.io/DOCKER-ID/bootc:latest \
  bootc install to-filesystem --replace=alongside /target

```

podman-bootc를 쓰는 편이 여러모로 편한 것 같음
```shell
podman pull docker.io/DOCKER-ID/bootc:latest

# 여기부터 실패함
podman-bootc run docker.io/DOCKER-ID/bootc:latest
```

## Question
- podman machine을 `podman machine init --rootful --now` 명령어를 사용해 생성해도도 rootless 관련 문제가 발생하는데 다른 분들도 발생하는지?
- (질문X) podman을 같이 공부해보면서 다음주까지 꼭 bootc 부팅 및 롤백까지 성공해오겠습니다다