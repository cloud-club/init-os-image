# 비유로 이해해보자 : ostree , rpm , 그리고 bootc

### ostree 등장 배경

"Fedora 40 환경에서 열심히 꾸민 GNOME RICING이, Fedora 41로 업데이트하면서 상당 부분 깨져버렸던 기억..." 

 중요한 작업을 앞두고, 혹은 애써 설정해둔 환경이 업데이트 한 번으로 틀어지는 순간의 당혹감이란 이루 말할 수 없죠.

마치 잘 달리던 자동차가 정비 후 사소한 부품 하나 때문에 삐걱거리기 시작하는 것과 비슷할까요? 이런 불안함과 불편함을 해결하기 위해 **ostree**라는 기술이 등장했습니다.

### ostree: "OS, 마치 '출판된 책'처럼 다루다"

ostree는 운영체제(OS)를 관리하는 새로운 접근 방식입니다. 핵심 아이디어는 OS를 '잘 제본된 출판 도서'처럼 다루는 것입니다.

- **불변성 (수정 불가 원칙):** OS의 핵심 내용물(예: `/usr` 디렉토리, 시스템 명령어와 라이브러리가 있는 곳)은 일단 '출판'되면 그 내용을 변경할 수 없습니다. 마치 인쇄가 완료된 책의 본문을 수정할 수 없는 것처럼요. 이를 통해 시스템 핵심부가 예기치 않게 변경될 가능성이 크게 줄어듭니다.
- **원자적 업데이트 (완벽한 교체):** 업데이트는 마치 책의 '개정판'으로 교체하는 것과 같습니다. 이전 판을 그대로 보존한 채, 완전히 새로운 '개정판'으로 시스템을 전환합니다. 이 전환은 매우 깔끔하게 이루어져서, 문제가 생겨도 즉시 이전 판으로 돌아갈 수 있습니다. 시스템이 불완전한 상태에 놓이는 일이 없죠.

**ostree의 장점:** 업데이트 실패를 걱정하지 않고도 언제든 이전 상태로 돌아갈 수 있는 안정감. 시스템은 항상 예측 가능한 상태를 유지합니다. 마치 중요한 문서 작업할 때 단계별로 버전을 저장해두는 것처럼 든든하죠.

### ostree 대 전통적 리눅스: 무엇이 다를까?

| **구분** | **전통적 리눅스** | **ostree 기반 OS** |
| --- | --- | --- |
| **업데이트 방식** | 개별 부품 교체식. 호환성 문제 발생 가능. | 완성차 교체식. 테스트 완료된 상태로 제공. |
| **안정성** | 부품 교체 중 시스템 불안정 위험. | 문제 발생 시 이전 버전으로 즉시 복구. |
| **핵심 파일 관리** | 자유로운 수정 가능. 위험 부담 있음. | 핵심 시스템 변경 불가. (단,`/etc`,`/var`수정 가능) |

### ostree의 든든한 지원군: rpm-ostree 와 bootc

ostree의 강력한 기반 위에 더욱 편리한 기능을 제공하는 기술들이 있습니다.

### 1. rpm-ostree: "출판된 책에 '공식 부록'을 추가하다"

**rpm-ostree**는 ostree로 관리되는 안정적인 OS '책' 위에 우리가 필요로 하는 추가 프로그램(RPM 패키지)을 마치 **'공식 부록'이나 '별책'처럼 안전하게 추가**할 수 있게 해줍니다.

- **어떻게?** 기본 OS '책'의 내용은 그대로 보존하면서, 그 위에 필요한 프로그램들을 '레이어' 형태로 덧붙여 새로운 합본 서적을 만듭니다. 이는 전체 시스템 이미지 단위로 관리되어 안전합니다.
    - **예시:** 기본 전공서적(ostree)을 그대로 두고, 교수님이 추천한 참고자료(RPM 패키지)를 함께 제본하여 나만의 학습자료 세트를 만드는 것과 같습니다. 원본 서적은 온전히 보존됩니다.

