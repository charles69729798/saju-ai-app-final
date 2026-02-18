
import sys
import os
import json

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from fortune_generator import generate_fortune
from saju_calculator import calculate_full_saju

def run_audit():
    profile = {
        "name_korean": "홍길동",
        "gender": "M",
        "mbti": "ENFP",
        "birth_date": "1990-05-15",
        "birth_time": "14:30",
        "job": "Software Engineer"
    }

    categories = [
        "평생사주", "재물운", "직업운", "애정운", "건강운", "신년운세", "MBTI분석"
    ]

    results = {}
    for cat in categories:
        print(f"Generating: {cat}...")
        res = generate_fortune(profile["birth_date"], profile["birth_time"], cat, profile)
        results[cat] = res["fortune"]

    # 1. Similarity Audit
    print("\n" + "="*50)
    print("CROSS-THEME SIMILARITY AUDIT")
    print("="*50)

    for i in range(len(categories)):
        for j in range(i + 1, len(categories)):
            cat1 = categories[i]
            cat2 = categories[j]
            
            text1 = results[cat1]
            text2 = results[cat2]
            
            # Simple line-by-line comparison
            lines1 = set([l.strip() for l in text1.split('\n') if len(l.strip()) > 20])
            lines2 = set([l.strip() for l in text2.split('\n') if len(l.strip()) > 20])
            
            intersection = lines1.intersection(lines2)
            similarity = len(intersection) / max(len(lines1), len(lines2)) * 100
            
            print(f"[{cat1}] vs [{cat2}]: {similarity:.1f}% Similarity ({len(intersection)} overlapping long lines)")

    # 2. Coach Tip Audit
    print("\n" + "="*50)
    print("COACH'S LAST TIP AUDIT")
    print("="*50)
    for cat in categories:
        text = results[cat]
        tip_start = text.find("### 🗝️ Coach's Last Tip")
        if tip_start != -1:
            tip = text[tip_start:].split('\n')[1]
            print(f"[{cat}]: {tip}")
        else:
            print(f"[{cat}]: NOT FOUND")

if __name__ == "__main__":
    run_audit()
