# 안드로이드 앱(APK) 만들기 가이드

에뮬레이터에서 웹 페이지가 잘 뜨는 것을 확인했으므로, 이제 "진짜 앱"을 만들 차례입니다.

## 1. 새 프로젝트 생성
1. **Android Studio**를 실행합니다.
2. **New Project** 버튼을 클릭합니다.
3. **Templates** 목록에서 **[Empty Views Activity]**를 선택하고 **Next**를 누릅니다. (가장 기본 화면)
4. 프로젝트 설정:
   - **Name**: `SajuApp`
   - **Package name**: `com.example.sajuapp` (중요: 제 코드와 일치해야 합니다)
   - **Save location**: 원하는 곳 (기본값)
   - **Language**: `Kotlin`
   - **Minimum SDK**: `API 24` (Android 7.0) 이상 권장
5. **Finish**를 누르고 프로젝트가 열릴 때까지 기다립니다.

## 2. 권한 설정 (AndroidManifest.xml)
1. 좌측 탐색기에서 **app > manifests > AndroidManifest.xml** 파일을 더블 클릭합니다.
2. 파일 내용을 모두 지우고, 제가 만들어둔 `android_setup/AndroidManifest.xml` 파일의 내용을 그대로 복사해 붙여넣습니다.
   - **핵심**: `<uses-permission ... INTERNET />`과 `usesCleartextTraffic="true"`가 포함되어 인터넷 접속이 가능해집니다.

## 3. 메인 화면 코드 (MainActivity.kt)
1. 좌측 탐색기에서 **app > java > com.example.sajuapp > MainActivity** 파일을 더블 클릭합니다.
2. 파일 내용을 모두 지우고, 제가 만들어둔 `android_setup/MainActivity.kt` 파일의 내용을 그대로 복사해 붙여넣습니다.
   - **핵심**: `webView.loadUrl("http://10.0.2.2:8000/")` 코드가 포함되어 로컬 서버를 앱 화면에 띄워줍니다.

## 4. 레이아웃 설정 (activity_main.xml)
1. 좌측 탐색기에서 **app > res > layout > activity_main.xml** 파일을 엽니다.
2. 우측 상단의 **Code** 버튼을 눌러 코드 모드로 전환합니다.
3. 내용을 모두 지우고 아래 코드를 붙여넣습니다:
```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <WebView
        android:id="@+id/webView"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
```

## 5. 앱 실행
1. 상단 툴바의 **▶ (Run)** 버튼을 누릅니다.
2. 아까 띄워둔 에뮬레이터에서 "SajuApp"이라는 이름의 **진짜 앱**이 설치되고 실행됩니다!
