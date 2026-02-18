
import requests
import json
import difflib

API_BASE = "http://localhost:8080/api"

USERS = [
    {"name": "User11 (ISTP)", "birth_date": "1992-03-15", "mbti": "ISTP", "gender": "M"},
    {"name": "User12 (ENFJ)", "birth_date": "1988-11-20", "mbti": "ENFJ", "gender": "F"},
    {"name": "User13 (INTJ)", "birth_date": "1995-07-07", "mbti": "INTJ", "gender": "M"},
]

THEMES = ["평생사주", "재물운", "애정운"]

def get_similarity(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).ratio()

def run_bulk_verification():
    print("🚀 Starting Bulk Verification for 10 users...")
    results = []
    
    for user in USERS:
        user_reports = {}
        print(f"Analyzing {user['name']}...")
        for theme in THEMES:
            payload = {
                "user_profile": {
                    "birth_date": user["birth_date"],
                    "birth_time": "12:00",
                    "name_korean": user["name"],
                    "gender": user["gender"],
                    "mbti": user["mbti"]
                },
                "category": theme
            }
            
            # For Relation Themes, add partner info
            if theme in ["애정운", "궁합"]:
                payload["relation_data"] = {
                    "target_name": "상대방",
                    "target_birth_date": "1995-12-25",
                    "target_birth_time": "12:00",
                    "target_gender": "M" if user["gender"] == "F" else "F",
                    "relation_code": "LOVER"
                }
            
            try:
                res = requests.post(f"{API_BASE}/saju/analyze", json=payload)
                data = res.json()
                if data["status"] == "success":
                    user_reports[theme] = data["result"]
                else:
                    print(f"  ❌ Failed {theme}: {data.get('message')}")
            except Exception as e:
                print(f"  ❌ Error {theme}: {e}")
        
        results.append({"user": user["name"], "reports": user_reports})

    # Analysis
    print("\n" + "="*50)
    print("BULK ANALYSIS REPORT")
    print("="*50)
    
    total_avg_sim = 0
    sim_count = 0
    
    for entry in results:
        user = entry["user"]
        reports = entry["reports"]
        themes = list(reports.keys())
        
        print(f"\n[User: {user}]")
        
        # Check for Blood Chemistry (should be 0)
        blood_count = sum(1 for text in reports.values() if "혈액형" in text)
        if blood_count > 0:
            print(f"  ⚠️ ALERT: '혈액형' found in {blood_count} reports!")
        else:
            print("  ✅ Legacy 'Blood Chemistry' excluded.")
            
        # Check for MBTI consistency
        mbti_count = sum(1 for theme, text in reports.items() if theme == "MBTI분석" and user["mbti"] in text)
        if mbti_count > 0:
            print(f"  ✅ MBTI Sync confirmed.")
        
        # Cross-theme Similarity check
        print("  Similarity Matrix:")
        for i in range(len(themes)):
            for j in range(i + 1, len(themes)):
                sim = get_similarity(reports[themes[i]], reports[themes[j]])
                print(f"    - {themes[i]} vs {themes[j]}: {sim:.1%}")
                total_avg_sim += sim
                sim_count += 1

    if sim_count > 0:
        overall_avg = total_avg_sim / sim_count
        print(f"\n📈 Overall Cross-Theme Similarity: {overall_avg:.1%}")
        if overall_avg < 0.30:
            print("  ✅ Redundancy Optimization Target (<30%) Met!")
        else:
            print("  ⚠️ Redundancy still higher than target.")

if __name__ == "__main__":
    run_bulk_verification()