### 2. bootc: "OS를 '표준 규격의 조립식 주택'처럼 관리하다"

- bootc(Bootable Containers)는 한 단계 더 나아가 운영체제 자체를 OCI 컨테이너 이미지라는 '국제 표준 규격의 조립식 주택 설계도'처럼 취급하고 배포합니다.
- **rpm-ostree와 뭐가 다를까요?**
    - **업데이트 소스:** bootc는 OCI 이미지를 통해 OS 업데이트를 받습니다. 마치 전 세계 어디서나 동일한 규격으로 제작된 '조립식 주택 키트'를 받는 것과 같죠.
    - **철학:** rpm-ostree가 기존 OS에 유연하게 프로그램을 추가하는 데 중점을 둔다면, bootc는 "OS는 검증된 표준 설계도(OCI 이미지)를 그대로 사용하는 것이 가장 안정적이고 효율적이다"라는 관점을 가집니다.
- **OCI 이미지 사용의 장점:**
    - 널리 사용되는 컨테이너 기술 표준(OCI)을 활용하므로, OS를 만들고, 배포하고, 관리하는 전체 과정이 훨씬 **단순해지고 빨라집니다.**
    - **예시:** 전 세계 어디서든 동일한 품질과 규격의 건축 자재로 집을 짓는 것처럼, OCI 이미지로 다양한 환경에서 일관된 OS를 손쉽게 구축하고 운영할 수 있습니다.

### ostree와 OverlayFS의 만남은 마치 책의 특별 부록과 유사하다

읽기 전용인 ostree 시스템의 '책' 내용을 임시로 수정해야 할 때가 있습니다. 예를 들어 개발 테스트를 위해 시스템 파일을 잠시 변경해야 하는 경우죠. 이럴 때 **OverlayFS**가 마법 같은 해결책을 제공합니다.

- **OverlayFS 역할:** 읽기 전용인 ostree의 OS '책' 위에 '투명한 필름(Overlay)'을 한 장 덮는다고 생각해보세요.
    - **ostree (원본 책):** 절대 변하지 않는 원본 내용을 보존합니다. (안정성!)
    - **OverlayFS (투명 필름):** 이 필름 위에 자유롭게 임시 메모나 수정 사항을 기록할 수 있습니다. 작업이 끝나고 필름을 걷어내면(예: 재부팅) 원본 책은 깨끗하게 보존되어 있습니다.

### 마무리

ostree, rpm-ostree, bootc는 우리의 컴퓨터를 더 안전하고 믿을 수 있게 만드는 도구입니다. 마치 컴퓨터를 위한 보험과 같아서, 문제가 생겨도 쉽게 복구할 수 있죠. 여기에 OverlayFS는 필요할 때 시스템을 잠시 수정할 수 있는 편리함을 더해줍니다.

이러한 기술들 덕분에 우리는 이제 컴퓨터가 갑자기 망가질까 걱정하지 않고 편하게 작업할 수 있게 되었습니다. 여러분이 공들여 꾸민 데스크톱 환경도 다음 업데이트 때는 안전하게 유지될 수 있을 거예요.

---

# 스터디장님의 퀘스트…

