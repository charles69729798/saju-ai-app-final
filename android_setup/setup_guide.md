# Android 개발 환경 구축 가이드

현재 시스템에서 `adb` 및 Android SDK가 감지되지 않았습니다. 아래 단계를 따라 설치를 진행해주세요.

## 1. Android Studio 설치 (필수)
가상 디바이스(에뮬레이터)와 SDK 도구를 한 번에 설치하려면 **Android Studio**가 필요합니다.
- [다운로드 링크](https://developer.android.com/studio)에서 최신 버전을 받아 설치하세요.
- 설치 시 **"Android Virtual Device"** 옵션을 반드시 체크하세요.

## 2. 환경 변수(PATH) 설정
설치가 완료되면 `adb` 명령어를 어디서든 실행할 수 있도록 환경 변수를 추가해야 합니다.

### Windows 설정 방법
1. `Win + S` 누르고 **"시스템 환경 변수 편집"** 검색 후 실행
2. **[환경 변수]** 버튼 클릭
3. **사용자 변수**의 `Path` 선택 후 **[편집]** 클릭
4. **[새로 만들기]**를 눌러 아래 두 경로를 추가합니다:
   - `%LOCALAPPDATA%\Android\Sdk\platform-tools`
   - `%LOCALAPPDATA%\Android\Sdk\emulator`
5. **[확인]**을 눌러 모두 닫은 뒤, 실행 중인 터미널(VS Code 등)을 재시작하세요.

## 3. 에뮬레이터 생성 및 서버 연결
1. Android Studio 실행 -> **More Actions** -> **Virtual Device Manager**
2. **Create Device** -> 원하는 기종(Pixel 등) 선택 -> **Next** -> 시스템 이미지 다운로드(R, S 등 최신) -> **Finish**
3. 생성된 에뮬레이터의 `▶` 버튼을 눌러 실행합니다.
4. `test_connection.bat` 파일을 실행하여 연결 상태를 테스트하세요.

## 4. 앱 실행 (WebView)
`android_setup` 폴더에 생성된 `MainActivity.kt`와 `AndroidManifest.xml` 코드를 사용하여 새 Android 프로젝트를 생성하고 앱을 빌드해보세요.
- **주요 변경점**: `http://localhost:8000` 대신 `http://10.0.2.2:8000`을 사용하여 로컬 서버에 접속합니다.
