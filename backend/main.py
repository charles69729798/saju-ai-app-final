"""
FastAPI 메인 애플리케이션
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from models import UserProfile, SajuData, AnalysisRequest, AnalysisResponse
from saju_calculator import calculate_full_saju
from fortune_generator import generate_fortune
from saju_db import query_celebs

app = FastAPI(
    title="사주 AI 상담 API",
    description="NotebookLM 기반 AI 사주 상담 서버",
    version="1.0.0"
)

# CORS 설정 (프론트엔드에서 접근 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    """서버 상태 확인"""
    return {
        "message": "사주 AI 상담 API 서버 정상 작동 중",
        "version": "1.0.0"
    }


@app.get("/api/categories")
def get_categories():
    """사용 가능한 분석 카테고리 목록"""
    return {
        "categories": [
            {"id": "평생사주", "name": "평생사주 (종합운세)", "priority": "필수"},
            {"id": "오늘의운세", "name": "오늘의 운세", "priority": "필수"},
            {"id": "이번달운세", "name": "이번 달 운세", "priority": "중요"},
            {"id": "신년운세", "name": "신년운세 (2026년)", "priority": "필수"},
            {"id": "재물운", "name": "재물운 (금전운)", "priority": "필수"},
            {"id": "애정운", "name": "애정운 (연애운)", "priority": "필수"},
            {"id": "직업운", "name": "직업운 (사업운)", "priority": "필수"},
            {"id": "건강운", "name": "건강운", "priority": "중요"},
            {"id": "궁합", "name": "궁합", "priority": "중요"},
            {"id": "개운법", "name": "개운법", "priority": "중요"},
        ]
    }


@app.get("/api/celebs")
def search_celebs(search: str = "", category: str = None):
    """스타/유명인 검색 API"""
    celebs = query_celebs(category, search)
    return {"celebs": celebs}


@app.post("/api/saju/calculate", response_model=SajuData)
def api_calculate_saju(user_profile: UserProfile):
    """
    생년월일시를 입력받아 사주팔자를 계산
    """
    try:
        saju = calculate_full_saju(
            user_profile.birth_date,
            user_profile.birth_time
        )
        return saju
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사주 계산 실패: {str(e)}")


@app.post("/api/saju/analyze", response_model=AnalysisResponse)
def api_analyze_saju(request: AnalysisRequest):
    """
    AI 사주 상담 요청
    """
    try:
        # Pydantic v2: model_dump()
        profile_dict = request.user_profile.model_dump()
        # Map name_korean to name for generator compatibility
        profile_dict["name"] = profile_dict.get("name_korean", "")
        
        # [Fix] relation_data 병합
        if request.relation_data:
            profile_dict["relation_data"] = request.relation_data.model_dump()
            
        print(f"DEBUG PROFILE: {profile_dict}") # Debug log
        
        result = generate_fortune(
            profile_dict.get("birth_date", ""),
            profile_dict.get("birth_time", ""),
            request.category,
            profile_dict
        )
        
        return AnalysisResponse(
            status=result["status"],
            category=request.category,
            result=result["fortune"],
            conversation_id=""
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 분석 실패: {str(e)}")


# Mount Static Files (Frontend)
# Must be after API routes to avoid overriding
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
