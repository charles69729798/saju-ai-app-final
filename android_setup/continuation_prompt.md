# SajuApp Android 전환 작업 이어하기 프롬프트

## 1. 현재 상황 요약
- **웹 앱 (Frontend/Backend)**: `http://localhost:8000`에서 '분석 시작하기' 버튼 제거 및 모든 기능(주소록, 스타검색, 분석) 정상 작동 확인 완료.
- **안드로이드 환경**: 
  - Android Studio 설치 완료.
  - 에뮬레이터(Pixel 9) 실행 중.
  - ADB 연결 및 네트워크(`http://10.0.2.2:8000`) 접속 테스트 성공.
- **남은 작업**: Android Studio에서 `SajuApp` 프로젝트 생성 후, WebView 코드를 적용하여 앱 빌드.

## 2. 새 세션용 프롬프트 (복사해서 사용하세요)
```text
사주 앱의 안드로이드 앱 전환 작업을 이어서 진행하겠습니다.

[현재 상태]
1. Python Flask 서버가 `c:\InsuranceProject\NotebookLM\saju-app`에서 8000번 포트로 실행 중입니다.
2. Android Studio가 설치되었고, 에뮬레이터가 실행되어 ADB 연결이 확인된 상태입니다.
3. 에뮬레이터 브라우저에서 `http://10.0.2.2:8000` 접속이 성공했습니다.

[오류 해결 및 목표]
현재 Android Studio에서 'SajuApp' 프로젝트를 생성하는 단계 직전입니다.
제가 Android Studio에서 'Empty Views Activity'로 프로젝트(패키지명: com.example.sajuapp)를 생성했다고 가정하고,
다음 파일들을 프로젝트 경로(`C:\Users\pc1\AndroidStudioProjects\SajuApp`)에 자동으로 덮어씌워 안드로이드 앱이 웹뷰로 동작하도록 만들어주세요:
1. `AndroidManifest.xml` (인터넷 권한 추가)
2. `MainActivity.kt` (WebView 로드 코드)
3. `activity_main.xml` (WebView 레이아웃)

이후 `adb`를 이용해 앱이 정상적으로 빌드되고 실행되는지 확인해주세요.
```