1. **Fedora/RHEL CoreOS에서 사용되는 OSTree는 무엇이며, 어떤 장점을 제공하는가?**
    - OSTree는 Linux 기반 운영 체제를 위한 업그레이드 시스템으로, 완전한 파일 시스템 트리의 원자적(atomic) 업그레이드를 수행합니다.
    - 이는 패키지 시스템이 아니라 패키지 시스템을 보완하는 도구입니다.
    - OSTree의 주요 장점은 다음과 같습니다:
        - **원자적이고 안전한 업그레이드**: 업그레이드 중 시스템이 충돌하거나 전원이 꺼져도 시스템은 이전 상태나 새로운 상태 중 하나로 유지되며, 불완전한 상태가 되지 않습니다.
        - **불변성(Immutable)**: OS의 핵심 콘텐츠(`/usr`)는 기본적으로 읽기 전용으로 관리되어 우발적인 손상을 방지합니다.
        - **병렬 설치**: 여러 버전의 운영 체제를 동시에 설치하고 부팅할 수 있습니다.
        - **스토리지 효율성**: Git과 유사한 콘텐츠 주소 지정 저장소를 사용하여 파일을 체크섬으로 관리하고, 하드링크로 여러 배포본 간 파일을 중복 없이 저장합니다. 업그레이드 시에는 변경된 파일만 저장하여 공간을 절약합니다.
        - **유연성**: 모든 파일 시스템이나 블록 스토리지 레이아웃에서 작동합니다.
        - **비중단 업데이트**: 업데이트가 실행 중인 시스템을 변경하지 않고 새로운 루트 디렉토리에 작성됩니다.
2. **OSTree의 불변성(immutable)과 원자적 업데이트(atomic update) 특성은 무엇인가?**
    - **불변성(Immutability)**:
        - 배포된 시스템에서 `/usr` 디렉토리는 런타임에 읽기 전용으로 마운트됩니다.
        - 시스템의 핵심 파일들은 변경할 수 없게 관리됩니다.
        - `/etc`와 `/var`는 변경 가능한 상태 관리를 위해 별도로 분리됩니다.
    - **원자적 업데이트(Atomic Update)**:
        - OSTree는 부팅 가능한 배포본들 간의 트랜잭션 전환을 구현하도록 설계되었습니다.
        - 업데이트는 오프라인에서 새로운 파일 시스템 트리를 생성하고, 부팅 시 이전 트리와 새로운 트리를 원자적으로 전환합니다.
        - 이 전환은 `/boot` 디렉토리 내 심볼릭 링크를 원자적으로 교체하고, 부트로더(GRUB 등) 설정 파일(`/boot/loader/entries`)을 업데이트하여 이루어집니다.
        - 이러한 방식으로 업데이트 중 문제가 발생해도 이전 상태로 안전하게 돌아갈 수 있습니다.
3. **다른 Linux 배포판과 비교할 때 OSTree는 어떻게 다른가?**
    - **패키지 관리자 관점**:
        - 전통적인 패키지 관리자(dpkg, rpm, yum, dnf)는 파일 시스템 트리, 메타데이터, 스크립트로 구성된 패키지를 클라이언트에서 동적으로 조립합니다.
        - OSTree는 서버에서 미리 생성된 완전한 파일 시스템 트리를 복제하여 배포합니다. 업데이트는 개별 파일이 아닌 전체 트리 단위로 이루어집니다.
        - OSTree는 패키지 시스템과 함께 사용될 수 있으며, 패키지 관리자는 실행 중인 파일 시스템을 직접 수정하는 대신 새로운 파일 시스템 트리를 구성하여 OSTree 저장소에 기록합니다.
    - **스냅샷 방식 관점**:
        - BTRFS/LVM과 같은 파일 시스템/볼륨 관리자 기반 스냅샷 도구는 패키지 관리자 *아래*에서 전체 파일 시스템의 스냅샷을 생성합니다.
        - OSTree는 파일 시스템 수준에서 콘텐츠 주소 지정 저장소와 하드링크로 트리를 버전 관리하고 배포를 관리합니다. 특정 블록 스토리지 기능에 의존하지 않아 모든 Unix 호환 파일 시스템에서 작동합니다.
        - 업데이트는 스냅샷과 유사해 보이지만, OSTree는 여러 배포본을 `/ostree/deploy` 디렉토리 아래에 별도로 관리하고 `/ostree/repo`를 통해 데이터를 공유합니다. 업데이트는 새로운 루트로 작성됩니다.
    - **파일 시스템 관점**:
        - 일반적인 Linux 배포판은 `/`, `/usr`, `/etc`, `/var` 등 모든 디렉토리가 기본적으로 변경 가능합니다.
        - OSTree는 `/usr`을 읽기 전용 불변 영역으로, `/etc`를 변경 가능한 시스템 설정 영역으로, `/var`를 배포본 간 공유되는 변경 가능 데이터 영역으로 명확히 구분합니다. `/ostree` 디렉토리로 저장소와 배포본을 관리합니다.

