import os
import json
import sqlite3
import datetime
import sys

# Add current directory to path just in case
sys.path.append(os.getcwd())

import saju_calculator
import fortune_generator

# Sample User Data for Audit
user_profile = {
    "name": "홍길동",
    "gender": "male",
    "birth_date": "1990-01-01",
    "birth_time": "12:30",
    "calendar_type": "solar",
    "job": "IT 기획자",
    "mbti": "INTJ",
    "blood_type": "A",
    "marital_status": "single",
    "education": "대졸",
    # Target (for compatibility)
    "target_name": "성춘향",
    "target_gender": "female",
    "target_birth_date": "1993-05-05",
    "target_birth_time": "14:20",
    "relation_type": "lover"
}

categories = [
    "평생사주", "오늘의운세", "이번달운세", "신년운세", 
    "재물운", "애정운", "직업운", "건강운", 
    "궁합", "개운법", "혈액형분석", "MBTI분석"
]

# Save to Desktop for user convenience
output_file = r"C:\Users\pc1\Desktop\saju_audit_data.md"

def export_all():
    print("Generating comprehensive audit data from backend...")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 🔮 사주 AI 콘텐츠 감사용 전체 리포트 (Full Audit Data)\n\n")
        f.write(f"**생성일시**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # 1. User Profile Raw
        f.write("## 👤 프로필 정보\n")
        f.write("```json\n")
        f.write(json.dumps(user_profile, indent=2, ensure_ascii=False))
        f.write("\n```\n\n")
        
        # 2. Category Results
        for cat in categories:
            print(f"Processing category: {cat}")
            try:
                # generate_fortune returns (result_text, is_cached)
                result_text, _ = fortune_generator.generate_fortune(user_profile, category=cat)
                
                f.write(f"---\n# [CATEGORY] {cat}\n\n")
                f.write(result_text)
                f.write("\n\n")
            except Exception as e:
                f.write(f"### [ERROR] {cat}: {str(e)}\n\n")

    print(f"✅ Success! Audit data saved to: {output_file}")

if __name__ == "__main__":
    export_all()
