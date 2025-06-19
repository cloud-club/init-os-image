# Package Dependency Management

## Why I Studied

- bootc든 rpm-ostree든 Linux Packaging에 대해서 Immutable을 강화하는 것인데, 단순 패키징 자체에 집중하는 것이 아니라 Immutable과 Package Dependency에 대한 문제점을 바라보는 시각이 필요하다고 생각이 듦
- 기존 어떤 애플리케이션/서비스를 배포할 때도 항상 Package Dependency 문제는 있었음

## rpm-ostree

- RHEL/CentOS/Fedora의 특정 목적을 위한 파생 OS에서 사용하는 패키지 관리 시스템
- 이미지 기반 트리 를 구성하여 시스템 관리
- 패키지 모델: 전통적 패키지 + OSTree 이미지 스냅샷
- 사용자 패키지는 layered 패키지로 관리하되, 재부팅하는 방식으로 업데이트
- 환경 격리는 컨테이너가 필요함
  - 사용자 수준에서 개별 환경 격리 (***e.g.** 여러 버전의 Python 등)을 하려면 Container or Flatpak을 사용해야 함

## Flatpack

- Linux Desktop 애플리케이션 배포 실행을 위한 Sandboxing 기술
- 각 앱은 독립된 Runtime 환경에서 실행. 시스템 파일과 최소한만 공유하여 보안성 증가
- 각 앱은 필요한 라이브러리를 직접 포함하거나 Runtime으로 명시
- 한 번 빌드하면 여러 Linux 배포판에서 실행 가능
- 멀티 버전 공존
- flactpack portal를 통해 파일시스템, 카메라, 네트워크 접근 제어.

## Nix

![Nix Concept](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTG86Wx7asqWyXjg981CWwC1tQRMxu8JsUR1A&s)

- 순수 함수형 패키지
	- input이 같으면 result도 동일. (Reproducibility)
	- App, Dev Environment, OS 모두 구성 가능
- 멀티 버전 공존
- 롤백 기능
	- 시스템, 환경, 패키지를 이전 상태로 롤백
- 환경 격리
	- `nix-shell`, `flakes`, `nix develop` 등으로 개발 환경 격리 가능
- 무상태 배포
	- configuration.nix로 시스템 선언이 가능하며, declarative state 유지
- 캐시 활용
	- 패키지 빌드를 바이너리 캐시로 대체 가능
- 플랫폼 독립성
	- 어느 플랫폼이든 간에 동일한 방식으로 패키지 및 환경 관리
	- nixpkgs repository가 따로 존재
- 의존성 트리 명시적 관리
	- 모든 의존성이 명시적이며 투명하게 관리됨

### How Nix Works

- [Reference](https://nixos.org/guides/how-nix-works/)
- 모든 패키지(의존성 패키지도 포함)가 다음과 같이 저장됨
```bash
# /nix/store/{hash}-{package}-{version}/
/nix/store/b6gvzjyb2pg0kjfwrjmg1vfhh54ad73z-firefox-33.1/
```
- 각 패키지(의존성 패키지)는 버전/빌드 옵션 등에 따라 저장 경로가 달라짐 (모든게 동일해야 동일한 결과가 생성)
	- ex) hello 패키지의 glibc 버전이 다르면 다음과 같이 서로 다른 경로에 저장됨
		- `/nix/store/abcd1234-hello-2.10 (glibc 2.31 기반)`
		- `/nix/store/efgh5678-hello-2.10 (glibc 2.33 기반)`
- Nix 패키지의 derivattion(`.drv`) 파일(빌드 명세서)과 빌드된 아티팩트 Runtime 내부 참조에 경로 참조 정보가 포함됨.
	- `nix build`, `nix-env -i`, `nix-shell`, `nixos-rebuild` 등 실행 시에 `.nix` or `flake.nix` 파일을 통해 `.drv` 생성
	- 모든, 의존성 패키지 마저도 .drv를 가짐
	- ex) `/nix/store/abcd1234-hello-2.10.drv` 안에 `/nix/store/aaa1-glibc-2.31` 등의 경로가 의존성으로 포함됨
	- `ldd <binary package>`
	- `.drv` -> 빌드 -> `/nix/store/<해시>-<name>-<version>/`
	- 전체 빌드 그래프는 .drv 파일들 간의 참조 관계로 구성된다
	- .drv 예시
```drv
inputDrvs = {
  "/nix/store/aaa1-glibc-2.31.drv" = [ "out" ];
  "/nix/store/bbb2-coreutils-9.1.drv" = [ "out" ];
};
```

=> 완전한 재현성이 보장이 되며, 모든 종속 경로가 명시되므로 패키지 충돌 방지 및 멀티 버전 존재가 가능.

### Disadvantage
- 디스크 중복 증가 (거의 비슷한 패키지들의 내부적으로 거의 같은 의존성을 다르게 빌드해서 가져감)
	- 중복되는 의존성 패키지가 저장됨
- 각 패키지 별로 의존성 패키지 차이로 인한 성능/기능의 차이 발생 가능
- 조금이라도 해시가 다르면 캐시 최적화 저하

=> nixpkgs를 flake 등으로 그래프 전체 pinning하여 해결 시도.  
단 재현성(Reproduce)가 최우선이기 때문에 자동 최적화, 공유, 통합은 의도적으로 하지 않음.

## vs rpm-ostree

- immutability 자체는 유사.
	- rpm-ostree => /usr을 immutable image로 구성해서 OS 업데이트를 atomic하게 수행
	- Nix => 시스템뿐 아니라, 패키지, 환경, User Application까지 전부 Reproducible하게 구성
- package management
	- rpm-ostree => rpm + layered package
	- Nix => `/nix/store/<hash>-<package>-<version>`
- environment isolation
	- rpm-ostreee => toolbox, podman 추가 사용
	- nix-shell, nix develop + default.nix
-   Declaration format
	- rpm-ostree => fix /etc
	- NixOS => configuration.nix
