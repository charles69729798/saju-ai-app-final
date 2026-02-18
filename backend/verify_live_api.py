import urllib.request
import json
import time

def verify_api():
    url = "http://localhost:8000/api/saju/analyze"
    headers = {"Content-Type": "application/json"}
    data = {
        "birth_date": "1990-01-01",
        "birth_time": "12:00",
        "category": "직업운",
        "name_korean": "홍길동",
        "job": "개발자",
        "mbti": "INTJ",
        "blood_type": "AB"
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    
    print(f"Connecting to {url}...")
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                result = json.load(response)
                fortune_text = result["result"]
                char_count = result["char_count"]
                
                print(f"✅ API Call Success!")
                print(f"Total Characters: {char_count}")
                
                # Check for key sections
                checks = {
                    "Classical Wisdom": "명리 고전 전문 해석",
                    "Contextual Cross Analysis": "MBTI 교차분석",
                    "Blood Type Analysis": "혈액형 유전자형"
                }
                
                all_passed = True
                for label, keyword in checks.items():
                    if keyword in fortune_text:
                        print(f"  [PASS] {label} found.")
                    else:
                        print(f"  [FAIL] {label} NOT found.")
                        all_passed = False
                
                if all_passed and char_count > 6000:
                    print("\n🎉 SYSTEM VERIFICATION PASSED!")
                    return True
                else:
                    print("\n⚠️ VERIFICATION FAILED: Missing sections or short length.")
                    return False
            else:
                print(f"❌ Server returned status: {response.status}")
                return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    # Wait for server to be fully ready
    time.sleep(2)
    verify_api()
