"""Full category fortune generation test"""
import os

if os.path.exists("saju_knowledge.db"):
    os.remove("saju_knowledge.db")
    print("DB reset")

from saju_db import init_db
init_db()

from fortune_generator import generate_fortune

# 11 categories (without gugap)
categories = [
    "jaemul", "aegjeong", "jikeop", "geongang", "pyeongsaeng",
    "gaeun", "hyeolaekhyeong", "mbti",
    "oneul", "ibeon", "sinnyeon"
]
cat_kr = [
    "jaemulun", "aegjeongun", "jikeopun", "geonganngun", "pyeongsaengsaju",
    "gaeunbeop", "hyeolaekhyeongbunsek", "mbtibunsek",
    "oneuluiunse", "ibeondalunse", "sinnyeonunse"
]
categories = [
    "jaemulun", "aegjeongun", "jikeopun", "geongangun", "pyeongsangsaju",
    "gaeunbeop", "hyeolaekhyeongbunsek", "mbtibunsek",
    "oneul", "ibeondalunse", "sinnyeonunse"
]

CATS = [
    "jaemulun", "aegjeongun", "jikeopun", "geongangun", "pyeongsangsaju",
    "gaeunbeop", "hyeolaekhyeongbunsek", "MBTIbunsek",
    "oneuluiunse", "ibeondalunse", "sinnyeonunse"
]

actual_cats = [
    "jaemulun", "aegjeongun", "jikeopun", "geongangun", "pyeongsangsaju",
    "gaeunbeop", "hyeolaekhyeongbunsek", "MBTIbunsek",
    "oneuluiunse", "ibeondalunse", "sinnyeonunse"
]

real_cats = [
    "재물운",
    "애정운",
    "직업운",
    "건강운",
    "평생사주",
    "개운법",
    "혈액형분석",
    "MBTI분석",
    "오늘의운세",
    "이번달운세",
    "신년운세",
]

profile = {
    "name": "박철세",
    "job": "보험계리사",
    "education": "대졸(4년)",
    "mbti": "ISTJ",
    "blood_type": "AO",
    "marital_status": "기혼",
    "children_count": 2,
}

total = 0
print("=" * 60)
print("Fortune Generation Test (11 categories)")
print("=" * 60)

for cat in real_cats:
    try:
        r = generate_fortune("1969-07-14", "09:30", cat, profile)
        c = r["char_count"]
        total += c
        mark = "pass" if c >= 5000 else "warn" if c >= 4000 else "low"
        print(f"  [{mark:4s}] {cat:10s} : {c:,} chars")
    except Exception as e:
        print(f"  [FAIL] {cat:10s} : {e}")

avg = total // len(real_cats)
print("=" * 60)
print(f"  AVG: {avg:,} chars")
print(f"  SUM: {total:,} chars")
print("=" * 60)
