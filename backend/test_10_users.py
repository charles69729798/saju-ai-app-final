import json
from fortune_generator import generate_fortune
from datetime import datetime

# 10명의 가상 사용자 프로필
test_profiles = [
    {"name": "김철수", "birth_date": "1980-06-25", "birth_time": "12:30", "gender": "남성", "mbti": "ISTJ", "blood_type": "AO", "marital_status": "기혼", "occupation": "금융업"},
    {"name": "이영희", "birth_date": "1992-03-12", "birth_time": "18:45", "gender": "여성", "mbti": "ENFP", "blood_type": "B", "marital_status": "미혼", "occupation": "디자이너"},
    {"name": "박지민", "birth_date": "1975-11-05", "birth_time": "08:20", "gender": "남성", "mbti": "ENTJ", "blood_type": "O", "marital_status": "기혼", "occupation": "사업가"},
    {"name": "최유진", "birth_date": "1988-12-24", "birth_time": "15:10", "gender": "여성", "mbti": "ISFJ", "blood_type": "A", "marital_status": "기혼", "occupation": "교사"},
    {"name": "정우성", "birth_date": "1995-09-02", "birth_time": "10:30", "gender": "남성", "mbti": "INTP", "blood_type": "AB", "marital_status": "미혼", "occupation": "개발자"},
    {"name": "한고은", "birth_date": "1982-05-15", "birth_time": "23:45", "gender": "여성", "mbti": "INFJ", "blood_type": "O", "marital_status": "미혼", "occupation": "작가"},
    {"name": "강다니엘", "birth_date": "2000-01-20", "birth_time": "06:15", "gender": "남성", "mbti": "ENFJ", "blood_type": "A", "marital_status": "미혼", "occupation": "연예인"},
    {"name": "조미령", "birth_date": "1970-08-30", "birth_time": "14:20", "gender": "여성", "mbti": "ESFJ", "blood_type": "B", "marital_status": "기혼", "occupation": "공무원"},
    {"name": "송중기", "birth_date": "1985-04-10", "birth_time": "20:50", "gender": "남성", "mbti": "INTJ", "blood_type": "A", "marital_status": "미혼", "occupation": "전문직"},
    {"name": "임윤아", "birth_date": "1998-02-14", "birth_time": "05:30", "gender": "여성", "mbti": "ESFP", "blood_type": "O", "marital_status": "미혼", "occupation": "유튜버"}
]

categories = ["재물운", "직업운", "애정운", "평생사주", "신년운세"]

def run_tests():
    report_lines = ["# 🧪 10인 가상 사용자 카테고리별 차별화 검증 리포트\n"]
    report_lines.append(f"테스트 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append("## 1. 테스트 목적\n사용자 프로필 및 일주(日柱) 데이터 보강에 따른 카테고리별 출력물의 정합성 및 차별화 여부 검증 (오프라인 로컬 DB 기반)\n")

    for i, profile in enumerate(test_profiles):
        report_lines.append(f"### 👤 사용자 {i+1}: {profile['name']} ({profile['mbti']}, {profile['blood_type']}형, {profile['occupation']})\n")
        
        for cat in categories:
            result = generate_fortune(profile["birth_date"], profile["birth_time"], cat, profile)
            text = result["fortune"]
            
            # 리포트에는 핵심 섹션만 요약해서 기록
            summary_start = text.find("###")
            summary = text[summary_start:summary_start+1000] + "..." # 처음 1000자만 추출
            
            report_lines.append(f"#### 📂 카테고리: {cat}\n")
            report_lines.append(f"{summary}\n")
            report_lines.append("---\n")

    with open("test_results_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    
    print("✅ 10인 테스트 완료. 'test_results_report.md'를 확인하세요.")

if __name__ == "__main__":
    run_tests()
