import requests
import difflib

API_URL = "http://localhost:8000/api/saju/analyze"

PROFILE = {
    "name": "홍길동",
    "gender": "male", 
    "birth_year": 1990, 
    "birth_month": 1, 
    "birth_day": 1, 
    "birth_hour": 12,
    "blood_type": "A", 
    "mbti": "INTJ", 
    "job": "개발자", 
    "education": "대졸"
}

def get_fortune(category):
    payload = {
        "birth_date": f"{PROFILE['birth_year']}-{PROFILE['birth_month']:02d}-{PROFILE['birth_day']:02d}",
        "birth_time": f"{PROFILE['birth_hour']:02d}:00",
        "gender": PROFILE['gender'],
        "name_korean": PROFILE['name'],
        "job": PROFILE['job'],
        "education": PROFILE['education'],
        "mbti": PROFILE['mbti'],
        "blood_type": PROFILE['blood_type'],
        "category": category
    }
    resp = requests.post(API_URL, json=payload)
    if resp.status_code == 200:
        return resp.json().get("result", "")
    return None

def compare_fortunes():
    print("🚀 Generating Wealth Luck...")
    wealth = get_fortune("재물운")
    
    print("🚀 Generating Love Luck...")
    love = get_fortune("애정운")
    
    if not wealth or not love:
        print("❌ Failed to generate fortunes.")
        return

    print("\n🔍 Comparing Results:")
    
    wealth_lines = set([l.strip() for l in wealth.split('\n') if l.strip()])
    love_lines = set([l.strip() for l in love.split('\n') if l.strip()])
    
    common_lines = wealth_lines.intersection(love_lines)
    
    print(f"- Total Lines (Wealth): {len(wealth_lines)}")
    print(f"- Total Lines (Love): {len(love_lines)}")
    print(f"- Common Lines: {len(common_lines)}")
    print(f"- Similarity: {len(common_lines) / min(len(wealth_lines), len(love_lines)) * 100:.1f}%")
    
    print("\n📜 Common Sections (First 10 lines):")
    for msg in list(common_lines)[:10]:
        print(f"  - {msg[:50]}...")
        
    print(f"Sample Wealth Length: {len(wealth)}")
    print(f"Sample Love Length: {len(love)}")
    
    # Check for specific blocks that should remain generic
    generics = ["오행 분석", "십성 분석", "생활 속 개운법", "풍수 인테리어"]
    print("\n🧐 Checking Generic Sections:")
    for g in generics:
        in_wealth = g in wealth
        in_love = g in love
        print(f"  - {g}: Wealth[{'O' if in_wealth else 'X'}] / Love[{'O' if in_love else 'X'}]")
        
    print(f"\nSimilarity Check: {len(common_lines)} common lines.")

if __name__ == "__main__":
    compare_fortunes()