---

# boot C 이미지 직접 만들어보자

## **최종 목표:**

VirtualBox에서 바로 부팅하여 웹 서버("성공!" 페이지를 보여주는)로 작동하는, 이식성 좋은 VDI 디스크 이미지를 만드는 것.

## **핵심 아이디어 (생각의 흐름):**

1. **"매번 빌드 환경을 수동으로 설정하기는 번거롭고 오류가 생기기 쉬워."**
    - **해결책:** `Vagrant`를 사용하자! `Vagrantfile` 하나로 빌드에 필요한 모든 도구(Podman, QEMU 유틸리티 등)가 설치된 깨끗한 Ubuntu 가상 머신(VM)을 자동으로 만들 수 있다. 덕분에 어떤 컴퓨터에서 작업하든 동일한 빌드 환경을 보장받을 수 있다.
2. **"내가 원하는 최종 OS와 애플리케이션은 어떻게 정의하지?"**
    - **해결책:** `Containerfile`(Dockerfile과 유사)을 사용하자! 여기에 기반 OS(CentOS Stream 9 bootC 이미지)를 지정하고, 웹 서버(Apache httpd)를 설치하고, 웹페이지(`index.html`)를 복사하고, 커널 부팅 인수(`kargs`)를 설정하는 등 모든 "설계도"를 담을 수 있다.
3. **"설계도(`Containerfile`)를 실제 실행 가능한 형태로 만들려면?"**
    - **해결책:** `podman build`를 사용하자! Vagrant VM 안에서 `podman`으로 `Containerfile`을 빌드하여 OCI 표준 컨테이너 이미지를 생성한다. 이 컨테이너 이미지가 OS와 애플리케이션이 담긴 "중간 결과물"이다.
4. **"컨테이너 이미지는 그 자체로 VM에서 부팅할 수 없는데, 어떻게 부팅 가능한 디스크 이미지로 만들지?"**
    - **해결책:** `bootc-image-builder`를 사용하자! 이 도구는 OCI 컨테이너 이미지를 받아서 실제 하이퍼바이저(VirtualBox 등)에서 부팅 가능한 디스크 이미지(예: QCOW2)로 변환해 준다. 이때 `config.toml` 파일로 로그인 계정도 추가할 수 있다.
5. **"VirtualBox를 주로 사용하는데, QCOW2보다는 VDI 형식이 더 좋지 않을까?"**
    - **해결책:** `qemu-img`를 사용하자! `bootc-image-builder`가 만든 QCOW2 파일을 VirtualBox 전용 VDI로 변환하면 호환성과 성능이 더 좋아진다.
6. **"빌드 VM 안에서 만들어진 VDI 파일을 내 PC로 가져와서 사용하고 싶어."**
    - **해결책:** `vagrant scp`를 사용하자! 이 플러그인으로 VM 안의 VDI 파일을 내 PC로 쉽게 복사할 수 있다.
7. **"이제 VDI 파일이 생겼으니, 이걸로 새 VirtualBox VM을 만들어서 부팅해보자!"**
    - **최종 단계:** VirtualBox에서 새 VM을 만들고 방금 복사한 VDI 파일을 하드 디스크로 지정한다. VM을 시작하면 CentOS Stream 9 기반 웹 서버가 부팅되고, 포트 포워딩을 통해 호스트 PC에서 "성공!" 페이지를 볼 수 있다.

