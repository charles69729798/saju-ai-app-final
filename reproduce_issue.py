
import requests
import json

def reproduce_error():
    url = "http://localhost:8000/api/saju/analyze"
    headers = {"Content-Type": "application/json"}
    
    # Data extracted exactly from user screenshot
    payload = {
        "birth_date": "2004-07-17",
        "birth_time": "09:18",
        "category": "애정운", # implied by 'User Relation' context usually
        "relation_type": "lover", # '연인/썸' is selected
        "name_hanja": "", # Not visible
        "job": "", # Not visible
        "education": "", # Not visible
        "mbti": "INTJ",
        "blood_type": "A", # Defaulting
        "marital_status": "Single", # Defaulting
        "children_count": 0,
        "relation_data": {
            "target_name": "이사이",
            "target_birth": "2010-05-03", 
            "target_time": "12:00",
            "relation_code": "LOVER", # Derived from 'lover' type
            "target_mbti": "ESTJ"
        }
    }

    print(f"🚀 Sending User's Exact Data to {url}...")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"📥 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                print("\n✅ SUCCESS: Backend handled this data correctly.")
            else:
                print(f"\n❌ FAILED: Backend returned logic error: {data}")
        else:
            print(f"\n❌ FAILED: HTTP {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"\n❌ EXCEPTION: {e}")

if __name__ == "__main__":
    reproduce_error()
