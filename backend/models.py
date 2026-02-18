"""
Pydantic 데이터 모델 정의
"""
from pydantic import BaseModel
from typing import Optional


class UserProfile(BaseModel):
    """사용자 프로필 입력 데이터"""
    
    # 필수 입력
    birth_date: str  # 생년월일 (YYYY-MM-DD)
    birth_time: str  # 출생 시간 (HH:MM)
    gender: str  # 성별 (남성/여성)
    is_lunar: bool = False  # 음력 여부
    
    # 선택 입력 (하이브리드 분석용)
    name_korean: str = ""  # 한글 이름
    name_hanja: str = ""  # 한자 이름
    
    # [Phase 2] 관계 및 하이브리드 데이터
    mbti: str = ""  # MBTI 유형
    nickname: str = "" # 닉네임 (프라이버시)


class SajuData(BaseModel):
    """사주팔자 계산 결과"""
    year_gan: str
    year_ji: str
    month_gan: str
    month_ji: str
    day_gan: str
    day_ji: str
    hour_gan: str
    hour_ji: str
    
    sol_date: str
    lun_date: str = ""
    
    # [Phase 2] 추가 계산 정보
    ten_gods: dict = {} # 십성 정보


class UserRelation(BaseModel):
    """[Phase 2] 관계 대상 정보"""
    target_name: str = ""
    target_birth_date: str
    target_birth_time: str = "12:00"
    target_mbti: str = ""
    relation_code: str # LOVER, BOSS, FRIEND, PEER, STAR


class AnalysisRequest(BaseModel):
    """AI 상담 요청"""
    user_profile: UserProfile
    category: str  # 분석 카테고리
    
    # [Phase 2] 관계 분석용 추가 데이터
    relation_data: Optional[UserRelation] = None


class AnalysisResponse(BaseModel):
    """AI 상담 응답"""
    status: str
    category: str
    result: str  # Markdown 형식의 AI 답변
    conversation_id: str = ""