## **전체 구축 및 생성 흐름**

### **Phase 1: 빌드 환경 자동화 (Vagrant)**

- **의도**: bootC 이미지 빌드에 필요한 모든 도구와 설정이 완료된 격리된 Ubuntu 가상 머신 환경을 `Vagrantfile`을 통해 자동으로 구축합니다. 이를 통해 수동 설정의 번거로움을 줄이고, 어떤 환경에서든 동일한 빌드 결과를 보장받습니다.
- **`Vagrantfile` 주요 구성**:
    
    ```ruby
    # -*- mode: ruby -*-
    # vi: set ft=ruby :
    
    Vagrant.configure("2") do |config|
      # Ubuntu 22.04 LTS (Jammy Jellyfish) 이미지 사용
      config.vm.box = "ubuntu/jammy64"
    
      # VM 설정
      config.vm.provider "virtualbox" do |vb|
        vb.name = "Ubuntu-bootC"
        vb.memory = 4096
        vb.cpus = 2
      end
    
      # 포트 포워딩 설정 (최종 생성될 VDI를 사용하는 VM을 위함)
      config.vm.network "forwarded_port", guest: 80, host: 8080
    
      # VM 프로비저닝 스크립트
      config.vm.provision "shell", inline: <<-SHELL
        # 패키지 목록 업데이트
        apt-get update
    
        # 필요한 기본 패키지 설치
        apt-get install -y podman git curl qemu-utils
    
        # bootC 이미지 빌드 준비 디렉터리 생성 및 이동
        sudo -u vagrant mkdir -p /home/vagrant/bootc-webserver
        cd /home/vagrant/bootc-webserver
    
        # CentOS Stream 9 bootC 기본 이미지 가져오기
        sudo podman pull quay.io/centos-bootc/centos-bootc:stream9
    
        # Containerfile 동적 생성 (내용은 아래 Phase 2 참조)
        cat > /home/vagrant/bootc-webserver/Containerfile << 'EOL'
    # ... Containerfile 내용 ...
    EOL
    
        # 웹페이지 파일(index.html) 동적 생성
        cat > /home/vagrant/bootc-webserver/index.html << 'EOL'
    <!DOCTYPE html>
    <html>
    <head>
        <title>My First bootC Web Server</title>
    </head>
    <body>
        <h1>성공!</h1>
        <p>bootC로 빌드한 웹서버가 실행 중입니다!</p>
    </body>
    </html>
    EOL
    
        # 출력 디렉토리 생성
        mkdir -p /home/vagrant/bootc-webserver/output
    
        # 파일 소유권 변경
        chown -R vagrant:vagrant /home/vagrant/bootc-webserver
    
        # 완료 메시지 출력
        echo "환경 설정이 완료되었습니다."
        # ... (후략) ...
      SHELL
    end
    
    ```
    
- **실행**: 호스트 PC에서 `vagrant up` 명령을 실행합니다.
- **결과**: `Ubuntu-bootC`라는 이름의 Ubuntu VM이 VirtualBox에 생성되고, 프로비저닝 스크립트에 따라 필요한 도구 설치 및 `Containerfile`, `index.html` 파일 생성이 완료됩니다. `/home/vagrant/bootc-webserver` 디렉터리에 빌드 준비가 완료됩니다.

### **Phase 2: OS 및 애플리케이션 정의 (`Containerfile`)**

