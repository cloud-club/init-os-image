![image](https://github.com/user-attachments/assets/269a06af-d7da-49ac-bb2b-f948cc45f579)

![image](https://github.com/user-attachments/assets/020a3f28-eda1-4817-b228-61906ca2c0a9)



# v1 이미지 : 자빅스 6.4 + 에이전트 1
```
...
# Zabbix 6.4 저장소 추가 및 설치
RUN rpm -Uvh https://repo.zabbix.com/zabbix/6.4/rhel/9/x86_64/zabbix-release-6.4-1.el9.noarch.rpm && \
    dnf -y install zabbix-server-mysql zabbix-web-mysql zabbix-apache-conf zabbix-sql-scripts zabbix-agent
...
```


# v2 이미지 : 자빅스 7.0 + 에이전트 2
```
...
# Zabbix 7.0 저장소 추가
RUN rpm -Uvh https://repo.zabbix.com/zabbix/7.0/rhel/9/x86_64/zabbix-release-7.0-2.el9.noarch.rpm && \
    dnf -y install zabbix-server-mysql zabbix-web-mysql zabbix-apache-conf zabbix-sql-scripts
...
```

# v3 이미지 
```
...
확인중
...
```


# v2, v3 도커 이미지 만들기

[root@bootc-client01 podman]# podman images
REPOSITORY                                TAG         IMAGE ID      CREATED         SIZE
localhost/bootc-zabbix                    v3          27b9e905fc98  9 minutes ago   1.93 GB
localhost/bootc-zabbix                    v2          db8ec123b323  10 minutes ago  1.87 GB
localhost/bootc-zabbix                    v1          9650833269c1  10 minutes ago  1.87 GB
192.168.10.50:5000/my-bootc-os            v1          b1e43207d4ca  8 days ago      1.69 GB
quay.io/centos-bootc/bootc-image-builder  latest      afc293631e4f  10 days ago     784 MB
quay.io/centos-bootc/centos-bootc         stream9     5254d78ea79c  11 days ago     1.64 GB

[root@bootc-client01 podman]# docker save -o bootc-zabbix-v2.tar localhost/bootc-zabbix:v2
Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
Copying blob a75c824d5854 done   |
Copying blob f1c975aab2e5 done   |
Copying blob 4483b8b84a81 done   |
Copying blob 9b409f7ed408 done   |
Copying blob 419461c56f6f done   |
Writing manifest to image destination


[root@bootc-client01 podman]# podman save -o bootc-zabbix-v3.tar localhost/bootc-zabbix:v3
Copying blob a75c824d5854 done   |
Copying blob f1c975aab2e5 done   |
Copying blob 4483b8b84a81 done   |
Copying blob 9b409f7ed408 done   |
Copying blob 419461c56f6f done   |
Copying blob 18563341cc6a done   |
Writing manifest to image destination




# docker hub 컨테이너 이미지 업로드
![image](https://github.com/user-attachments/assets/95928134-a17d-4c26-bef7-a17b5d88699f)



![image](https://github.com/user-attachments/assets/38dbe1c7-9fdd-4447-ae23-a53ff0d0d172)



# 레지스트리 생성
docker run -d -p 5000:5000 --name localregistry registry:2
podman push localhost:5000/bootc-zabbix:v2 --tls-verify=false

# 레지스트리 목록 확인 (클라이언트)
bash-5.1# curl http://10.109.16.153:5000/v2/_catalog
{"repositories":["bootc-zabbix"]}

# 보안 HTTP 허용
vi /etc/containers/registries.conf
[[registry]]
location = "10.109.16.153:5000"
insecure = true



# 클라이언트 switch
bootc switch 10.109.16.153:5000/bootc-zabbix:v2 --apply
이후 알아서 리부팅

# 클라이언트 bootc status
bash-5.1# bootc status
● Booted image: 10.109.16.153:5000/bootc-zabbix:v2
        Digest: sha256:02346eca8b5a5fce9b9b6cf0fa8c40c9f353ecf666b8085d105fcfda0ad7bb8d (amd64)
       Version: 9 (2025-05-27T05:57:28Z)

  Rollback image: localhost/bootc-zabbix:v1
          Digest: sha256:1a1943c652cfff5daa3efa73b3189f83e3cd71d1c10036946d31c5a36c9c06e7 (amd64)
         Version: 9 (2025-05-27T05:06:23Z)

# 신규 버전 확인
bash-5.1# zabbix_server -V
zabbix_server (Zabbix) 7.0.13
Revision 42673dd61ca 20 May 2025, compilation time: May 20 2025 00:00:00

bash-5.1# systemctl status zabbix-agent2
● zabbix-agent2.service - Zabbix Agent 2
     Loaded: loaded (/usr/lib/systemd/system/zabbix-agent2.service; enabled; preset: disabled)
     Active: active (running) since Tue 2025-05-27 06:25:48 UTC; 3min 55s ago
   Main PID: 845 (zabbix_agent2)
      Tasks: 8 (limit: 24005)
     Memory: 20.5M
        CPU: 65ms
     CGroup: /system.slice/zabbix-agent2.service
             └─845 /usr/sbin/zabbix_agent2 -c /etc/zabbix/zabbix_agent2.conf

May 27 06:25:48 localhost.localdomain systemd[1]: Started Zabbix Agent 2.
May 27 06:25:48 localhost.localdomain zabbix_agent2[845]: Starting Zabbix Agent 2 (7.0.13)
May 27 06:25:48 localhost.localdomain zabbix_agent2[845]: Zabbix Agent2 hostname: [Zabbix server]
May 27 06:25:48 localhost.localdomain zabbix_agent2[845]: Press Ctrl+C to exit.


# 롤백 버전 확인
bash-5.1# bootc rollback
Next boot: rollback deployment
bash-5.1# reboot

[root@localhost ~]# bootc status
● Booted image: localhost/bootc-zabbix:v1
        Digest: sha256:1a1943c652cfff5daa3efa73b3189f83e3cd71d1c10036946d31c5a36c9c06e7 (amd64)
       Version: 9 (2025-05-27T05:06:23Z)

  Rollback image: 10.109.16.153:5000/bootc-zabbix:v2
          Digest: sha256:02346eca8b5a5fce9b9b6cf0fa8c40c9f353ecf666b8085d105fcfda0ad7bb8d (amd64)
         Version: 9 (2025-05-27T05:57:28Z)

[root@localhost ~]# zabbix_server -V
zabbix_server (Zabbix) 6.4.21
Revision 58bcc6747a9 27 January 2025, compilation time: Jan 27 2025 00:00:00


# 외부 도커에서 가져오기
curl https://registry.hub.docker.com/v2/repositories/gag2012/bootc-zabbix/tags/
bootc switch docker.io/gag2012/bootc-zabbix:v3 --apply
![alt text](IMAGES/image.png)


bootc status
● Booted image: docker.io/gag2012/bootc-zabbix:v3
        Digest: sha256:c5a4ba0d5209c03ffaf3cbcc1d31d8803856e5f47f868593a9093de1ae9cf5b5 (amd64)
       Version: 9 (2025-05-26T23:09:56Z)

  Rollback image: localhost/bootc-zabbix:v1
          Digest: sha256:1a1943c652cfff5daa3efa73b3189f83e3cd71d1c10036946d31c5a36c9c06e7 (amd64)
         Version: 9 (2025-05-27T05:06:23Z)




# Harbor 설치

(1) Docker Compose 설치

sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 71.2M  100 71.2M    0     0  4184k      0  0:00:17  0:00:17 --:--:-- 4961k
sudo chmod +x /usr/local/bin/docker-compose
docker-compose version
  > Docker Compose version v2.36.2

(2) Harbor 다운로드 및 설치
wget https://github.com/goharbor/harbor/releases/download/v2.10.0/harbor-online-installer-v2.10.0.tgz
tar xvf harbor-online-installer-v2.10.0.tgz 
vi harbor.yml
  > hostname: harbor.bootc.com
  > # https related config (주석)


sudo ./install.sh (반짝반짝 이쁨)
![alt text](IMAGES/image-2.png)


(3) Harbor 홈페이지 접속
ID : admin / PW : Harbor12345
![alt text](IMAGES/image-3.png)


# Harbor에 bootc 이미지 업로드
(1) PODMAN 보안 설정
 vi /etc/containers/registries.conf
[[registry]]
location = "harbor.bootc.com:80"
insecure = true

systemctl restart podman

podman login harbor.bootc.com:80
![alt text](IMAGES/image-4.png)


# Harbor에 올릴 새로운 컨테이너 이미지 생성
(1) Contianer_harbor 작성
```
FROM quay.io/centos-bootc/centos-bootc:stream9

RUN dnf install -y nginx mariadb-server mariadb
RUN systemctl enable nginx mariadb

RUN bootc container lint

LABEL containers.bootc=1
LABEL ostree.bootable=1
```

(2) 생성
podman build -t harbor.bootc.com:80/sales/nginx-mariadb:v1 -f Containerfile_harbor .

(3) 이미지 확인
podman images
REPOSITORY                                TAG         IMAGE ID      CREATED        SIZE
harbor.bootc.com:80/sales/nginx-mariadb   v1          ccf857be1459  7 minutes ago  1.94 GB

(4) Harbor 프로젝트 생성
![alt text](IMAGES/image-6.png)

(5) podman push to harbor sales repo
podman push harbor.bootc.com:80/sales/nginx-mariadb:v1
![alt text](IMAGES/image-5.png)

(6) Harbor > sales 프로젝트 > 정상 업로드 확인
![alt text](IMAGES/image-7.png)

# Client에서 해당 Harbor bootc 레포지토리를 통해 업그레이드
(1) PODMAN 보안 설정
 vi /etc/containers/registries.conf
[[registry]]
location = "harbor.bootc.com:80"
insecure = true

systemctl restart podman

(2) Harbor 로그인
podman login harbor.bootc.com:80

(3) Harbor > 클라이언트 switch 명령어를 실행하면 권한 문제 발생하여 Public으로 변경

[root@localhost ~]# bootc switch harbor.bootc.com:80/sales/nginx-mariadb:v1 --apply
ERROR Switching: Creating importer: failed to invoke method OpenImage: failed to invoke method OpenImage: reading manifest v1 in harbor.bootc.com:80/sales/nginx-mariadb: unauthorized: unauthorized to access repository: sales/nginx-mariadb, action: pull: unauthorized to access repository: sales/nginx-mariadb, action: pull

![alt text](IMAGES/image-8.png)
![alt text](IMAGES/image-9.png)

(4) 프로젝트를 Public으로 변경하니 가능
![alt text](IMAGES/image-10.png)

(5) 스위칭 및 리부팅 이후 bootc status (대략 60초 소요)
아니 근데 생각해보니깐 IP 주소를 바꿔줬었는데 이건 새롭게 반영이 안되어서 엄청 편하네 진짜 뭐지
```
bash-5.1# bootc status
● Booted image: harbor.bootc.com:80/sales/nginx-mariadb:v1
        Digest: sha256:7fb05fb00d1f98373bba7e2dde2270ef33fc84d4098507d0419cf221c4ea2917 (amd64)
       Version: 9 (2025-05-27T08:33:16Z)

  Rollback image: docker.io/gag2012/bootc-zabbix:v3
          Digest: sha256:c5a4ba0d5209c03ffaf3cbcc1d31d8803856e5f47f868593a9093de1ae9cf5b5 (amd64)
         Version: 9 (2025-05-26T23:09:56Z)

bash-5.1#
bash-5.1#
bash-5.1# systemctl status mariadb
× mariadb.service - MariaDB 10.5 database server
     Loaded: loaded (/usr/lib/systemd/system/mariadb.service; enabled; preset: disabled)
     Active: failed (Result: exit-code) since Tue 2025-05-27 08:59:22 UTC; 58s ago
       Docs: man:mariadbd(8)
             https://mariadb.com/kb/en/library/systemd/

bash-5.1#
bash-5.1# systemctl status nginx
× nginx.service - The nginx HTTP and reverse proxy server
     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; preset: disabled)
     Active: failed (Result: exit-code) since Tue 2025-05-27 08:59:22 UTC; 1min 6s ago
        CPU: 19ms
```