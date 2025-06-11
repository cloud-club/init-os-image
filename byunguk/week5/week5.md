# bootC + GitHub Actions Workflow + GitHub Self Hosted Runner ?
[ppt보기](https://docs.google.com/presentation/d/1gDvuMkLPdsOv68zSOi-mNTewdUSbYvFc/edit?usp=sharing&ouid=103204687067264269924&rtpof=true&sd=true)

## 무엇이 헷갈렸는가?

클라이언트 개발만 해봤던 내 입장에서 bootc는 그래도 컨테이너 기반의 OS 관리 도구라는 컨셉은 어렴풋이 이해했다. 하지만 GitHub Self-hosted Runner라는 것이 도대체 무엇이고, 왜 이걸 bootc와 함께 써야 하는지 전혀 감이 오지 않았다. 

더 헷갈렸던 건, 이게 bootc와 무슨 상관이 있다는 거였다. bootc는 OS를 컨테이너로 만드는 기술이고, GitHub Runner는 CI/CD를 돌리는 거라는데... 이 둘이 왜 만나야 하는지 도무지 감이 안 왔다.

bootc 이미지를 빌드하는데 굳이 내 서버를 사용해야 하는 이유가 뭔가? 이 모든 것들이 어떻게 연결되는 건지 도저히 그림이 그려지지 않았다.

하루컷 내려다가 포기했다. 이건 개념부터 제대로 잡고 가야겠다는 생각이 들었다.

## GitHub Actions Workflow, GitHub Self-hosted Runner 너 도대체 뭐야..?

bootc는 대충 컨셉정도는 이해했다고 생각했지만, GitHub Self-hosted Runner는 도대체 무엇인가? 개발 경험이래야 클라이언트단의 코드만 만졌던 내 수준에서는 사실 빌드-배포 파이프라인을 이해하기에 어려웠다. 

그래서 사실 날먹으로 self-hosted runner 과제를 하루컷 내보려고 했지만, 이거 컨셉을 이해하는 것부터 어려운데..? 안되겠다, 일단 이 둘의 컨셉을 '왜?' 쓰는지 정리하고, 이게 bootC와 어떻게 같이 쓰일 수 있을지 내용을 정리해보려고한다.

---

# GitHub Actions Workflow

## What is GitHub Actions Workflow ?

GitHub Actions Workflow는 코드 저장소에서 발생하는 이벤트(push, pull request 등)를 트리거로 하여 특정 작업을 자동으로 수행하도록 구성할 수 있는 자동화 도구다. 이게 왜 탄생했을까?

과거에는 개발자들이 코드를 수정하고 나서 매번 수동으로 빌드하고, 테스트하고, 배포하는 과정을 거쳐야 했다. 이 과정에서 사람의 실수가 발생하기 쉬웠고, 반복적인 작업으로 인한 비효율성이 컸다. GitHub Actions는 이런 불편함을 해결하기 위해 등장했다.

```
- Workflows: YAML 파일로 작성된 자동화 프로세스
- Jobs: 같은 실행 환경에서 돌아가는 작업 그룹
- Steps: 각 작업 내의 개별 명령어나 액션 GitHub
- Actions: 재사용 가능한 코드 블록
- Runners: 워크플로우를 실제로 실행하는 가상 머신 Codefresh
```

## Why GitHub Actions Workflow ?

예를 들어 이런 상황을 생각해보자. 당신이 웹 애플리케이션을 개발하고 있는데, 코드를 수정할 때마다 다음과 같은 과정을 거쳐야 한다고 가정해보자:

1. 코드 수정 완료
2. 로컬에서 빌드 테스트
3. 서버에 접속해서 기존 애플리케이션 중지
4. 새 코드로 다시 빌드
5. 애플리케이션 재시작
6. 동작 확인

이 과정을 매번 반복한다면? 정말 비효율적이고 실수하기 쉽다. GitHub Actions Workflow를 사용하면 main 브랜치에 코드를 push하는 순간 자동으로 빌드, 테스트, 배포까지 모든 과정이 자동화된다.

그래서 자동화가 필요했던 것이다. 코드를 GitHub에 푸시하면 알아서 테스트 돌리고, 빌드하고, 배포까지. 마치 공장의 컨베이어 벨트처럼.

## How to use GitHub Actions Workflow ?

GitHub Actions의 전체적인 흐름은 이렇다:

1. `.github/workflows/` 디렉토리에 YAML 파일로 워크플로우를 정의한다
2. 특정 이벤트(push, pull_request 등)가 발생하면 워크플로우가 트리거된다
3. 정의된 Job들이 순차적 또는 병렬로 실행된다
4. 각 Job 내의 Step들이 순서대로 실행된다

핵심은 모든 것이 코드로 정의되고 자동으로 실행된다는 점이다.

그런데 여기서 중요한 게 "어떤 환경에서 실행할지"다. 이게 바로 Runner인데...

---

# GitHub Self-hosted Runner

## What is GitHub Self-hosted Runner ?

결국 빌드라는것은 컴퓨팅 파워를 수반한다. GitHub Actions를 실행하려면 어딘가에서 실제로 코드가 돌아야 한다. 기본적으로는 GitHub이 제공하는 가상머신(GitHub-hosted runner)에서 돌아간다.

GitHub Self-hosted Runner는 GitHub Actions에서 사용자가 지정하는 로컬 컴퓨팅 자원으로 빌드를 수행하도록 설정하는 기능이다. 그럼 왜 GitHub에서 제공하는 기본 runner를 두고 굳이 내 서버를 사용해야 할까?

GitHub-hosted runner는 사용량에 따라 비용이 발생하고, 실행 시간에 제한이 있으며, 무엇보다 사용자가 환경을 자유롭게 커스터마이징할 수 없다는 한계가 있었다. 또한 내부 네트워크 자원에 접근이 어렵고, 보안상 민감한 작업을 GitHub의 서버에서 실행하기 부담스러운 경우가 많았다.

| 구분         | GitHub-hosted                     | Self-hosted                       |
|--------------|-----------------------------------|-----------------------------------|
| 관리 주체    | GitHub이 완전 관리                | 직접 관리 필요                    |
| 환경         | 매번 새로운 깨끗한 VM             | 지속적인 환경 (설정 가능)        |
| 성능         | 제한된 스펙 (2코어, 7GB RAM)      | 원하는 만큼 성능 확장            |
| 비용         | 사용량 기반 과금                  | 인프라 비용만 지불               |
| 커스터마이징 | 제한적                            | 완전한 자유도                    |
| 네트워크     | 동적 IP, 제한된 접근              | 내부 네트워크 접근 가능          |


## Why GitHub Self-hosted Runner ?

구체적인 시나리오로 설명해보자. 당신의 회사에서 다음과 같은 상황에 처했다고 가정해보자:

**시나리오**: 대용량 데이터를 처리하는 AI 모델을 개발하는 팀
- GitHub-hosted runner로는 메모리와 CPU가 부족해서 빌드가 자주 실패한다
- 빌드 시간이 6시간을 초과해서 GitHub의 시간 제한에 걸린다
- 회사 내부 데이터베이스에 접근해야 하는데 GitHub 서버에서는 접근이 불가능하다
- macOS 빌드가 필요한데 GitHub-hosted macOS runner 비용이 분당 $0.08로 너무 비싸다

이런 경우 Self-hosted Runner를 사용하면 자신의 서버 환경에서 원하는 하드웨어 스펙으로, 시간 제한 없이, 내부 네트워크에 접근하면서 빌드를 수행할 수 있다.

## How to use GitHub Self-hosted Runner ?

Self-hosted Runner 사용의 전체적인 흐름은 이렇다:

1. GitHub Repository의 Settings → Actions → Runners에서 "New self-hosted runner" 선택
2. 자신의 서버에 runner 애플리케이션을 다운로드하고 설치
3. GitHub에서 제공하는 토큰으로 runner를 등록
4. `./run.sh` 명령으로 runner를 실행
5. 워크플로우에서 `runs-on: self-hosted`로 지정하여 사용

핵심은 GitHub Actions의 job을 받아와서 자신의 서버에서 실행한다는 점이다. GitHub에서 job을 push하는 방식이 아니라, runner가 주기적으로 GitHub에 접속해서 job을 pull해오는 방식이라 보안상 더 안전하다.

이제 GitHub Actions와 Self-hosted Runner가 뭔지는 알겠다. 그런데 bootc와는 무슨 상관일까..?

---

# bootC + GitHub Actions Workflow + GitHub Self-hosted Runner

## 그렇다면, bootC는 GitHub Actions Workflow와 GitHub Self-hosted Runner와 어떤 연관이 있는가?

bootc는 컨테이너 이미지를 사용하여 운영체제를 관리하는 도구인데, 이 bootc 이미지를 빌드하고 배포하는 과정을 자동화하는 것이 바로 이 조합의 핵심이다.

생각해보자. bootc 이미지를 빌드하려면 상당한 시스템 리소스가 필요하고, 특정 권한과 도구들이 설치된 환경이 필요하다. 또한 빌드된 이미지를 Harbor나 Docker Hub 같은 레지스트리에 push해야 한다. 이 모든 과정을 매번 수동으로 하기에는 너무 번거롭다.

또한, GitHub의 호스팅된 러너는 약 14GB의 여유 디스크 공간을 제공하는데, bootc 이미지 빌드에는 부족할 수 있다. 또한 bootc 빌드 과정에서는 컨테이너의 보안 격리 기능을 대부분 해제하고, 컨테이너에게 호스트(Host) 시스템의 거의 모든 권한을 부여하기 위한 `--privileged` 모드가 필요하다.

이러한 이유로, 높은 권한이 요구되는 bootC를 CI/CD 파이프라인에서 실행하려면, 사실상 Self-hosted runner를 사용하는 것이 합리적이기 때문이다.

## 이렇게 함께 쓴다면, 어떤 이점을 누릴 수 있는가?

구체적인 시나리오로 설명해보자:

**시나리오**: 수백대 이상의 엣지 디바이스용 Linux 시스템을 관리하는 팀, 각 기기의 OS를 업데이트 해야 한다면?
1. 개발자가 bootc 이미지의 소스코드(Containerfile)를 수정하고 GitHub에 push한다
2. GitHub Actions Workflow가 자동으로 트리거된다
3. Self-hosted Runner에서 bootc 이미지 빌드가 시작된다 (GitHub-hosted runner로는 리소스 부족)
4. 빌드된 이미지가 자동으로 Harbor 레지스트리에 push된다
5. GitOps 도구(ArgoCD 등)가 새 이미지를 감지하고 엣지 디바이스들에 자동 배포한다

이렇게 하면 코드 한 번 push로 전체 시스템 업데이트가 자동화된다. 그리고 bootc를 사용하기에, 문제가 생긴다면 이전 이미지로의 롤백도 간편하여, 수백 대의 엣지 디바이스를 일일이 관리할 필요가 없어진다.


## 그렇다면, 어떤식으로 구현할 수 있는가?

전체적인 구현 흐름은 이렇다:

1. **준비 단계**: Self-hosted Runner 서버에 Docker, bootc-image-builder 등 필요한 도구들을 설치한다
2. **워크플로우 정의**: `.github/workflows/`에 bootc 이미지 빌드를 위한 YAML 파일을 작성한다
3. **빌드 자동화**: Containerfile이 수정되면 자동으로 `podman build` 또는 `bootc-image-builder`를 실행한다
4. **레지스트리 push**: 빌드된 이미지를 Harbor/Docker Hub에 자동으로 push한다
5. **배포 연동**: GitOps 도구와 연동하여 새 이미지 배포를 자동화한다

핵심은 모든 과정이 코드로 정의되고 자동으로 실행된다는 점이다.

---

# 결론

## 이 세 기술을 굳이 함께 사용했던 이유?

결국 이 조합이 필요했던 이유는 '자동화'와 '확장성' 때문이었다. bootc 이미지 하나하나를 수동으로 빌드하고 배포하기에는 너무 비효율적이고 실수하기 쉬웠다. GitHub Actions로 자동화를 구현하되, 빌드 작업이 무겁고 특수한 환경이 필요해서 Self-hosted Runner를 사용하게 된 것이다.

## bootc 이미지 빌드부터 Harbor/Docker Hub Registry에 push하는 것을 구현하기 위해, 이 기술들이 사용되었던 이유?

bootc 이미지 빌드는 일반적인 애플리케이션 빌드와 다르다. 운영체제 전체를 이미지로 만드는 작업이기 때문에 더 많은 리소스와 권한이 필요하고, 빌드 시간도 오래 걸린다. GitHub-hosted runner로는 한계가 있어서 Self-hosted Runner가 필요했던 것이다.

또한 빌드된 이미지를 Harbor나 Docker Hub에 자동으로 push하려면 CI/CD 파이프라인이 필요했는데, GitHub Actions가 이를 가장 간편하게 구현할 수 있는 방법이었다.

## 기대효과

이 조합을 통해 얻을 수 있는 효과는 명확하다:

1. **개발 생산성 향상**: 코드 push 한 번으로 전체 시스템 업데이트가 자동화된다
2. **운영 비용 절감**: GitHub-hosted runner 비용을 절약하고, 수동 작업을 줄인다
3. **보안 강화**: 내부 네트워크 환경에서 안전하게 빌드할 수 있다
4. **확장성 확보**: 수십, 수백 개의 시스템을 일관되게 관리할 수 있다

결국 이 모든 것은 '컨테이너 기반 OS 관리의 완전 자동화'를 위한 것이었다. bootc라는 새로운 기술을 실제 프로덕션에서 활용하기 위해서는 이런 자동화 인프라가 반드시 필요했던 것이다.

## 참고자료

- [GitHub Actions에 Self-hosted Runner 등록 가이드 (설치, 설정, 활용, 장단점 포함)](https://danawalab.github.io/common/2022/08/24/Self-Hosted-Runner.html)
- [Self-hosted Runner 개념, 지원 OS, 설치 및 관리 방법, 보안 및 그룹 관리까지](https://www.korgithub.com/Ch4.GitHub%20Actions/04.Action%EB%9F%AC%EB%84%88/02.Self-hosted-runner.html)
- [GitHub Hosted Runner와 Self-hosted Runner 차이점 및 개념 정리](https://velog.io/@dksek3050/CICD-GitHub-hosted-runner-%EC%99%80-Self-hosted-runner-%EB%9E%80)
- [GitHub Actions 구조와 활용법](https://thinkingtool.tistory.com/entry/GitHub-Actions%EC%9D%98-%EA%B5%AC%EC%A1%B0%EC%99%80-%ED%99%9C%EC%9A%A9%EB%B2%95)
- [GitHub Actions 기초 및 실습 예제](https://bumday.tistory.com/90)
- [GitHub Actions로 CI/CD 구축하기](https://seungjjun.tistory.com/316)
- [GitHub Actions 정리 및 실습](https://kfdd6630.tistory.com/entry/GitHub-GitHub-Actions-%EC%A0%95%EB%A6%AC)
- [GitHub Actions Workflow 작성 및 활용 예시](https://domae.tistory.com/183)
- [GitHub Actions 소개 및 사용법](https://tech-recipe.tistory.com/31)
- [Linux에서 bootc 이미지 관리 및 활용](https://tech.chhanz.xyz/linux/2025/03/09/bootc/)
- [RHEL 10 bootc 시스템에서 커널 인자 관리 방법](https://docs.redhat.com/ko/documentation/red_hat_enterprise_linux/10/html/using_image_mode_for_rhel_to_build_deploy_and_manage_operating_systems/managing-kernel-arguments-in-bootc-systems)
- [RHEL 10 bootc로 컨테이너 이미지 배포 방법](https://docs.redhat.com/ko/documentation/red_hat_enterprise_linux/10/html/using_image_mode_for_rhel_to_build_deploy_and_manage_operating_systems/deploying-a-container-image-by-using-bootc)
- [RHEL bootc 이미지 배포 방법](https://docs.redhat.com/ko/documentation/red_hat_enterprise_linux/10/html/using_image_mode_for_rhel_to_build_deploy_and_manage_operating_systems/deploying-the-rhel-bootc-images)
- [GitHub Actions 입문 및 실습 가이드](https://umanking.github.io/2023/03/06/github-action-starter/)
- [GitHub Actions로 CI/CD 실습](https://velog.io/@hyeongjun-hub/Github-Actions%EB%B6%80%ED%84%B0-CICD-%EC%8B%A4%EC%8A%B5%EA%B9%8C%EC%A7%80)
- [GitHub Actions Workflow 작성 팁](https://wildeveloperetrain.tistory.com/401)
- [GitHub Actions로 자동 배포 환경 구축](https://hello-judy-world.tistory.com/210)
- [RHEL bootc 이미지 관리 방법](https://docs.redhat.com/ko/documentation/red_hat_enterprise_linux/10/html/using_image_mode_for_rhel_to_build_deploy_and_manage_operating_systems/managing-rhel-bootc-images)
- [GitHub Actions로 배포 자동화](https://zzang9ha.tistory.com/404)
- [GitHub Actions로 CI/CD 구축하기 (간단 예제)](https://ddohyung.tistory.com/13)
- [GitHub Actions 요금제 및 과금 관리 안내 (공식 문서)](https://docs.github.com/ko/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions)
- [GitHub Actions Billing (영문 공식 문서)](https://docs.github.com/billing/managing-billing-for-github-actions/about-billing-for-github-actions)
- [GitHub Actions job별 시간 제한 설정 방법](https://mong-blog.tistory.com/entry/github-Actions-job%EB%B3%84%EB%A1%9C-%EC%8B%9C%EA%B0%84-%EC%A0%9C%ED%95%9C-%EA%B1%B8%EA%B8%B0-timeout-minutes)
- [GitHub Actions 자동 배포 예제](https://dalsim777-tech.tistory.com/22)
- [GitHub Actions 사용량, 제한, 과금, 관리 (공식 문서)](https://docs.github.com/ko/enterprise-cloud@latest/actions/administering-github-actions/usage-limits-billing-and-administration)
- [GitHub Actions 기초 및 실습 예제](https://stdhsw.tistory.com/141)
- [GitHub Actions로 Spring Boot 배포 자동화](https://hkjeon2.tistory.com/197)
- [GitHub Actions로 CI/CD 파이프라인 구축](https://whxogus215.tistory.com/105)
- [쿠버네티스 환경에서 GitOps 구축 방법](https://jsyeo.tistory.com/entry/kubeadm%EC%9C%BC%EB%A1%9C-%EA%B5%AC%EC%B6%95%ED%95%9C-%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4-%ED%99%98%EA%B2%BD%EC%97%90%EC%84%9C-GitOps-%EA%B5%AC%EC%B6%95)
- [RHEL 10 bootc 이미지 관리 및 배포 PDF 가이드](https://docs.redhat.com/ko/documentation/red_hat_enterprise_linux/10/pdf/using_image_mode_for_rhel_to_build_deploy_and_manage_operating_systems/Red_Hat_Enterprise_Linux-10-Using_image_mode_for_RHEL_to_build_deploy_and_manage_operating_systems-ko-KR.pdf)
- [GitHub Actions로 CI/CD 파이프라인 구축 실습](https://coding-business.tistory.com/136)
- [RHEL 이미지 모드에서 CICD 파이프라인 구축](https://developers.redhat.com/articles/2024/11/22/creating-cicd-pipelines-image-mode-rhel)
- [GitHub Actions CI/CD 구축 실습](https://lucas-owner.tistory.com/49)
- [Docker와 GitHub Actions로 Spring Boot CICD 구축](https://velog.io/@zvyg1023/CICD-Docker-Github-Action-Spring-Boot)
- [GitHub Actions로 자동 배포 환경 구축](https://cholol.tistory.com/606)
- [GitHub Actions로 이미지 빌드 후 GitHub Registry에 올리기](https://velog.io/@juyoung810/Github-Action-%EC%9C%BC%EB%A1%9C-image-build-%ED%95%B4-github-image-Registry-%EC%97%90-%EC%98%AC%EB%A6%AC%EA%B8%B0)
- [GitHub Actions로 CI/CD 구축 실습](https://righteous.tistory.com/30)
- [GitHub Container Registry에 Push 실패 시 해결 방법 (Stack Overflow)](https://stackoverflow.com/questions/76389568/failed-pushing-to-github-container-registry)
- [GitHub Actions Self-hosted Runner 소개](https://velog.io/@zuckerfrei/Github-Actions-1.-self-hosted-runner)
- [Self-hosted Runner 관리 및 활용 (공식 문서)](https://docs.github.com/ko/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)
- [GitHub Actions 관련 최신 소식 및 팁](https://news.hada.io/topic?id=20479)
- [IT 부트캠프 용어 및 기원 설명](https://codelabsacademy.com/ko/blog/what-is-the-meaning-of-the-term-bootcamp-and-where-did-it-originate-from/)
- [CI/CD 관련 소식 및 팁](https://news.hada.io/topic?id=19473)
- [GitHub Actions로 자동 배포 환경 구축 실습](https://dkswnkk.tistory.com/674)
- [GitHub Actions로 CI/CD 구축 실습](https://hulrud.tistory.com/106)
- [GitHub Actions와 Docker로 CICD 구축](https://velog.io/@leeeeeyeon/Github-Actions%EA%B3%BC-Docker%EC%9D%84-%ED%99%9C%EC%9A%A9%ED%95%9C-CICD-%EA%B5%AC%EC%B6%95)
- [GitHub Actions Larger Runner 사용 방법 및 성능 비교](https://blog.kmong.com/github-actions%EC%9D%98-%EB%8A%90%EB%A0%A4%ED%84%B0%EC%A7%84-%EC%84%B1%EB%8A%A5%EC%9D%84-%ED%9A%8C%EC%82%AC-%EB%8F%88-%EC%A3%BC%EA%B3%A0-%EC%82%AC%EB%B3%B4%EC%9E%90-github-hosted-larger-runners-%EC%82%AC%EC%9A%A9%EA%B8%B0-ec27427f1501)
- [GitHub Hosted Runner 소개 및 활용법 (공식 문서)](https://docs.github.com/ko/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners)
- [Harbor를 활용한 프라이빗 Docker 레지스트리 구축 (LINE Engineering)](https://engineering.linecorp.com/ko/blog/harbor-for-private-docker-registry/)
- [Harbor란? 개념 및 사용법](https://kimmj.github.io/harbor/what-is-harbor/)
- [Docker와 CI/CD 파이프라인 구축 실습](https://waspro.tistory.com/631)
- [DevOps와 Docker 가상화 기술 강의 안내](https://www.inflearn.com/course/devops-docker-%EA%B0%80%EC%83%81%ED%99%94-%EA%B8%B0%EC%88%A0)
- [GitHub Actions와 Docker로 Spring Boot 자동 배포 시스템 구축](https://velog.io/@jinkonu/Github-Actions-Docker%EB%A1%9C-%EC%8A%A4%ED%94%84%EB%A7%81-%EB%B6%80%ED%8A%B8-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EC%9E%90%EB%8F%99-%EB%B0%B0%ED%8F%AC-%EC%8B%9C%EC%8A%A4%ED%85%9C-%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0)
- [GitHub Actions로 CI/CD 파이프라인 구축 실습](https://yejin-code.tistory.com/51)
