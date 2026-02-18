import requests
import json
import sys

# API 엔드포인트 설정
API_URL = "http://localhost:8000/api/saju/analyze"

# 테스트용 사용자 프로필
TEST_USER = {
    "name": "김철수",
    "gender": "male",
    "birth_year": 1990,
    "birth_month": 5,
    "birth_day": 5,
    "birth_hour": 14,
    "calendar_type": "solar",
    "job": "소프트웨어 개발자",
    "mbti": "INTP",
    "blood_type": "A"
}

def verify_category(category, expected_keywords):
    """특정 카테고리의 운세 생성 및 키워드 검증"""
    print(f"\n🚀 Testing Category: {category}...")
    
    payload = {
        "birth_date": f"{TEST_USER['birth_year']}-{TEST_USER['birth_month']:02d}-{TEST_USER['birth_day']:02d}",
        "birth_time": f"{TEST_USER['birth_hour']:02d}:00",
        "gender": TEST_USER["gender"],
        "name_korean": TEST_USER["name"],
        "job": TEST_USER["job"],
        "mbti": TEST_USER["mbti"],
        "blood_type": TEST_USER["blood_type"],
        "category": category
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        fortune_text = result.get("result", "")
        if not fortune_text:
            print(f"❌ Failed: No fortune text generated for {category}")
            return False
            
        print(f"   - Generated {len(fortune_text)} characters.")
        
        missing = []
        for keyword in expected_keywords:
            if keyword not in fortune_text:
                missing.append(keyword)
        
        if missing:
            print(f"❌ Failed: Missing keywords in {category}: {missing}")
            return False
            
        print(f"✅ Pass: All {len(expected_keywords)} expected keywords found.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("========================================")
    print("🔍 Saju App Upgrade Verification")
    print("========================================")
    
    # 1. 재물운 검증 (심층 재물 전략)
    wealth_keywords = [
        "심층 재물운 & 자산 포트폴리오 전략",
        "타고난 '부(富)의 그릇' 진단",
        "오행 기반 맞춤 투자 포트폴리오",
        "'돈이 새는 구멍' 막는 솔루션"
    ]
    wealth_pass = verify_category("재물운", wealth_keywords)
    
    # 2. 직업운 검증 (커리어 로드맵)
    career_keywords = [
        "커리어 로드맵 & 조직 적합도 분석",
        "나에게 맞는 '조직의 형태'",
        "사주로 본 '천직(天職)' 키워드",
        "슬럼프 극복 & 번아웃 예방"
    ]
    career_pass = verify_category("직업운", career_keywords)
    
    # 3. 애정운 검증 (관계 역동성)
    love_keywords = [
        "관계 역동성(Dynamics) & 솔루션",
        "나의 관계 맺기 스타일",
        "갈등 패턴 시뮬레이션",
        "운명의 짝(Ideal Match)"
    ]
    love_pass = verify_category("애정운", love_keywords)
    
    print("\n========================================")
    if wealth_pass and career_pass and love_pass:
        print("🎉 ALL UPGRADE TESTS PASSED!")
        sys.exit(0)
    else:
        print("💥 SOME TESTS FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
