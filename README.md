# 클라우드 클럽 7기 스터디 - OS image 기초 공사

## 1. Introduction

> [!NOTE]
>
> ### 스터디 소개
>
> OS image 기초 공사 스터디는, OS image를 효율적으로 빌드하고 관리하기 위한 방법을 배우는 스터디입니다.

---

<br>

### 🕑 Schedule & Members

- **기간**: 2025.05 ~ 2025.07 (8회)
- **시간**: 매주 목요일 저녁
- **장소**: 온라인 /오프라인
- **PR 제출 마감**: 스터디 1일 전 **수요일 오후 11:59**까지

<br>

### Who need this study?

- Infrastructure에 관심이 있는 사람
- 리눅스를 프로젝트를 통해 공부해보고 싶은 사람
- 컨테이너를 넘어 머신(노드) 레이어의 OS 구성을 직접 커스텀하고 자동화해서 배포해보고 싶은 사람 (CI/CD)

---

<br>

## 2. 👽 Our Squad

<table>
  <tr>
    <td align="center"><a href="https://github.com/yureutaejin"><img src="https://avatars.githubusercontent.com/u/85734054?v=4" width="100px;" alt=""/><br /><sub><b>
진윤태</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/Cybecho"><img src="https://avatars.githubusercontent.com/u/42949995?v=4" width="100px;" alt=""/><br /><sub><b>
소병욱</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/window9u"><img src="https://avatars.githubusercontent.com/u/121847433?v=4" width="100px;" alt=""/><br /><sub><b>문찬규</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/charlie3965"><img src="https://avatars.githubusercontent.com/u/19777578?v=4" width="100px;" alt=""/><br /><sub><b>
박천수</b></sub></a><br /></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/yucori"><img src="https://avatars.githubusercontent.com/u/110710238?v=4" width="100px;" alt=""/><br /><sub><b>
장지원</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/jskim096"><img src="https://avatars.githubusercontent.com/u/40004210?v=4" width="100px;" alt=""/><br /><sub><b>
김종석</b></sub></a><br /></td>
  </tr>
</table>

<br>

## 3. ⛳ Curriculum (Season - 2)

### Season 1 : 25.03.02 ~ 25.05.05

커리쿨럼은 매주 달라집니다. 당일에 모여 1) 목표를 정하고 2) 계획을 세우고 3) 진행하고 4) 정리합니다.

<br>

---

## 4. GitHub Collaboration Guidelines

> [!TIP]
> PR 및 Commenting on PR 예시는 이 [PR](https://github.com/cloud-club/rezero-homelab/pull/25)을 참고해주세요

리뷰어는 [reviewer-lottery](https://github.com/uesteibar/reviewer-lottery/tree/v3.1.0/)를 통해 자동 할당 됩니다.

### a. 디렉토리 구조

사이트 목차를 기반으로 디렉토리 구조를 구성합니다:

```
root
├── README.md
├── yuntae
│   ├── [task_name]
│   │   ├── README.md
│   │   └── ...
├── jongseok
│   ├── [task_name]
│   │   ├── README.md
│   │   └── ...
```

### b. 브랜치 규칙

- 브랜치명: `INITOS-{이름 대문자}/{task_name}` 형식으로 작성
- 예시: `INITOS-YUNTAE/create-sample-bootc`

### c. PR(Pull Request) 규칙

> [!TIP]
> 간략하게 써주시고 자세한 내용은 ./[taskname]/[user]/README.md에 작성해주세요.
> 리뷰어에게 README.md에 대한 부가적인 설명/질문이 필요하다면 이 [docs](https://docs.github.com/ko/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/commenting-on-a-pull-request)를 참고하여 comment를 남겨주세요

- PR 제목: `[INITOS-YUNTAE] - [taskname]` 형식으로 작성
- PR 내용은 아래에 따라 작성:

  ```markdown
  # Description

  여기에 개인 Repo PR 링크를 붙여 놓고 간단히 무엇을 어떻게 진행했는지 리스트 3줄로 써주시면 됩니다.  
  질문/부가 설명은 comment on pr로 남겨주세요.

  ## Question

  PR comment 외에 추가적으로 요약가능한 질문
  ```

## 5. Reference

- [bootc docs](https://bootc-dev.github.io/bootc/)
- [멀티 클라우드 환경에 호환가능한 클라우드 이미지 개발](https://www.youtube.com/watch?v=OxG_OfOH5h8)
- [cloud-init](https://velog.io/@ujeongoh/cloud-init-%EC%84%9C%EB%B9%84%EC%8A%A4)
- [NixOS](https://nixos.org/)
- [Talos](https://insight.infograb.net/blog/2024/08/14/introducing-talos/)

> [!WARNING]
>
> **출석 규정**
>
> 3회 이상 불참 시 7기를 수료할 수 없습니다.  
> 각 스터디 모임에 참여하지 못할 경우, 사전에 Slack으로 사유를 작성해주세요
