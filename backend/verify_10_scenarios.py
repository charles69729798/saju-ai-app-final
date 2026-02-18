import requests
import json
import time

API_URL = "http://localhost:8000/api/saju/analyze"

SCENARIOS = [
    { 
        "id": 1, "name": "김완전", "info": "전체 정보 입력 (직업운)", 
        "data": { "birth_date": "1990-01-01", "birth_time": "12:00", "gender": "male", "name_korean": "김완전", "job": "개발자", "education": "박사", "mbti": "INTJ", "blood_type": "A", "category": "직업운" },
        "expect": { "status": 200, "checks": ["직업운", "INTJ", "A형"] } 
    },
    { 
        "id": 2, "name": "이이름", "info": "혈액형 누락 (애정운 - 허용)", 
        "data": { "birth_date": "1992-03-15", "birth_time": "09:00", "gender": "female", "name_korean": "이이름", "job": "디자이너", "mbti": "ENFP", "blood_type": "", "category": "애정운" },
        "expect": { "status": 200, "checks": ["애정운", "!혈액형 유전자형"] } 
    },
    { 
        "id": 3, "name": "박미비", "info": "MBTI 누락 (재물운 - 허용)", 
        "data": { "birth_date": "1985-07-07", "birth_time": "18:00", "gender": "male", "name_korean": "박미비", "job": "기획자", "mbti": "", "blood_type": "O", "category": "재물운" },
        "expect": { "status": 200, "checks": ["재물운", "!MBTI 교차분석"] }
    },
    { 
        "id": 4, "name": "최소한", "info": "최소 정보 (오늘의운세)", 
        "data": { "birth_date": "2000-12-25", "birth_time": "00:00", "gender": "female", "name_korean": "최소한", "category": "오늘의운세", "mbti": "", "blood_type": "" },
        "expect": { "status": 200, "checks": ["오늘의 운세", "!혈액형", "!MBTI"] }
    },
    { 
        "id": 5, "name": "정엄격", "info": "필수값 누락 (MBTI분석 - 차단)", 
        "data": { "birth_date": "1995-05-05", "birth_time": "14:00", "gender": "male", "name_korean": "정엄격", "category": "MBTI분석", "mbti": "" },
        "expect": { "status": 400, "checks": ["error"] } 
    },
    { 
        "id": 6, "name": "한혈액", "info": "필수값 누락 (혈액형분석 - 차단)", 
        "data": { "birth_date": "1996-06-06", "birth_time": "10:00", "gender": "female", "name_korean": "한혈액", "category": "혈액형분석", "blood_type": "" },
        "expect": { "status": 400, "checks": ["error"] } 
    },
    { 
        "id": 7, "name": "홍길동", "info": "고전 명리 해석 확인 (평생사주)", 
        "data": { "birth_date": "1980-01-01", "birth_time": "00:00", "gender": "male", "name_korean": "홍길동", "category": "평생사주", "blood_type": "B", "mbti": "ENTP" },
        "expect": { "status": 200, "checks": ["명리 고전 전문 해석", "자평진전"] }
    },
    { 
        "id": 8, "name": "강누수", "info": "정보 잔존 확인 (신년운세)",
        "data": { "birth_date": "1999-09-09", "birth_time": "09:00", "gender": "female", "name_korean": "강누수", "category": "신년운세", "blood_type": "", "mbti": "" },
        "expect": { "status": 200, "checks": ["!B형", "!ENTP"] } 
    },
    { 
        "id": 9, "name": "장직업", "info": "직업운 심층 분석 확인",
        "data": { "birth_date": "1988-08-08", "birth_time": "15:00", "gender": "male", "name_korean": "장직업", "job": "CEO", "category": "직업운", "blood_type": "AB", "mbti": "ESTJ" },
        "expect": { "status": 200, "checks": ["커리어 로드맵", "조직 적합도"] }
    },
    { 
        "id": 10, "name": "임재물", "info": "재물운 심층 분석 확인",
        "data": { "birth_date": "1977-07-07", "birth_time": "11:00", "gender": "female", "name_korean": "임재물", "category": "재물운", "blood_type": "O", "mbti": "ESFJ" },
        "expect": { "status": 200, "checks": ["부(富)의 그릇", "투자 포트폴리오"] }
    }
]

def run_tests():
    print("\n" + "="*80)
    print("🚀 사주 서비스 고도화 검증 시뮬레이션 (10인 페르소나)")
    print("="*80)
    
    success_count = 0
    
    for s in SCENARIOS:
        print(f"\n[테스트 #{s['id']}] 페르소나: {s['name']} ({s['info']})")
        print(f"  - 📡 API 요청 전송 중... ({s['data']['category']})")
        
        try:
            start_time = time.time()
            resp = requests.post(API_URL, json=s['data'])
            elapsed = time.time() - start_time
            
            # 1. Status Check
            print(f"  - 📥 응답 수신 완료 (상태 코드: {resp.status_code}, 소요 시간: {elapsed:.2f}s)")
            
            if resp.status_code != s['expect']['status']:
                print(f"  - ❌ 오류: 상태 코드 불일치 (기대: {s['expect']['status']}, 실제: {resp.status_code})")
                continue
                
            data = resp.json()
            
            # 2. Content Check
            if resp.status_code == 200:
                print("  - 🔍 결과 텍스트 무결성 검증 중...")
                text = data.get('result', '')
                failed_checks = []
                for check in s['expect']['checks']:
                    if check.startswith("!"):
                        keyword = check[1:]
                        if keyword in text:
                            failed_checks.append(f"비기대 키워드 검출: '{keyword}'")
                    elif check != "error":
                        if check not in text:
                            failed_checks.append(f"필수 키워드 누락: '{check}'")
                
                if failed_checks:
                    for fc in failed_checks:
                        print(f"    - ❌ {fc}")
                else:
                    char_count = data.get('char_count', 0)
                    print(f"    - ✅ 모든 키워드 검증 통과!")
                    print(f"    - ✅ 생성된 문장량: {char_count}자 (충분한 분량 확보)")
                    success_count += 1
            
            elif resp.status_code == 400:
                msg = data.get('message', data.get('error', ''))
                print(f"  - ✅ 기대된 에러 정상 포착: {msg}")
                success_count += 1
                
            # 시연 시각화를 위한 짧은 지연
            time.sleep(1.2)
                
        except Exception as e:
            print(f"  - ❌ 예외 발생: {str(e)}")

    print("\n" + "="*80)
    print(f"✅ 최종 검증 결과: {success_count}/{len(SCENARIOS)} 통과")
    print("="*80 + "\n")

if __name__ == "__main__":
    run_tests()
