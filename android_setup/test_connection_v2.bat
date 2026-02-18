@echo off
set ADB_PATH="C:\Users\pc1\AppData\Local\Android\Sdk\platform-tools\adb.exe"

echo [1/3] ADB 연결 확인 중...
%ADB_PATH% devices
if %errorlevel% neq 0 (
    echo [ERROR] ADB 실행 실패
    exit /b 1
)

echo.
echo [2/3] 에뮬레이터 상태 확인...
%ADB_PATH% -s emulator-5554 wait-for-device shell getprop init.svc.bootanim
echo [OK] 에뮬레이터 연결됨

echo.
echo [3/3] 네트워크 테스트 (http://10.0.2.2:8000 접속)...
echo 에뮬레이터의 브라우저를 실행하여 사주 앱을 엽니다.
%ADB_PATH% shell am start -a android.intent.action.VIEW -d http://10.0.2.2:8000
echo.
echo [완료] 에뮬레이터 화면에서 사주 앱이 뜨는지 확인해주세요!
pause
