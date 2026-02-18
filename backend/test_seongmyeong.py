from saju_calculator import calculate_full_saju
from fortune_blocks import build_name_analysis_block
from saju_db import init_db

# DB 초기화 확인
init_db()

# 1. 샘플 프로필 (박철세)
profile = {
    "name": "박철세",
    "name_hanja": "朴哲世",
    "job": "보험계리사",
    "mbti": "ISTJ",
    "blood_type": "AO"
}

# 2. 사주 계산
saju = calculate_full_saju("1980-05-15", "14:00")

# 3. 성명학 블록 생성 테스트
print("=== 성명학 분석 블록 테스트 ===")
block = build_name_analysis_block(saju, profile)
if block:
    print(block)
else:
    print("성명학 블록이 생성되지 않았습니다. (데이터 매칭 실패 가능성)")
