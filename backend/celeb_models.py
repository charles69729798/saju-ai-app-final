"""
스타 사주 DB 운영을 위한 모델 및 스키마 확장
"""
import sqlite3
import os
from pydantic import BaseModel
from typing import Optional, List

DB_PATH = os.path.join(os.path.dirname(__file__), "saju_knowledge.db")

class CelebSajuModel(BaseModel):
    id: Optional[int] = None
    name: str
    category: str
    rank: int
    birth_date: str
    birth_time: Optional[str] = None
    is_lunar: bool = False
    is_leap: bool = False
    gender: str
    mbti: Optional[str] = None
    is_mbti_estimated: bool = False
    description: Optional[str] = ""
    tags: Optional[str] = ""

def update_celeb_schema():
    """celeb_saju 테이블 생성"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""CREATE TABLE IF NOT EXISTS celeb_saju (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        search_popularity_rank INTEGER,
        birth_date TEXT,
        birth_time TEXT,
        is_lunar INTEGER DEFAULT 0,
        is_leap INTEGER DEFAULT 0,
        gender TEXT,
        mbti TEXT,
        is_mbti_estimated INTEGER DEFAULT 0,
        description TEXT,
        tags TEXT
    )""")
    
    conn.commit()
    conn.close()
    print("✅ celeb_saju 테이블 생성 완료")

def insert_celebs(celebs: List[CelebSajuModel]):
    """스타 데이터 삽입"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    data = [
        (
            item.name, item.category, item.rank, item.birth_date, item.birth_time,
            1 if item.is_lunar else 0, 1 if item.is_leap else 0, item.gender,
            item.mbti, 1 if item.is_mbti_estimated else 0,
            item.description, item.tags
        )
        for item in celebs
    ]
    
    c.executemany("""
        INSERT INTO celeb_saju (
            name, category, search_popularity_rank, birth_date, birth_time,
            is_lunar, is_leap, gender, mbti, is_mbti_estimated, description, tags
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, data)
    
    conn.commit()
    conn.close()
    print(f"✅ {len(celebs)}명의 스타 데이터 삽입 완료")

if __name__ == "__main__":
    update_celeb_schema()
