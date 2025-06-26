### 준비 과정
---
```
처음에는 bootc 메인 서버가 있으면 하위 클라이언트에 bootc를 설치하여 에이전트 방식으로 운영체제를 포함한 데이터를 관리하는 줄 알았다.

그래서 bootc 메인 서버에서 podman으로 CentOS bootc 이미지를 만들고 레지스트리로 push했다.
그리고 클라이언트에서 bootc pull하거나 upgrade하면 자동으로 내가 원하는 컨테이너 파일 설정으로 부팅이 된다고 생각했다.
( 잘못 접근했으며 전용 bootc iso로 최초 설치해야하는 것으로 이해함 )

그러나 bootc upgrade 를 입력했을 때 아래와 같은 오류가 발생했다.
( 해당 오류는 클라이언트 시스템이 ostree 기반으로 부팅되지 않아서 발생한 오류이다. ostree는 GIT처럼 버전을 관리한다고 하는데 검색 좀 해봐야겠다. )

[root@bootc-client01 ~]# bootc upgrade
ERROR Upgrading: Initializing storage: Acquiring sysroot: Preparing for write: This command requires an ostree-booted host system

어쨌든 그래서 처음부터 시작
```

### 환경 구성
---
![image](https://github.com/user-attachments/assets/d3f639b8-cc9b-4a56-8f85-e96484351ce3)



### bootc 설치를 위한 순서 정리
---
```
(1) ESXi 위에 CentOS 가상머신을 설치
(2) CentOS 환경에서 podman과 bootc-image-builder를 설치
(3) containerfile을 작성해 원하는 원하는 환경 작성
(4) podman을 이용해 containerfile로부터 bootc 이미지를 빌드
(5) bootc-image-builder를 사용해 빌드한 이미지를 boot.iso로 변환
(6) 생성된 boot.iso 파일을 이용해 새로운 VM 배포
```

## 아래 과정은 bootc를 이용한 클라이언트 배포 과정과 결과를 포함함  

### Containerfile 생성
---
\# vi ~/Containerfile
> \> centos 9 stream 운영체제 선택   
FROM quay.io/centos-bootc/centos-bootc:stream9<br><br>
> \> zabbix 6.4 패키지 설치<br>
RUN rpm -Uvh https://repo.zabbix.com/zabbix/6.4/rhel/9/x86_64/zabbix-release-6.4-1.el9.noarch.rpm && \\<br>
dnf -y install zabbix-server-mysql zabbix-web-mysql zabbix-apache-conf zabbix-sql-scripts zabbix-agent<br><br>
> \> SSH 설정 변경 (루트 로그인 허용)<br>
RUN sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config<br><br>
> \> 네트워크 설정 (고정 IP)<br>
RUN echo -e "TYPE=Ethernet\nPROXY_METHOD=none\nBROWSER_ONLY=no\nBOOTPROTO=none\nIPADDR=192.168.10.55\nNETMASK=255.255.255.0\nGATEWAY=192.168.10.254\nDNS1=8.8.8.8" > /etc/sysconfig/network-scripts/ifcfg-eth0<br><br>
> \> 서비스 활성화<br>
RUN systemctl enable sshd zabbix-server zabbix-agent httpd<br><br>
> \>bootc 이미지 검증<br>
RUN bootc container lint

###  컨테이너 실행 (생략함)
---
\# podman build --no-cache -t localhost:5000/bootc-zabbix-os:v1 .
```
STEP 1/6: FROM quay.io/centos-bootc/centos-bootc:stream9
STEP 2/6: RUN rpm -Uvh https://repo.zabbix.com/zabbix/6.4/rhel/9/x86_64/zabbix-release-6.4-1.el9.noarch.rpm && dnf -y install zabbix-server-mysql zabbix-web-mysql zabbix-apache-conf zabbix-sql-scripts zabbix-agent && dnf clean all
warning: /var/tmp/rpm-tmp.BO07nO: Header V4 RSA/SHA512 Signature, key ID 08efa7dd: NOKEY
Retrieving https://repo.zabbix.com/zabbix/6.4/rhel/9/x86_64/zabbix-release-6.4-1.el9.noarch.rpm
Verifying... ########################################
Preparing... ########################################
Updating / installing...
zabbix-release-6.4-1.el9 ########################################
Updating Subscription Management repositories.
Unable to read consumer identity
This system is not registered with an entitlement server. You can use subscription-manager to register.
CentOS Stream 9 - BaseOS 1.3 MB/s | 8.7 MB 00:06
CentOS Stream 9 - AppStream 2.0 MB/s | 23 MB 00:11
CentOS Stream 9 - Extras packages 16 kB/s | 19 kB 00:01
Zabbix Official Repository - x86_64 151 kB/s | 340 kB 00:02
Zabbix Official Repository non-supported - x86_ 678 B/s | 1.1 kB 00:01
Dependencies resolved.
================================================================================
 Package Arch Version Repository Size
================================================================================
Installing:
 zabbix-agent x86_64 6.4.21-release1.el9 zabbix 566 k
 zabbix-apache-conf noarch 6.4.21-release1.el9 zabbix 12 k
 zabbix-server-mysql x86_64 6.4.21-release1.el9 zabbix 2.0 M
 zabbix-sql-scripts noarch 6.4.21-release1.el9 zabbix 8.0 M
 zabbix-web-mysql noarch 6.4.21-release1.el9 zabbix 11 k

>Complete!
Updating Subscription Management repositories.
Unable to read consumer identity

This system is not registered with an entitlement server. You can use subscription-manager to register.

31 files removed
--> 06ddd1146745
STEP 3/6: RUN sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
--> 07f668cc6c58
STEP 4/6: RUN echo -e "TYPE=Ethernet\nPROXY_METHOD=none\nBROWSER_ONLY=no\nBOOTPROTO=none\nIPADDR=192.168.10.55\nNETMASK=255.255.255.0\nGATEWAY=192.168.10.254\nDNS1=8.8.8.8" > /etc/sysconfig/network-scripts/ifcfg-eth0
--> d36eb91d5c6c
STEP 5/6: RUN systemctl enable sshd zabbix-server zabbix-agent httpd
Created symlink /etc/systemd/system/multi-user.target.wants/zabbix-server.service → /usr/lib/systemd/system/zabbix-server.service.
Created symlink /etc/systemd/system/multi-user.target.wants/zabbix-agent.service → /usr/lib/systemd/system/zabbix-agent.service.
Created symlink /etc/systemd/system/multi-user.target.wants/httpd.service → /usr/lib/systemd/system/httpd.service.
--> 8bf0c2c92cfa
STEP 6/6: RUN bootc container lint
Lint warning: sysusers: Found /etc/passwd entry without corresponding systemd sysusers.d:
  zabbix
Found /etc/group entry without corresponding systemd sysusers.d:
  zabbix

Lint warning: var-log: Found non-empty logfile: /var/log/dnf.librepo.log (and 4 more)
Lint warning: var-tmpfiles: Found content in /var missing systemd tmpfiles.d entries:
  d /var/cache/dnf/appstream-831abc7e9d6a1a72 0755 root root - -
  d /var/cache/dnf/appstream-831abc7e9d6a1a72/packages 0755 root root - -
  d /var/cache/dnf/appstream-831abc7e9d6a1a72/repodata 0755 root root - -
  d /var/cache/dnf/baseos-044cae74d71fe9ea 0755 root root - -
  d /var/cache/dnf/baseos-044cae74d71fe9ea/packages 0755 root root - -
  ...and 33 more
Found non-directory/non-symlink files in /var:
  var/lib/dnf/history.sqlite
  var/lib/dnf/history.sqlite-shm
  var/lib/dnf/history.sqlite-wal
  var/lib/dnf/repos/appstream-831abc7e9d6a1a72/countme
  var/lib/dnf/repos/baseos-044cae74d71fe9ea/countme
  ...and 12 more

Checks passed: 9
Checks skipped: 1
Warnings: 3
COMMIT localhost:5000/bootc-zabbix-os:v1
--> bdc1a2dea870
Successfully tagged localhost:5000/bootc-zabbix-os:v1
bdc1a2dea8707bb676be9e8a940e95a721afd1d1f01b40f71f9e21d15cb3fd89
```




### 비밀번호 설정 파일 생성
---
\# vi config.toml
```
------------------------
[[customizations.user]]
name = "root"
password = "V7d^L3q$R9@KtP5!mF8*"
groups = ["wheel"]

[[customizations.user]]
name = "admin"
password = "X2y&8z#Q!pL9wE$rT6%"
groups = ["wheel"]
```


### bootc ISO 추출
---

\> 출력 디렉토리 생성  
\# sudo mkdir -p ./output

\> ISO 빌드  
\# sudo podman run --rm -it --privileged \\  
  --security-opt label=type:unconfined_t \\  
  -v \$(pwd)/output:/output \\  
  -v /var/lib/containers/storage:/var/lib/containers/storage \\  
  -v \$(pwd)/config.toml:/config.toml:ro \\    
  quay.io/centos-bootc/bootc-image-builder:latest \\    
  --type iso \\  
  --config /config.toml \\  
  --local \\  
  localhost:5000/bootc-zabbix-os:v1


```
WARNING: --local is now the default behavior, you can remove it from the command line
[-] Image building step
[9 / 9] Pipeline bootiso [----------------------------------------------------------------------------------------------------------------------------------------------------------------------->] 100.00%
[3 / 3] Stage org.osbuild.implantisomd5 [-------------------------------------------------------------------------------------------------------------------------------------------------------->] 100.00%
Message: Results saved in .
```

### ISO 업로드 (ESXi라는 가상화 호스트의 데이터스토어)
![image](https://github.com/user-attachments/assets/0a712677-0a6e-45e5-880b-b66af28d1f83)



### 설치 확인
---
![image](https://github.com/user-attachments/assets/009740d2-6972-423e-b107-71385d565cd3)

### 클라이언트 측 bootc 상태
---
![image](https://github.com/user-attachments/assets/9b6f20e0-fb13-4ac7-b6d5-e5670c5d5ab8)

```
여기서 좀 막혔다. bootc 본 서버는 192.168.10.50:5000 로 서비스 LISTEN 상태이긴한데레지스트리에 접근하는데 보안 관련 문제가 발생한다.
서버가 HTTP를 사용하고, 클라이언트가 HTTPS를 사용해서 그렇다고 한다.
어디에 기준을 둬야할까? 너무 많이하면 재미없으니 여기까쥐
```

### 2주차를 마치며
---
```
(1) 깃허브 어렵다

(2) bootc로 iso 부팅 과정에서 root 및 user 계정 정보를 설정하지 않고 바로 넘어가는 이유는 뭘까?
    아무래도 자동화(간편)에 초점이 맞춰져서 그런 듯 하다.
    그래서 config.toml 파일에 평문 형태로 암호를 저장하는데 적절한 방법일까? 보안담당자한테 걸리면 혼날 것 같다.

(3) bootc를 실제 현업에 적용하려면 어떠한 고민을 해야할까?

(4) 주요 경로는 수정이 안된다고 하는데 유저 생성/삭제이나 패키지 설치는 되는 것 같다. 기준이 무엇일까?!
```

### bootc를 현업에 도입하려면?
---
```
고려 사항이 꽤나 생각난다.

[데이터]
- /var 하위 경로에 대한 로그 데이터는 유지 가능해보인다.

- 근데 만약 JEUS(WAS) 서버를 사용하여 /home/jeus6/data/log 과 같이 default로 쌓이는 로그 파일은 어떻게 설정할까? 이를 /var에 저장할 수 있도록 협의를 해야할까?

- 그리고 /home/jeus6/data/config 파일을 내가 아닌 다른 담당자가 변경한 후 나에게 공유를 안해줬다고 치자. 그럼 Containerfile 반영을 하지 않았을 떄 이슈가 생길 수 있을 것 같다.

[데이터 : 서버분리]
- 아니면 데이터 전용 서버를 분리해서 bootc WAS 서버에는 데이터를 저장하지 않고 이를 타서버의 경로를 이용하는 건 어떨까? ( A WAS 서버 > nfs mount > B DB 서버 )

- 그럼 bootc로 A 서버를 재부팅해도 B 데이터는 영향이 없을 것 같다.

- 환경을 구성하려면 구성과 컨테이너파일을 세밀히 만들고 이력 관리할 수 있는 프로세스를 고민해봐야겠따....

```
