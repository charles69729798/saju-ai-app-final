import requests
import json
import os
from datetime import datetime

API_URL = "http://localhost:8000/api/saju/analyze"
REPORT_FILE = r"C:\Users\pc1\.gemini\antigravity\brain\067f724d-780a-440d-b979-544a8bc9dc42\verification_report_10_users.md"

# 10명의 가상 사용자 시나리오
SCENARIOS = [
    {
        "id": 1,
        # 모든 정보가 있는 경우
        "desc": "Full Info (김완전)",
        "profile": {
            "name": "김완전", "gender": "male", "birth_year": 1990, "birth_month": 1, "birth_day": 1, "birth_hour": 12,
            "blood_type": "A", "mbti": "INTJ", "job": "개발자", "education": "박사"
        },
        "check": ["blood", "mbti"]
    },
    {
        "id": 2,
        # 혈액형 정보 없음
        "desc": "No Blood Type (이이름)",
        "profile": {
            "name": "이이름", "gender": "female", "birth_year": 1992, "birth_month": 3, "birth_day": 15, "birth_hour": 9,
            "blood_type": "", "mbti": "ENFP", "job": "디자이너", "education": "대졸"
        },
        "check": ["no_blood", "mbti"]
    },
    {
        "id": 3,
        # MBTI 정보 없음
        "desc": "No MBTI (박미비)",
        "profile": {
            "name": "박미비", "gender": "male", "birth_year": 1985, "birth_month": 7, "birth_day": 7, "birth_hour": 18,
            "blood_type": "O", "mbti": "", "job": "기획자", "education": "대졸"
        },
        "check": ["blood", "no_mbti"]
    },
    {
        "id": 4,
        # 최소 정보 (혈액형, MBTI, 직업, 학력 없음)
        "desc": "Minimal Info (최소한)",
        "profile": {
            "name": "최소한", "gender": "female", "birth_year": 2000, "birth_month": 12, "birth_day": 25, "birth_hour": 0,
            "blood_type": "", "mbti": "", "job": "", "education": ""
        },
        "check": ["no_blood", "no_mbti"]
    },
    {
        "id": 5,
        # Null 값 처리 확인
        "desc": "Null Values (널체크)",
        "profile": {
            "name": "널체크", "gender": "male", "birth_year": 1988, "birth_month": 8, "birth_day": 8, "birth_hour": 8,
            "blood_type": None, "mbti": None, "job": None, "education": None
        },
        "check": ["no_blood", "no_mbti"]
    },
    {
        "id": 6,
        # 연속성 테스트 1 (정보 있음)
        "desc": "Sequence 1 (순서일)",
        "profile": {
            "name": "순서일", "gender": "female", "birth_year": 1995, "birth_month": 5, "birth_day": 5, "birth_hour": 14,
            "blood_type": "AB", "mbti": "ISTP", "job": "엔지니어"
        },
        "check": ["blood", "mbti"]
    },
    {
        "id": 7,
        # 연속성 테스트 2 (직전 사용자 정보 잔존 여부 확인)
        "desc": "Sequence 2 (순서이 - 정보없음)",
        "profile": {
            "name": "순서이", "gender": "male", "birth_year": 1996, "birth_month": 6, "birth_day": 6, "birth_hour": 14,
            "blood_type": "", "mbti": "", "job": ""
        },
        "check": ["no_leakage_blood", "no_leakage_mbti"]
    },
    {
        "id": 8,
        # 혈액형 소문자 입력 ('a') -> 매핑 확인
        "desc": "Lowercase Blood (소문자)",
        "profile": {
            "name": "소문자", "gender": "female", "birth_year": 1980, "birth_month": 2, "birth_day": 20, "birth_hour": 10,
            "blood_type": "a", "mbti": "isfj", "job": "선생님"
        },
        "check": ["blood", "mbti"] # 소문자도 처리되어야 함 (현재 로직엔 없으나 확인용)
    },
    {
        "id": 9,
        # 직업만 있는 경우
        "desc": "Job Only (직업만)",
        "profile": {
            "name": "직업만", "gender": "male", "birth_year": 1999, "birth_month": 9, "birth_day": 9, "birth_hour": 9,
            "blood_type": "B", "mbti": "ENTP", "job": "요리사", "education": ""
        },
        "check": ["blood", "mbti"]
    },
    {
        "id": 10,
        # 최종 확인
        "desc": "Final Check (막판왕)",
        "profile": {
            "name": "막판왕", "gender": "female", "birth_year": 1990, "birth_month": 1, "birth_day": 1, "birth_hour": 0,
            "blood_type": "O", "mbti": "ESFJ", "job": "운영"
        },
        "check": ["blood", "mbti"]
    }
]

