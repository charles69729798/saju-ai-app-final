
import sqlite3
import requests
import json

def check_db():
    print("--- Database Diagnostics ---")
    try:
        conn = sqlite3.connect('backend/saju_knowledge.db')
        c = conn.cursor()
        
        # Check celebrity count
        c.execute("SELECT COUNT(*) FROM celeb_saju")
        count = c.fetchone()[0]
        print(f"✅ Total Celebrity Entries: {count}")
        
        # Check recent star additions
        c.execute("SELECT name, category, mbti FROM celeb_saju ORDER BY id DESC LIMIT 5")
        stars = c.fetchall()
        print("🔍 Recently Added Stars:")
        for s in stars:
            print(f"   - {s[0]} ({s[1]}) | MBTI: {s[2]}")
            
        conn.close()
    except Exception as e:
        print(f"❌ DB Error: {e}")

def check_api():
    print("\n--- API Diagnostics ---")
    base_url = "http://localhost:8000/api"
    
    # 1. Categories
    try:
        res = requests.get(f"{base_url}/categories")
        if res.status_code == 200:
            print(f"✅ Categories API: OK ({len(res.json()['categories'])} items)")
        else:
            print(f"❌ Categories API: Failed ({res.status_code})")
    except Exception as e:
        print(f"❌ Categories API Error: {e}")
        
    # 2. Celebrity List
    try:
        res = requests.get(f"{base_url}/celebs")
        if res.status_code == 200:
            count = len(res.json()['celebs'])
            print(f"✅ Celebs API: OK ({count} items)")
        else:
            print(f"❌ Celebs API: Failed ({res.status_code})")
    except Exception as e:
        print(f"❌ Celebs API Error: {e}")

    # 3. Sample Analysis (Dry Run)
    try:
        payload = {
            "birth_date": "1990-01-01",
            "birth_time": "12:00",
            "category": "평생사주",
            "mbti": "INFJ",
            "gender": "F",
            "name_hanja": "金美娜"
        }
        res = requests.post(f"{base_url}/saju/analyze", json=payload)
        if res.status_code == 200:
            print("✅ Analysis API: OK (Report Generated)")
        else:
            print(f"❌ Analysis API: Failed ({res.status_code})")
            print(res.text)
    except Exception as e:
        print(f"❌ Analysis API Error: {e}")

if __name__ == "__main__":
    check_db()
    check_api()
