# Github Actions 도입하기

## 1. Self hosted runner 등록하기

os 이미지 빌드의 무거움을 해소하기 위해 self hosted runner 사용

```bash
# Create a folder
$ mkdir actions-runner && cd actions-runnerCopied!# Download the latest runner package
$ curl -o actions-runner-linux-x64-2.325.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.325.0/actions-runner-linux-x64-2.325.0.tar.gzCopied!# Optional: Validate the hash
$ echo "5020da7139d85c776059f351e0de8fdec753affc9c558e892472d43ebeb518f4  actions-runner-linux-x64-2.325.0.tar.gz" | shasum -a 256 -cCopied!# Extract the installer
$ tar xzf ./actions-runner-linux-x64-2.325.0.tar.gz

# Create the runner and start the configuration experience
$ ./config.sh --url https://github.com/yucori/bootc-practice --token {MY_TOKEN}# Last step, run it!
$ ./run.sh

# Use this YAML in your workflow file for each job
runs-on: self-hosted
```

- runner 등록 과정에서 Must not run with sudo 문제 발생
  ⇒ `export RUNNER_ALLOW_RUNASROOT="1"` 으로 문제 해결
  - 원래 runner는 root 사용이 비권장되지만, bootc를 통해 os 이미지를 관리하기 위해서 root로 runner 실행하도록 함

## 2. workflow 작성

```yaml
name : Build & Push

on:
  push:
      branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: self-hosted
    steps:
    - uses: actions/checkout@v4
    - name: Install Podman
      run: sudo apt install -y podman

    - name: Build an image
      run: podman build -t bootc:latest /root

    - name: Login Registry
      run: podman login -u ${{ secrets.REGISTRY_USER }} -p ${{ secrets.REGISTRY_PW }} docker.io

    - name: Push an Image
      run: podman push bootc:latest docker.io/${{ secrets.REGISTRY_USER }}/bootc:latest

```

- workflow 작성 후 secrets 변수들 등록
- runner를 run.sh로 단순 실행했다가 터미널이 종료되면 runner가 listen을 못하기에 nohup을 통해 백그라운드로 실행
  - `nohup ./run.sh & > nohup.out`

![스크린샷 2025-06-24 오후 11.33.39.png](attachment:1eb8aeec-b79f-4272-b405-18f1bae64301:스크린샷_2025-06-24_오후_11.33.39.png)

빌드 후 도커 허브에 업로드까지 완료!

이 김에 push 시에 디코로 알림이 오도록 설정

디코에 채널 만들고 webhook 링크를 깃헙에 등록

```yaml
name : Build & Push

on:
  push:
      branches: [main]
  workflow_dispatch:

jobs:
  notify_discord:
    runs-on: self-hosted

    steps:
    - name: Checkout Repository
      uses: actions/checkout@v4

    - name: Notify Discord
      uses: rjstone/discord-webhook-notify@v1
      with:
          severity: info
          details: "${{ github.actor }} added new push\n📜 ${{ github.event.head_commit.message }}"
          webhookUrl: ${{ secrets.DISCORD_WEBHOOK }}
  
  build:
    runs-on: self-hosted
    needs: notify_discord

    steps:    
    - name: Install Podman
      run: sudo apt install -y podman

    - id: build-phase
      name: Build an image
      run: podman build -t bootc:latest /root

    - name: Login Registry
      run: podman login -u ${{ secrets.REGISTRY_USER }} -p ${{ secrets.REGISTRY_PW }} docker.io

    - name: Push an Image
      run: podman push bootc:latest docker.io/${{ secrets.REGISTRY_USER }}/bootc:latest

    - name: 'Notify Discord - Success'
      if: steps.build-phase.outcome == 'success'
      uses: rjstone/discord-webhook-notify@v1
      with:
          severity: info
          details: 'Build - Success'
          webhookUrl: ${{secrets.DISCORD_WEBHOOK }}

    - name: 'Notify Discord - Fail'
      if: steps.build-phase.outcome != 'success'
      uses: rjstone/discord-webhook-notify@v1
      with:
          severity: error
          details: 'Build - Fail'
          webhookUrl: ${{ secrets.DISCORD_WEBHOOK }}

```

![스크린샷 2025-07-02 145655.png](attachment:7b9f71ef-7971-4016-956c-d99b9d06c6c9:스크린샷_2025-07-02_145655.png)

성공~ 굳굳티비~