def generate_report():
    report_lines = []
    report_lines.append(f"# 🧪 가상 사용자 10명 데이터 무결성 검증 보고서")
    report_lines.append(f"**생성 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append(f"본 보고서는 10명의 가상 인물 시나리오를 통해 앱의 데이터 처리 정확성, 누락 정보 처리, 정보 잔존(Leakage) 문제를 검증한 결과입니다.\n")
    
    report_lines.append("## 📊 테스트 요약")
    report_lines.append("| ID | 이름 | 테스트 시나리오 | 혈액형/MBTI 입력 | 검증 결과 | 비고 |")
    report_lines.append("|:---:|:---|:---|:---:|:---:|:---|")

    detailed_results = []
    
    for case in SCENARIOS:
        p = case['profile']
        
        # Payload 생성
        payload = {
            "birth_date": f"{p['birth_year']}-{p['birth_month']:02d}-{p['birth_day']:02d}",
            "birth_time": f"{p['birth_hour']:02d}:00",
            "gender": p['gender'],
            "name_korean": p['name'],
            "job": p.get('job', ''),
            "education": p.get('education', ''),
            "mbti": p.get('mbti', ''),
            "blood_type": p.get('blood_type', ''),
            "category": "직업운" # 직업운이 가장 많은 정보를 사용함
        }
        
        status = "✅ Pass"
        note = ""
        
        try:
            resp = requests.post(API_URL, json=payload)
            if resp.status_code != 200:
                status = "❌ Error"
                note = f"HTTP {resp.status_code}"
                text = ""
            else:
                data = resp.json()
                text = data.get("result", "")
                
                # 검증 로직
                checks = case['check']
                errors = []
                
                has_blood = "혈액형" in text and "유전자형 분석" in text
                has_mbti = "MBTI" in text and "교차분석" in text
                
                # 혈액형 (blood) 체크
                if "blood" in checks and not has_blood:
                    # Note: 소문자 처리는 현재 DB 로직에 없어서 실패할 수 있음 (확인용)
                    if p.get('blood_type') == 'a': # 소문자 케이스 예외 처리 (만약 실패하면)
                         pass # 지금은 Strict하게 Fail로 처리
                    errors.append("혈액형 누락")
                
                # 혈액형 없음 (no_blood) 체크 - 있으면 실패
                if "no_blood" in checks and "혈액형 유전자형 분석" in text:
                    errors.append("혈액형 오출력")
                
                # MBTI (mbti) 체크
                if "mbti" in checks and not has_mbti:
                    errors.append("MBTI 누락")
                
                # MBTI 없음 (no_mbti) 체크 - 있으면 실패
                if "no_mbti" in checks and "MBTI 교차분석" in text:
                    errors.append("MBTI 오출력")
                    
                # 정보 잔존 (no_leakage) 체크 - 이전 정보(Case 6)가 나오면 안됨
                if "no_leakage_blood" in checks:
                    if "AB형" in text or "AB-복합" in text: # Case 6의 혈액형
                         errors.append("이전 혈액형 잔존")
                
                if "no_leakage_mbti" in checks:
                    if "ISTP" in text: # Case 6의 MBTI
                        errors.append("이전 MBTI 잔존")

                if errors:
                    status = "⚠️ Fail"
                    note = ", ".join(errors)
                    
        except Exception as e:
            status = "❌ Exception"
            note = str(e)
        
        # 요약표 행 추가
        input_summary = f"{p.get('blood_type', '❌')}/{p.get('mbti', '❌')}"
        if p.get('blood_type') is None: input_summary = "None/None"
        
        report_lines.append(f"| {case['id']} | **{p['name']}** | {case['desc']} | {input_summary} | {status} | {note} |")
        
        # 상세 결과 저장
        detailed_results.append(f"### SCENARIO {case['id']}: {case['desc']}")
        detailed_results.append(f"- **입력 프로필**: `{p}`")
        detailed_results.append(f"- **검증 항목**: `{case['check']}`")
        detailed_results.append(f"- **결과 상태**: {status}")
        if note:
             detailed_results.append(f"- **발견된 문제**: 🔴 {note}")
        detailed_results.append(f"- **출력 텍스트 길이**: {len(text)}자")
        detailed_results.append(f"- **주요 섹션 포함 여부**: 혈액형[{'O' if has_blood else 'X'}], MBTI[{'O' if has_mbti else 'X'}]")
        detailed_results.append(f"\n---\n")

    report_lines.append("\n## 📝 상세 테스트 로그")
    report_lines.extend(detailed_results)
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    
    print(f"Report generated at: {REPORT_FILE}")

if __name__ == "__main__":
    generate_report()
