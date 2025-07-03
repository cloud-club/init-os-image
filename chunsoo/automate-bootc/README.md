# Automate Bootc (미완성)

bootc 빌드, 업데이트, 확인 자동화

## 시나리오

1. Containerfile build → registry upload → device에 ssh 접속하여 update
2. Containerfile & config.toml로 iso 이미지 빌드 → 설치

## 사전준비


## 확인


## 고찰?

### 더 써보고 싶은 것

- github actions self-hosted runner를 사용하기 전까지는 ssh pass를 사용했었는데, 어차피 ssh로 bootc 디바이스에 접근해야 한다면 ansible을 사용해보는 것이 낫지 않을까 싶음
- redfish라는 것이 있던데, bootc와 함께 사용한다면 RestAPI로 bootc를 실행하여여 더 손쉽게 환경 관리가 가능하지 않을까 싶지만 redfish를 아직 사용한 적도 없고 사용 사례를 많이 탐색하지 않아 불확실함
    - [(Redhat) Redfish API를 사용하여 HTTP 호스팅 ISO 이미지에서 부팅](https://docs.redhat.com/ko/documentation/openshift_container_platform_installation/4.13/html/installing_on_a_single_node/install-booting-from-an-iso-over-http-redfish_install-sno-installing-sno-with-the-assisted-installer)

### 배포 방법에 대한 의문점

- bootc 이미지를 배포할 때, bootc가 설치되어 있는 깡통 iso 파일을 설치한 후 `bootc switch`를 진행한다면 더 빠른 배포가 가능하지 않을까?
- 초기 배포시 bootc의 iso 이미지를 빌드하여 새로이 os를 설치하는 것과 bootc가 설치되어 있는 os에서 `bootc switch`를 진행하는 것의 배포 관점에서의 차이를 비교해봐야겠음
- production 환경에서 환경과 관련하여 고려해야 할 점을 탐색해 봐야겠다 느꼈음