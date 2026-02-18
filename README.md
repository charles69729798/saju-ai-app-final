# 사주 AI 상담 서버

NotebookLM 기반 AI 사주 상담 API 서버입니다.

## 설치 및 실행

### 1. 의존성 설치
```bash
cd backend
pip install -r requirements.txt
```

### 2. 환경 변수 설정 (선택)
```bash
# .env 파일 생성
NOTEBOOKLM_NOTEBOOK_ID=a0997172-3a52-47c1-b3f8-74fcbdfbade0
```

### 3. 서버 실행
```bash
python main.py
```

서버는 `http://localhost:8000`에서 실행됩니다.

## API 문서

서버 실행 후 `http://localhost:8000/docs`에서 자동 생성된 API 문서를 확인할 수 있습니다.

## 주요 엔드포인트

- `GET /api/categories` - 분석 카테고리 목록 조회
- `POST /api/saju/calculate` - 사주팔자 계산
- `POST /api/saju/analyze` - AI 사주 상담

## 테스트 예시

```bash
# 1. 사주 계산
curl -X POST "http://localhost:8000/api/saju/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1969-07-14",
    "birth_time": "09:30",
    "gender": "남성",
    "is_lunar": false
  }'

# 2. AI 상담 (재물운)
curl -X POST "http://localhost:8000/api/saju/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "user_profile": {
      "birth_date": "1969-07-14",
      "birth_time": "09:30",
      "gender": "남성",
      "name_korean": "박철세",
      "name_hanja": "朴哲世",
      "blood_type_genotype": "AO",
      "mbti": "ISTJ",
      "job": "소프트웨어 개발자"
    },
    "saju_data": {...},
    "category": "재물운"
  }'
```
