import requests
import json

payload = {
    'birth_date': '2004-08-31',
    'birth_time': '12:00',
    'name_korean': 'charles',
    'gender': 'M',
    'mbti': 'INTJ',
    'category': '평생사주',
    'relation_type': 'lover'
}

print("Sending request to http://localhost:8000/api/saju/analyze ...")
try:
    res = requests.post('http://localhost:8000/api/saju/analyze', json=payload, timeout=10)
    print(f"Status Code: {res.status_code}")
    if res.status_code == 200:
        print("Success! (First 100 chars of result):")
        print(res.json().get('fortune', '')[:100])
    else:
        print("Error Response:")
        print(res.text)
except requests.exceptions.Timeout:
    print("Request Timed Out! This indicates the server is hanging.")
except Exception as e:
    print(f"An error occurred: {e}")
