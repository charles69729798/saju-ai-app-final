@echo off

:: 1. ADB 설치 확인
adb version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] ADB가 설치되지 않았거나 PATH에 없습니다.
    echo Android Studio 설치 후 C:\Users\YourUser\AppData\Local\Android\Sdk\platform-tools 경로를 PATH에 추가해주세요.
    exit /b 1
)
echo [OK] ADB 설치됨

:: 2. 에뮬레이터 연결 확인
adb devices | findstr "emulator" >nul
if %errorlevel% neq 0 (
    echo [ERROR] 연결된 에뮬레이터가 없습니다. Android Studio에서 에뮬레이터를 실행해주세요.
    exit /b 1
)
echo [OK] 에뮬레이터 연결됨

:: 3. 10.0.2.2 연결 테스트 (Curl 대신 핑/브라우저 실행)
echo [TEST] 에뮬레이터 브라우저에서 Flask 서버(10.0.2.2:8000) 접속 시도...
:: 안드로이드 기본 브라우저 실행
adb shell am start -a android.intent.action.VIEW -d http://10.0.2.2:8000
echo [INFO] 에뮬레이터 화면을 확인해주세요. 사주 앱 웹페이지가 뜨면 성공입니다!

:: 핑 테스트 (옵션)
echo [TEST] Ping 10.0.2.2...
adb shell ping -c 3 10.0.2.2
