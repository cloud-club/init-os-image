# Link
[퍼플렉시티 리서치](https://www.perplexity.ai/search/prompttemplate-task-bootable-c-hSTv7a0HSOu7YaiN9vUc9Q)

[제미나이 리서치](https://docs.google.com/document/d/1VkxKrGcOpzJ5D83kf8CUFzlOyNrIuXLVJ4GVOsc_2bg/edit?usp=sharing)

# boot C

## A. 도대체 무엇일까?
- bootC 이미지는 일반 컨테이너 이미지와 달리, "부팅 가능한 컨테이너(bootable container)"로 설계되어 있습니다.
- 이 이미지를 bootc install 명령어로 시스템에 설치하면, 기존 OS 대신 해당 이미지를 기반으로 시스템이 부팅된다고 한다.
- 이때 실제로 OS의 루트 파일 시스템(/usr, /etc, /var 등)이 bootC 이미지로 대체되고, 커널 파라미터, 서비스 설정 등도 이미지에 정의된 대로 적용된다고 한다.
- 오우오우, 그러면 이거 걍 바이오스에서 부팅 우선순위 하는거랑 다를바가 없겠네?
- 설치 후 시스템을 재부팅하면, 내가 만든 bootC 이미지가 OS로 동작하는지 직접 확인할 수 있습니다. 예를 들어, 이미지에 포함한 패키지나 파일, 서비스가 정상적으로 동작하는지 체크할 수 있습니다.

## B. 그래서 왜 쓰는가?
- 이거 이미지 자체를 버전별로 관리하려고 쓰기 좋음.
- 원자성이 보장됨. 이것이 무엇을 의미하냐? 해당 OS는 그 OS자체만으로 역할을 수행할 수 있다는것임.
    - 운영자는 그냥 이미지만 바꿔끼워두면 해당 OS의 동작은 머 그냥 다 알아서 함. 내부 들어가서 만질 필요가 없음.

### B-1. 구체적으로, 어디에 쓰일 수 있을까?

서버 수십 대, 수백 대 OS 환경을 다 똑같이 맞춰야 할 때? 아니면 IoT 기기나 엣지 장비들처럼 손 대기 어려운 곳에 배포하고 원격으로 업데이트할 때 유용할듯.

개발 환경이랑 운영 환경 OS까지 똑같이 맞추고 싶을 때도 쓸 수 있을듯.

### B-2. 현재 내 환경에서는 어디에 적용될수 있을까?

만약 내가 서버 여러 대 돌리면서 OS 버전 맞추느라 골머리 썩는다면? 

아니면 새 프로젝트 시작할 때마다 OS 세팅하는 게 귀찮다면? 그럴 때 bootC로 딱 OS 이미지 만들어두고 그걸로 싹 설치해버리면 편할수도..?

근데 아직은 VM보다 더 나은걸 잘 모르겠음

## C. boot C 대신에 사용할 수 있는 기술들에 대한 레퍼런스

### C-1. 왜 굳이 bootC일까? docker/ansible 기반 자동화로는 안될까?? cloud init쓰면 안돼?


얘네들이랑은 목적이 좀 다른 것 같아. 걔네들은 OS '위에서' 또는 OS를 '설정하는' 역할이라면, bootC는 OS '자체'를 통으로 다루는 느낌? 그래서 더 근본적인 OS 관리 방식이라고 봐야 하나? 바이오스에서 부팅 우선순위 정하는 거랑 비슷하다고 느꼈던 것처럼, OS 레벨에서 갈아끼우는 거니까. Docker나 Ansible은 그 위에 올라가는 레이어고. 뭐 그런 차이 아닐까?

## D. 그래서, boot C는 어떻게 사용하는가?

### D-1. 놀랍게도, bootC의 문법은 Dockerfile과 유사하다.
- bootC 이미지는 놀랍게도 우리가 이미 익숙한 방식으로 만들어진다. 
- 바로 표준 Containerfile (Dockerfile과 거의 같다) 문법과 Podman, Docker, Buildah 같은 도구들을 사용해서 빌드된다.
- 즉, bootC용 베이스 이미지에서 시작해 필요한 요소를 추가하면 나만의 이미지가 된다.
- 패키지 설치, 설정 추가, 애플리케이션 내장 등 다양한 커스터마이징이 가능하며, Docker 이미지 만드는 방식과 유사하다.

### D-2. 예제 코드
아래는 위의 간단한 bootC Containerfile을 빌드하고, 이미지를 확인하며, 실제로 bootc로 실행(테스트)하는 방법을 안내합니다.

#### 1. Containerfile 작성

아래 코드를 `Containerfile`이라는 이름으로 저장하세요.

```Dockerfile
# CentOS Stream bootC 베이스 이미지 사용
FROM quay.io/centos-bootc/centos-bootc:stream9

# vim 패키지 설치 (필요한 패키지만 최소로 설치)
RUN dnf -y install vim

# 간단한 텍스트 파일 추가
RUN echo "안녕하세요, bootC 간단 예제입니다." > /root/hello.txt
```

#### 2. 빌드 및 실행

```Dockerfile
# 1. Containerfile이 있는 디렉터리로 이동
cd /path/to/your/containerfile

# 2. 이미지를 빌드합니다. (my-bootc-test라는 이름으로 태그)
podman build -t my-bootc-test .

# 3. 빌드된 이미지를 확인합니다.
podman images

# 4. (선택) bootc로 이미지를 테스트 설치합니다.
sudo bootc install --image localhost/my-bootc-test

# 또는 podman-bootc로 컨테이너 기반 부팅 테스트를 할 수 있습니다.
# podman-bootc가 설치되어 있어야 합니다.
podman bootc install --image localhost/my-bootc-test

# 5. (테스트 후) /root/hello.txt 파일이 잘 생성되었는지 확인합니다.
cat /root/hello.txt

```

### D-3. bootc로 이미지를 테스트 설치한다는 의미가 도대체 무엇일까?

`sudo bootc install --image localhost/my-bootc-test`

해당 명령어는 예제에서 (선택) 태깅이 되어있다. 왜 선택일까? 위험한 작업일까?
그에대한 정답은, 해당 프로젝트에 대한 이름, 부팅 가능한 컨테이너! 그 자체에 있었다.

이 명령은 내가 만든 bootC 컨테이너 이미지를 현재 시스템의 운영체제로 설치하는 작업이다.
즉, 기존 리눅스 시스템을 내 bootC 이미지 기반의 새로운 OS로 "변환"하거나, 해당 이미지를 부팅 가능한 OS로 "적용"하는 과정이라는 것이다.

즉, 이 명령은 "내가 만든 컨테이너 이미지를 실제 OS로 설치해서, 다음 부팅 때부터 그 이미지로 시스템을 운영하겠다"는 의미이다.

bootc install --image ... 명령은 지정한 컨테이너 이미지를 시스템에 설치하여,
다음 부팅부터 그 이미지가 OS로 동작하게 만든다.

즉, 이 명령을 실행하면,

현재 시스템의 루트 파일시스템(예: /usr, /etc, /var 등)이 bootC 이미지로 대체되고,

시스템을 재부팅하면 내가 만든 bootC 이미지가 실제 OS처럼 부팅되는 것이다.

이 과정은 기존 OS를 완전히 지우는 것이 아니라,
부팅 가능한 이미지를 "스테이지"하고, 부팅 시점에 전환하는 방식이므로, 롤백(이전 상태로 복구) 도 매우 쉽게 할 수 있지만? Podman으로도 충분히 테스트가 가능하기에, 해당 명령어 설정에는 주의를 요하라는 의미이다.

즉, 컴퓨터 바이오스에 특정 iso를 마운트해서 부팅 우선순위를 설정하는것과 비슷하다고 느껴지기도한다.