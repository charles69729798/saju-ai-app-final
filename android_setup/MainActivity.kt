package com.example.sajuapp

import android.annotation.SuppressLint
import android.os.Bundle
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        webView = findViewById(R.id.webView)
        
        // 1. 웹뷰 설정: 자바스크립트 허용
        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            cacheMode = WebSettings.LOAD_DEFAULT
        }

        // 2. 외부 브라우저 실행 방지 (앱 내에서 웹페이지 열기)
        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView, url: String): Boolean {
                view.loadUrl(url)
                return true
            }
        }

        // 3. 에뮬레이터에서 로컬 호스트(Flask: 8000) 접속을 위해 10.0.2.2 사용
        // 실제 배포 시에는 'http://your-domain.com'으로 변경하세요.
        val targetUrl = "http://10.0.2.2:8000/" 
        webView.loadUrl(targetUrl)
    }

    // [중요] 뒤로 가기 버튼 처리: 웹뷰 히스토리 뒤로 가기
    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}
