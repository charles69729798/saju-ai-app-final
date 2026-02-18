import requests
import json
import time

API_URL = "http://localhost:8000/api/saju/analyze"

def verify_strict_validation():
    print("========================================")
    print("🛡️ Strict Validation & Dynamic Footer Test")
    print("========================================")
    
    # 1. 필수 데이터 누락 테스트 (400 에러 기대)
    print("\n[Test 1] Missing Required Data...")
    
    # MBTI분석에 MBTI 없음
    payload_no_mbti = {
        "birth_date": "1990-01-01", "birth_time": "12:00", "gender": "male", "name_korean": "테스트",
        "category": "MBTI분석", "mbti": "" 
    }
    resp1 = requests.post(API_URL, json=payload_no_mbti)
    if resp1.status_code == 400:
        print("✅ MBTI Missing Check: Passed (400 Bad Request)")
    else:
        print(f"❌ MBTI Missing Check: Failed ({resp1.status_code})")

    # 혈액형분석에 혈액형 없음
    payload_no_blood = {
        "birth_date": "1990-01-01", "birth_time": "12:00", "gender": "male", "name_korean": "테스트",
        "category": "혈액형분석", "blood_type": "" 
    }
    resp2 = requests.post(API_URL, json=payload_no_blood)
    if resp2.status_code == 400:
        print("✅ Blood Type Missing Check: Passed (400 Bad Request)")
    else:
        print(f"❌ Blood Type Missing Check: Failed ({resp2.status_code})")
        
    # 2. 동적 푸터 테스트
    print("\n[Test 2] Dynamic Footer Content...")
    
    # Case A: 둘 다 없음 -> 기본 푸터
    payload_none = {
        "birth_date": "1990-01-01", "birth_time": "12:00", "gender": "male", "name_korean": "기본",
        "category": "신년운세", "mbti": "", "blood_type": ""
    }
    resp_none = requests.post(API_URL, json=payload_none)
    result_none = resp_none.json().get("result", "")
    
    if "사주를 바탕으로" in result_none and "현대적 MBTI" not in result_none:
        print("✅ Footer (None): Passed")
    else:
        print(f"❌ Footer (None): Failed\nSample: {result_none[-200:]}")

    # Case B: MBTI만 있음 -> MBTI 포함 푸터
    payload_mbti = {
        "birth_date": "1990-01-01", "birth_time": "12:00", "gender": "male", "name_korean": "엠비티아이",
        "category": "신년운세", "mbti": "INTJ", "blood_type": ""
    }
    resp_mbti = requests.post(API_URL, json=payload_mbti)
    result_mbti = resp_mbti.json().get("result", "")
    
    if "현대적 MBTI" in result_mbti and "혈액형" not in result_mbti:
        print("✅ Footer (MBTI Only): Passed")
    else:
        print(f"❌ Footer (MBTI Only): Failed\nSample: {result_mbti[-200:]}")
        
    # Case C: 둘 다 있음 -> 전체 푸터
    payload_all = {
        "birth_date": "1990-01-01", "birth_time": "12:00", "gender": "male", "name_korean": "전체",
        "category": "신년운세", "mbti": "INTJ", "blood_type": "A"
    }
    resp_all = requests.post(API_URL, json=payload_all)
    result_all = resp_all.json().get("result", "")
    
    if "현대적 MBTI/혈액형" in result_all or "혈액형/현대적 MBTI" in result_all:
        print("✅ Footer (All Info): Passed")
    else:
        print(f"❌ Footer (All Info): Failed\nSample: {result_all[-200:]}")

if __name__ == "__main__":
    verify_strict_validation()
