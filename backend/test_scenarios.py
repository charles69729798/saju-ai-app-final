from browser_mcp import run_saju_test_logic

def run_tests():
    # 1. 시나리오 A: 기본 운세 (홍길동)
    categories = ["평생사주", "재물운", "직업운", "건강운"]
    for cat in categories:
        print(f"\n🚀 [Scenario A] {cat} 테스트 중...")
        try:
            res = run_saju_test_logic(
                name="홍길동", birth_date="1990-01-01", gender="M", category=cat
            )
            print(f"✅ {cat}: 성공")
        except Exception as e:
            print(f"❌ {cat}: 실패 ({e})")

    # 2. 시나리오 B: MBTI 결합 (김철수, ENFP)
    print("\n🚀 [Scenario B] MBTI 분석 테스트 중...")
    try:
        res = run_saju_test_logic(
            name="김철수", birth_date="1995-05-05", gender="M", 
            category="MBTI분석", mbti="ENFP"
        )
        if "ENFP" in res or "MBTI" in res:
             print("✅ MBTI 분석: 성공 (키워드 발견)")
        else:
             print("⚠️ MBTI 분석: 완료되었으나 키워드 확인 필요")
    except Exception as e:
        print(f"❌ MBTI 분석: 실패 ({e})")

    # 3. 시나리오 C: 궁합 (이영희 & 박지성)
    print("\n🚀 [Scenario C] 궁합 분석 테스트 중...")
    try:
        res = run_saju_test_logic(
            name="이영희", birth_date="1992-12-25", gender="F",
            category="궁합", 
            target_name="박지성", target_birth_date="1992-07-07", target_gender="M"
        )
        print(f"DEBUG RESULT:\n{res}") # 디버깅용 전체 출력
        if "박지성" in res:
            print("✅ 궁합 분석: 성공 (상대방 이름 발견)")
        else:
            print("⚠️ 궁합 분석: 완료되었으나 상대방 이름 미확인")
    except Exception as e:
        print(f"❌ 궁합 분석: 실패 ({e})")

if __name__ == "__main__":
    run_tests()
