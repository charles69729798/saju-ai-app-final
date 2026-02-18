import requests
import json

BASE_URL = "http://localhost:8000"

def test_guardian_logic():
    print("🚀 Testing 'Zodiac Guardian' logic...")
    
    payload = {
        "birth_date": "1990-01-01", # Year of the Horse (1990)
        "birth_time": "12:00",
        "name": "홍길동",
        "category": "평생사주"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/saju/analyze", json=payload)
        if response.status_code == 200:
            data = response.json()
            result = data.get("result", "")
            
            print("✅ API Response Received")
            
            # Check for Guardian section
            if "### 🛡️ 당신의 수호신:" in result:
                print("✅ Found 'Guardian' section in the report!")
                # Extract the guardian message to verify it's correct for the year
                if "말신(神)" in result:
                    print("✅ Correct Guardian (Horse) identified for 1990!")
                else:
                    print("❌ Incorrect Guardian identified.")
            else:
                print("❌ 'Guardian' section NOT found in the report.")
                print(f"Result snippet: {result[:500]}...")

        else:
            print(f"❌ API Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_guardian_logic()
