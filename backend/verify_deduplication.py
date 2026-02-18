import requests
import json

API_URL = "http://localhost:8000/api/saju/analyze"

def get_fortune(category):
    data = {
        "birth_date": "1990-05-15",
        "birth_time": "14:00",
        "gender": "male",
        "name_korean": "홍길동",
        "job": "개발자",
        "mbti": "INTJ",
        "blood_type": "A",
        "category": category
    }
    resp = requests.post(API_URL, json=data)
    return resp.json().get('result', '')

def calculate_overlap(text1, text2):
    """간단한 라인 기반 중복도 계산"""
    lines1 = set(text1.split('\n'))
    lines2 = set(text2.split('\n'))
    common = lines1.intersection(lines2)
    overlap_ratio = len(common) / min(len(lines1), len(lines2)) * 100
    return overlap_ratio, common

def run_distinction_test():
    print("\n" + "="*80)
    print("🚀 운세 콘텐츠 중복 제거 및 차별화 검증")
    print("="*80)

    # 1. 평생사주 (Full) vs 재물운 (Compact)
    print("\n[테스트 1] 평생사주 vs 재물운 비교")
    lifetime = get_fortune("평생사주")
    wealth = get_fortune("재물운")
    
    overlap, common = calculate_overlap(lifetime, wealth)
    print(f"  - 중복률: {overlap:.2f}% (목표: 40% 이하)")
    
    # 2. 핵심 섹션 위치 확인
    print("\n[테스트 2] 핵심 섹션 배치 순서 확인")
    lines = wealth.split('\n')
    wealth_section_idx = -1
    for i, line in enumerate(lines):
        if "재물운 심층 분석" in line:
            wealth_section_idx = i
            break
            
    if wealth_section_idx != -1 and wealth_section_idx < 30:
        print(f"  - ✅ 재물운 핵심 섹션이 상단({wealth_section_idx}라인)에 배치됨.")
    else:
        print(f"  - ❌ 재물운 핵심 섹션 위치 부적절 ({wealth_section_idx}라인)")

    # 3. 헤더 Compact 모드 작동 확인
    print("\n[테스트 3] 헤더 Compact 모드 검증")
    if "#### 사주 구성 한눈에 보기" not in wealth:
        print("  - ✅ 재물운 헤더에서 상세 테이블 제거됨 (Compact 모드 정상)")
    else:
        print("  - ❌ 재물운 헤더에 여전히 상세 테이블 존재")

    if "#### 사주 구성 한눈에 보기" in lifetime:
        print("  - ✅ 평생사주 헤더에 상세 테이블 유지됨 (Full 모드 정상)")

    print("\n" + "="*80)
    if overlap < 40:
        print("🎉 결과: 중복 제거 및 카테고리 차별화 성공!")
    else:
        print("⚠️ 결과: 중복률이 여전히 높습니다. 추가 조정 필요.")
    print("="*80 + "\n")

if __name__ == "__main__":
    run_distinction_test()
