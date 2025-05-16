### Goal

bootc에 대해서 질문을 했을 때 (누군가 bootc를 처음 이해하고 싶을 때) 어느정도 막힘이 없게.

- bootc가 도대체 어디/왜에 쓰이는가
    - OS 초기화
- 자신의 환경/프로젝트에서 bootc를 어디에 활용할 수 있을 지
- bootc 대신 사용할 수 있는 기술/방법 등에 대한 레퍼런스
    - 남이 이해가 가능하게 요약 (최소)
    - ex) 왜 docker/ansible 기반 자동화/cloud-init 로는 안돼

### Questions
1.  그럼 BootC는 뭐가 바뀌지 않고, 기존의 OS 설치는 뭐가 바뀌는거냐?
	1. 예를 들어 apt install같은 것들을 못함. /usr/bin/~~ 가 immutable하게 되어 있기 때문이다.
	2. 기존 cloud-init이나 일반 OS에서는 user 정보나 패키지 설치, 서비스들을 이후에 변경할 수 있지만, container로 만든 OS늠 불가하다.
2. OS 업데이트를 할 때, 원자적으로 한다. 그럼 원래는 어떻게 했는데? 
	1. 그럼 업데이트를 할때 업데이트는 누가 해주는데?? Boot strapping에서는, bootable usb가 해주는데?
	2. bootc가 해주는 것 같다. `bootc upgrade` 또한 `rollback`
	3. 그럼 구현은 어떻게 되는거지..? `bootc`가 업데이트 할 동안 `bootc` 그 자체는 어디서 동작하고 있는거지?? `bootc`도 OS 위에 올라와 있어야 하는 것 아닌가??
		1. bootc는 “실행 중인 OS의 자기 자신”이 “다음 부팅에 사용할 새로운 OS(그리고 그 안의 bootc)”를 준비하는 구조다.
3. 그럼 bootc OS 위에서 도커도 쓰면 뭔가 컨테이너 안에서 컨테이너를 사용하는건가?
	1. bootc OS는 컨테이너가 아니라 완전한 리눅스 OS이다.
	2. 또한 bootc  OS 위에서 container orchestration tool을 설치하는 것은 매우 권장된다. talos같이.
4. 기존의 vm에서 snapshot을 뜨는 거랑 뭐가 얼마나 그렇게 다른데?
	1. 기존 snapshot을 뜨는 과정을 알아야 할 것 같다.
		1. vm 스냅샷은 가상 머신 전체에 대하여 스냅샷을 찍는다. (메모리 포함)
		2. 그리고 불변도 아니다.
		3. 근데 메모리 빼고 찍을 수도 있지 않을까?
5. 근데 OS가 immutable이면 위에 application도 못띄우는 것 아님?? 어디서부터 어디까지 immutable이지?
	1. /usr 나 /boot 같은 파일은 read only이지만, /etc, /var는 writable하게 만들어진다.
	2. 이거 어떻게 구현하지? 특정 파일시스템으로?
6. OCI 기술이 뭐지? rpn-ostree는??
7. 그럼 bootc로 만든 이미지를 어떻게 나의 home server에 올릴 수가 있을까??
	1. machine에 따라 다르게 빌드해야하나? 만약 라즈베리파이이면?
		1. 라즈베리 파이 전용 이미지를 사용하면 된다.
	2. bootc를 사용할 때 기존의 OS는 bootc를 사용하지 않았어도 괜찮나??
		1. 그럼 실제 머신에 usb를 안꽂고, ssh 만으로 OS 업그레이드가 가능하다고??
8. bootc가 필요한 상황 vs 필요하지 않은 상황.
   1. 보통 prod에서는 한번 배포를 하고 OS를 수정하지 않음. 또한, 수정해야 할 경우가 별로 없음.
   2. dev 환경에서 OS 세팅을 할 때는 bootc를 사용하면, OS가 immutable해져서 안좋을 것 같음.
      1. dev 환경에서 OS 세팅을 하고, 해당 OS를 bootc로 구워서 prod에 올리는 것이 이상적일 것 같다.