- **의도**: 부팅될 최종 운영체제의 구성 요소(기반 OS, 설치될 패키지, 서비스 설정, 커널 부팅 인수, 복사될 파일 등)를 `Containerfile`에 명세합니다. 이는 컨테이너 이미지의 "설계도" 역할을 합니다.
- **`Containerfile` 내용**:
    
    ```
    FROM quay.io/centos-bootc/centos-bootc:stream9
    
    # 웹서버(httpd) 설치 및 활성화
    RUN dnf -y install httpd && \\
        systemctl enable httpd && \\
        mv /var/www /usr/share/www && \\
        echo 'd /var/log/httpd 0700 - - -' > /usr/lib/tmpfiles.d/httpd-log.conf && \\
        sed -ie 's,/var/www,/usr/share/www,' /etc/httpd/conf/httpd.conf
    
    # 부팅 인수 설정을 위한 디렉토리 생성
    RUN mkdir -p /usr/lib/bootc/kargs.d
    
    # 부팅 인수 설정 (직렬 콘솔 활성화)
    RUN echo 'kargs = ["console=ttyS0,115200n8"]' > /usr/lib/bootc/kargs.d/kcmdline.toml
    
    # 기본 index.html 제거
    RUN rm /usr/share/httpd/noindex -rf
    
    # 사용자 지정 웹페이지 추가
    COPY index.html /usr/share/www/html/
    
    # 포트 노출 (컨테이너 레벨)
    EXPOSE 80
    
    ```
    

### **Phase 3: OCI 컨테이너 이미지 빌드 (Podman)**

- **의도**: `Containerfile`을 기반으로 표준 OCI 컨테이너 이미지를 생성합니다. 이 이미지는 정의된 OS와 애플리케이션을 포함하는 실행 가능한 패키지이지만, 아직 VM에서 직접 부팅할 수 있는 형태는 아닙니다.
- **실행 (Ubuntu VM 내부에서)**:
    1. `vagrant ssh` (호스트 PC에서 VM 접속)
    2. `cd ~/bootc-webserver`
    3. `sudo podman build -t my-bootc-webserver .`
- **결과**: `localhost/my-bootc-webserver:latest`라는 이름과 태그를 가진 OCI 컨테이너 이미지가 Ubuntu VM 내부의 Podman 로컬 저장소에 생성됩니다.

### **Phase 4: 부팅 가능 QCOW2 디스크 이미지 생성 (bootc-image-builder)**

- **의도**: Podman으로 빌드한 OCI 컨테이너 이미지를 KVM/QEMU 등 가상화 환경에서 널리 사용되는 QCOW2 형식의 부팅 가능한 디스크 이미지로 변환합니다. 이 과정에서 최종 OS에 로그인할 사용자 계정 등의 추가 설정도 적용합니다.
- **실행 (Ubuntu VM 내부에서)**:
    1. 사용자 설정 파일 생성 (`config.toml`):
        
        ```bash
        cat > config.toml << 'EOL'
        [[customizations.user]]
        name = "admin"
        password = "bootcpassword"
        groups = ["wheel"]
        EOL
        
        ```
        
    2. `bootc-image-builder` 실행:
    (참고: `-output /output` 옵션은 빌더 컨테이너 내의 `/output` 디렉터리를 의미하며, 이 디렉터리는 호스트 VM의 `./output`에 마운트되어 있습니다. `bootc-image-builder`는 이 디렉터리 내에 특정 구조로 QCOW2 파일을 생성할 수 있습니다. 가이드에서는 이후 `output/qcow2/disk.qcow2` 경로를 사용합니다.)
        
        ```bash
        sudo podman run \\
          --rm \\
          -it \\
          --privileged \\
          --pull=newer \\
          --security-opt label=type:unconfined_t \\
          -v ./config.toml:/config.toml:ro \\
          -v ./output:/output \\
          -v /var/lib/containers/storage:/var/lib/containers/storage \\
          quay.io/centos-bootc/bootc-image-builder:latest \\
          --type qcow2 \\
          --output /output \\
          localhost/my-bootc-webserver
        
        ```
        
- **결과**: Ubuntu VM의 `~/bootc-webserver/output/qcow2/disk.qcow2` (또는 유사한 경로 및 파일명)에 부팅 가능한 QCOW2 디스크 이미지가 생성됩니다.

### **Phase 5: VDI 형식 변환 (qemu-img)**

