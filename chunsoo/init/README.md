# Init

bootc를 본격적으로 사용하기 전 자료 모아보기

## What is bootc?

### 정의

- bootc는 부팅 가능한 컨테이너를 관리하기 위한 CLI 도구
- OCI/Docker 컨테이너 이미지를 사용하여 트랜잭션 기반의 운영 체제 업데이트 제공
- Red Hat에서 개발한 부팅 가능한 컨테이너 시스템

[bootable container는 정말 컨테이너인가?](https://www.notion.so/bootable-container-1f40be9cb75c8046ab2ad661c2bec388?pvs=21)

### 핵심 아이디어

- 기존 Docker 컨테이너 모델의 "레이어" 개념을 부팅 가능한 호스트 시스템에 적용
- 표준 OCI/Docker 컨테이너를 기본 운영 체제 업데이트를 위한 전송 및 배포 형식으로 사용
- 컨테이너 이미지에 Linux 커널(`/usr/lib/modules`)을 포함하여 부팅에 사용

### 작동 방식

- 실행 중인 시스템에서 기본 사용자 공간은 기본적으로 컨테이너에서 실행되지 않음
- systemd가 일반적으로 pid1로 작동하며, "외부" 프로세스가 없음
- 부팅 가능한 컨테이너 OS는 `/usr`가 읽기 전용이며 컨테이너로 정의됨
- ostree 프로젝트를 기반으로 안정적인 운영 체제 업데이트 제공

### base image

- Red Hat Enterprise Linux (RHEL) 9
- CentOS Stream 9, 10
- Fedora (예정)
- 커스텀 Linux 배포판
    
    bootc는 특정 배포판에 종속적이지 않으며, 커스텀 패키지 셋이나 자체 리포지터리를 활용해 맞춤형 base image를 빌드할 수 있음 (rpm-ostree 기반).
    
    - standard: 기본적으로 제공되는 서버 지향의 표준 이미지
    - minimal: 커널, systemd, dnf 등 필수 패키지만 포함한 최소 이미지 (직접 빌드 필요, 공식 컨테이너로는 아직 미제공)

## bootc의 장점과 특징

### DevOps를 위한 통합 접근 방식

- GitOps 및 CI/CD를 포함한 컨테이너 기반 툴링을 통해 전체 OS를 관리
- 애플리케이션 개발 주기와 운영 팀 간의 격차를 해소
- 대규모로 Linux를 효율적으로 관리하는데 도움

### 보안 강화

- OS가 컨테이너 이미지 형태로 제공되어 고급 컨테이너 보안 도구 활용 가능
- 컨테이너 보안의 발전을 커널, 드라이버, 부트로더 등에 적용
- 패치, 검사, 검증, 서명 등의 보안 프로세스 통합

### 속도 및 생태계 통합

- 컨테이너 중심의 광범위한 도구와 기술 생태계에 통합
- 새로운 규모와 속도로 Linux 시스템을 빌드, 배포, 관리 가능
- 간소화된 툴체인으로 더 짧은 시간 내에 시스템 관리

### 롤백 및 안전성

- `/usr`는 읽기 전용이며, 컨테이너를 이전 상태로 쉽게 롤백 가능
- 새로운 테마나 구성을 실험하다 실패해도 안전하게 복구할 수 있음
- `ostree admin unlock` 명령으로 재부팅 없이 일시적인 커스터마이징 가능

## bootc/ansible/cloud-init/PXE 비교교

GPT作

| 항목 | bootc | Ansible | cloud-init | PXE/Kickstart |
| --- | --- | --- | --- | --- |
| 배포 모델 | 컨테이너 이미지 기반(OS 전체를 OCI 이미지로 배포) | Push 방식 구성 관리(플레이북 실행 시점에 설정 적용) | VM 첫 부팅 스크립트(user-data) 기반 | 네트워크 부팅 → Kickstart 스크립트 기반 |
| 설치 트리거 | - Live ISO/PXE → `bootc install`- Podman → `bootc install to-disk` | SSH/API 호출로 `ansible-playbook` 실행 | VM 생성 시 메타데이터(user-data) 전달 | PXE 부팅 → DHCP/TFTP → Kickstart 파일 자동 로드 |
| 설치 단계 | 1. 이미지 다운로드2. 디스크에 이미지 전개3. 재부팅 | 1. 대상 서버 접속2. 패키지 설치·설정 파일 배포 | 1. cloud-init 초기화2. user-data 스크립트 실행 | 1. OS 커널/initrd 로드2. Kickstart에 정의된 파티션/패키지 설치 |
| 설정 적용 시점 | - 이미지 빌드 시 포함- 재부팅 시 신규 이미지 적용- 필요 시 cloud-init 연동 | 플레이북 실행 시 매번(재실행 가능) | 첫 부팅 시 1회 실행(부팅 후 재실행 기본 미지원) | 설치 중 `%post` 단계에서 스크립트 실행 |
| Idempotency (멱등성) | ◎ 이미지 단위(원자적)× 일부 설정은 cloud-init 의존 | ○ 모듈별 보장(사용자 작성 idempotent 여부에 따름) | △ 일부 모듈(idempotent)만 지원 | △ 재설치 시만 보장(설치 완료 후 반복 실행 미지원) |
| Rollback 지원 | ◎ OSTree 커밋 히스토리 기반 자동 롤백 | × 별도 롤백 메커니즘 필요 | × 미지원 | × 미지원 |
| 불변성(Immutable) | ◎ 시스템 전체 읽기 전용, `/etc`만 쓰기 가능 | × 실행 시마다 상태 변화 | × 임시 설정 스크립트 수준 | × 설치 시점만 불변, 운영 중 별도 관리 필요 |
| 주요 도구/명령 | `bootc CLI`, `podman`, 컨테이너 레지스트리 | `ansible-playbook`, `inventory`, 모듈들 | `cloud-init` 서비스, user-data YAML/스크립트 | `tftp`, `dhcp`, `anaconda`, `kickstart 파일` |
| 장점 | - 일관된 OS 이미지 배포- 트랜잭션 업데이트/롤백- 중앙 레지스트리 관리 | - 유연한 모듈 지원- 에이전트리스- 다양한 OS 지원 | - 클라우드 네이티브- 별도 에이전트 불필요- 간단한 스크립트 | - 완전 자동화 초기 설치- 운용 중 OS 미설치 환경에도 적용 가능 |
| 단점 | - 초기 설정은 별도 도구 필요- 기존 패키지 관리와 호환성 낮음 | - 드리프트 발생 가능- 대규모 반복 실행 시 성능 저하 | - 부팅 1회 한정 실행- OS 업데이트/롤백 기능 미지원 | - 운영 중 업데이트 지원 미흡- 재설치 방식이라 롤백 복잡 |

### Docker/컨테이너 기반 접근 방식

- 일반적인 Docker는 애플리케이션 컨테이너화에 중점, OS 전체를 관리하지 않음
- bootc는 OS 자체를 컨테이너화하여 시스템 레벨의 관리 제공
- Docker 컨테이너는 일반적으로 부팅 가능한 시스템이 아닌 반면, bootc는 부팅 가능한 시스템 제공

### Ansible 기반 자동화

- Ansible은 Atomic/Immutable OS와 함께 사용하기에 이상적이지 않음
- bootc 기반 시스템에서 Ansible 사용은 "anti-pattern"으로 간주
- 패키지 설치나 시스템 수정이 bootc 철학과 충돌
- 기존 Ansible 자동화를 많이 보유한 조직은 전환이 어려울 수 있음

### cloud-init 기반 초기화

- cloud-init은 인스턴스의 첫 부팅 시 구성을 적용하는 도구
- bootc는 OS 전체의 업데이트 및 관리에 중점을 두는 반면, cloud-init은 초기 구성에 중점
- cloud-init은 bootc 환경 내에서도 사용 가능하며 상호 보완적
- 부팅 가능한 컨테이너 OS에서 cloud-init.service를 활성화하여 함께 사용

### PXE 부팅 방식

- PXE는 네트워크를 통해 OS를 부팅하는 방식
- bootc는 컨테이너 기반 업데이트를 제공하며, PXE와 함께 사용 가능
- HPC 클러스터와 같은 환경에서는 PXE를 통한 "stateless" OS 이미지 부팅이 일반적
- bootc는 PXE 부팅 환경과 결합하여 관리성을 높일 수 있음

## 계획

### 어디에 사용해볼까?

https://github.com/easy-cloud-Knet

- core(VM 생성 및 관리) 환경 세팅(심심할 때 마다 서버를 옮김) 및 private cloud 구성 시 설치 용이성 및 멱등성을 보장할 수 있도록 → debian linux 커널을 사용하도록 개발해두어([libvirt](https://libvirt.org/)+[KVM](https://aws.amazon.com/ko/what-is/kvm/)으로 VM 생성) 타 환경에서 사용하려면 OS 재설치가 필수적이던 문제를 bootc를 사용하면 설치 과정이 매우 간소화될 수 있음
- 오버헤드가 있지 않을까 싶어 동일 머신에서 설치 후 메트릭을 뽑아 비교해보고 싶음 → AI 시켜서 계산해봤는데 종류 무관 헛소리를..

- 네트워크 장비에서도 사용 가능할까?!

### 어떤 것을 해볼까?

- **bootc 실행 성공하기 (제일 중요)**
- bootc custom image(base image가 아닌 debian, ubuntu 등등) 생성해보기
- bootc로 환경 설정 성공
- bootc 환경에서의 오버헤드 정량적으로 측정해보기