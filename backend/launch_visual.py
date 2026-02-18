from playwright.sync_api import sync_playwright
import time

def launch_app_visual():
    print("🚀 앱 화면을 띄웁니다...")
    try:
        with sync_playwright() as p:
            # Headless=False로 설정하여 브라우저 창이 보이게 함
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={'width': 450, 'height': 800}, # 모바일 뷰포트 느낌
                locale='ko-KR'
            )
            page = context.new_page()
            
            print("🌐 http://localhost:8000 접속 중...")
            page.goto("http://localhost:8000")
            
            print("✅ 앱이 실행되었습니다. 창을 닫지 않고 대기합니다.")
            print("(종료하려면 터미널에서 Ctrl+C를 누르세요)")
            
            # 사용자가 볼 수 있도록 무한 대기 (실제로는 타임아웃 등으로 종료될 수 있음)
            while True:
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\n🛑 종료합니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    launch_app_visual()