- **의도**: 생성된 QCOW2 이미지를 VirtualBox의 네이티브 디스크 형식인 VDI로 변환하여 호환성 및 성능을 최적화합니다.
- **실행 (Ubuntu VM 내부에서)**:
    
    ```bash
    qemu-img convert -f qcow2 -O vdi output/qcow2/disk.qcow2 output/bootc-webserver.vdi
    
    ```
    
- **결과**: Ubuntu VM의 `~/bootc-webserver/output/` 디렉터리에 `bootc-webserver.vdi` 파일이 생성됩니다.

### **Phase 6: VDI 파일 호스트 PC 전송 (Vagrant SCP)**

- **의도**: Ubuntu 빌드 VM 내부에 생성된 `bootc-webserver.vdi` 파일을 호스트 PC로 복사하여 VirtualBox에서 사용할 수 있도록 합니다.
- **실행 (호스트 PC에서)**:
    1. `vagrant plugin install vagrant-scp` (최초 1회)
    2. `vagrant scp default:/home/vagrant/bootc-webserver/output/bootc-webserver.vdi ./`
- **결과**: 호스트 PC의 현재 디렉터리에 `bootc-webserver.vdi` 파일이 복사됩니다.

### **Phase 7: VirtualBox에서 VDI 이미지 부팅**

- **의도**: 최종 생성된 `bootc-webserver.vdi` 파일을 사용하여 VirtualBox에서 새로운 가상 머신을 부팅하고, 웹 서버가 정상적으로 작동하는지 확인합니다.
- **실행 (호스트 PC의 VirtualBox에서)**:
    1. 새로운 가상 머신을 생성합니다.
    2. "종류(Type)"는 "Linux", "버전(Version)"은 "Red Hat (64-bit)" 또는 "CentOS (64-bit)" 등으로 선택합니다.
    3. "하드 디스크" 단계에서 "기존 가상 하드 디스크 파일 사용"을 선택하고, 호스트 PC로 복사한 `bootc-webserver.vdi` 파일을 지정합니다.
    4. 가상 머신을 시작합니다.
- **결과**: VirtualBox에서 CentOS Stream 9 기반의 웹 서버가 부팅되며, 호스트 PC의 웹 브라우저에서 `http://localhost:8080` (포트 포워딩 설정에 따라)으로 접속 시 `index.html`에 정의된 "성공!" 페이지가 표시됩니다.

## Question

### Q) vdi 만으로 어떻게 VM이 바로 실행되는걸까?

```json
그런데, vdi자체로는 부팅이 불가능하고, 버추얼박스에서 linux를 선택하고(iso는 선택되지도않음) vdi를 부팅디스크로설정했을때 동작하는데, vdi는 도대체 무엇이고, 버추얼박스에서 iso를선택하지않고 토글에서 linux를 선택하는게 무슨 의미를 가지는거고, 결과적으로 어떻게 이게 동작하는걸까?
```

- **VDI 파일**: 이미 윈도우나 리눅스가 완벽하게 설치되어 있고, 필요한 프로그램까지 다 깔려있는 "만능 하드 디스크"입니다.
- **버추얼박스**: 이 "만능 하드 디스크"를 끼워서 실제 컴퓨터처럼 사용할 수 있게 해주는 특별한 "컴퓨터 본체(케이스 + 메인보드)"입니다.
- **버추얼박스에서 "Linux" 선택**: "컴퓨터 본체"를 만들 때, "이 본체에는 리눅스용 하드 디스크를 끼울 거니까, 리눅스가 잘 돌아가도록 내부 부품(가상 하드웨어)들을 설정해줘!" 라고 요청하는 것과 같습니다.
- **ISO 파일**: 운영체제 설치용 "CD 또는 USB"입니다. 이미 OS가 설치된 "만능 하드 디스크"(VDI)를 사용하므로, 설치용 CD가 필요 없는 것입니다.