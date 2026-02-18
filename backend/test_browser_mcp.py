from browser_mcp import open_app_logic, run_saju_test_logic

if __name__ == "__main__":
    print("🚀 1. 앱 접속 테스트 중...")
    try:
        # 직접 구현 로직 함수 호출
        title = open_app_logic()
        print(f"✅ 앱 접속 성공: {title}")
    except Exception as e:
        print(f"❌ 앱 접속 실패: {e}")

    print("\n🚀 2. 사주 분석 테스트 중...")
    try:
        # 직접 구현 로직 함수 호출
        result = run_saju_test_logic("김철수", "1995-05-05", "14:30", "M", "평생사주")
        print(f"✅ 결과:\n{result}")
    except Exception as e:
        print(f"❌ 사주 분석 테스트 실패: {e}")
