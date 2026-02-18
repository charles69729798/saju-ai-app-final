import urllib.request
import json
import os

# 테스트 대상 페르소나
user_data = {
    "birth_date": "1990-05-05",
    "birth_time": "14:30",
    "name_korean": "김철수",
    "job": "소프트웨어 개발자",
    "mbti": "INTP",
    "blood_type": "A",
    "marital_status": "미혼",
    "education": "대학교 졸업"
}

# 비교할 카테고리
categories_to_compare = [
    "평생사주", 
    "직업운", 
    "재물운",
    "MBTI분석" 
]

output_file = "fortune_comparison_result.md"

def fetch_fortune(category):
    url = "http://localhost:8000/api/saju/analyze"
    headers = {"Content-Type": "application/json"}
    payload = user_data.copy()
    payload["category"] = category
    
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return json.load(response)["result"]
            return f"Error: Status {response.status}"
    except Exception as e:
        return f"Error: {str(e)}"

def run_analysis():
    print("🚀 Fetching fortune results for comparison...")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 운세 카테고리 간 상호 비교 분석 결과\n\n")
        f.write(f"**테스트 대상**: {user_data['name_korean']} ({user_data['birth_date']})\n")
        f.write("---\n\n")
        
        results = {}
        
        for cat in categories_to_compare:
            print(f"  - Requesting {cat}...")
            content = fetch_fortune(cat)
            results[cat] = content
            
            f.write(f"## [{cat}] 결과 (일부분 발췌)\n")
            f.write("```markdown\n")
            # 앞부분 500자 (헤더/기본분석) 확인
            f.write(content[:1000] + "\n... (중략) ...\n")
            # 뒷부분 1000자 (개운법/고전 등) 확인
            f.write(content[-1500:] + "\n")
            f.write("```\n\n")
            f.write("---\n\n")

    print(f"✅ Comparison data saved to {output_file}")

if __name__ == "__main__":
    run_analysis()
