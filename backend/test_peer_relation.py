import requests
import json

BASE_URL = "http://localhost:8000"

def test_peer_relation():
    print("🚀 Testing 'Colleague/Peer' relationship context...")
    
    payload = {
        "birth_date": "1990-01-01",
        "birth_time": "12:00",
        "name": "홍길동",
        "job": "Software Engineer",
        "mbti": "INTJ",
        "blood_type": "A",
        "category": "평생사주",
        "relation_type": "peer"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/saju/analyze", json=payload)
        if response.status_code == 200:
            data = response.json()
            result = data.get("result", "")
            
            print("✅ API Response Received")
            
            # Check for specific 'peer' context in the result
            if "동기/동료" in result and "커리어 파트너십" in result:
                print("✅ Found 'peer' specific context in the report!")
            else:
                print("❌ 'peer' specific context NOT found in the report.")
                print(f"Result snippet: {result[:500]}...")
                
            # Check if headers reflect the context
            if "| 관계 유형 | 동기/동료 |" in result:
                 print("✅ Found '관계 유형: 동기/동료' in the header table!")
            else:
                 print("❌ '관계 유형: 동기/동료' NOT found in the header table.")

        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_peer_relation()
