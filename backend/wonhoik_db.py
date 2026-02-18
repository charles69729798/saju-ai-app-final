"""
Won-hoik (Traditional Dictionary) Hanja Stroke Data
- 성명학 원획(原劃) 기준 획수 데이터
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "saju_knowledge.db")

# 원획(原劃) 보정 규칙 (부수 기준)
# 성명학에서는 특정 부수가 변형되었을 때 원형의 획수를 따릅니다.
# 예: 氵(삼수변) -> 水(물 수) 4획으로 계산
WONHOIK_RULES = {
    "氵": 4, # 水
    "忄": 4, # 心
    "扌": 4, # 手
    "犭": 4, # 犬
    "礻": 5, # 示
    "衤": 6, # 衣
    "艹": 6, # 艸
    "辶": 7, # 辵
    "阝": 8, # 邑 (우부방) or 阜 (좌부방) - 위치에 따라 다름
    "王": 5, # 玉 (구슬옥변)
}

# 이름에 자주 쓰이는 한자의 원획 획수 DB (일부 발췌)
# 실제 상용 인명용 한자는 수천 개이나, 핵심 데이터 위주로 구축
WONHOIK_STROKES = {
    "朴": 6,  # 木(4) + 卜(2) -> 원획 6
    "金": 8,
    "李": 7,
    "崔": 11,
    "鄭": 19, # 奠(12) + 邑(7) -> 원획은 15+4? 명확한 옥편 기준 필요
    "姜": 9,
    "趙": 14,
    "尹": 4,
    "張": 11,
    "林": 8,
    "韓": 17,
    "吳": 7,
    "徐": 10,
    "申": 5,
    "權": 22,
    "黃": 12,
    "安": 6,
    "宋": 7,
    "劉": 15,
    "洪": 10, # 氵(4) + 共(6) = 10 (필획은 9)
    "哲": 11, # 扌(4) + 斤(4) + 口(3) = 11 (필획은 10)
    "世": 5,
    "潤": 16, # 氵(4) + 門(8) + 王(4?) -> 15 or 16
    "燦": 17,
    "炫": 9,
    "熙": 13,
    "鉉": 13,
    "廷": 7,
    "準": 14, # 氵(4) + 隹(8) + 十(2) = 14 (필획 13)
}

def init_wonhoik():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # hanja_elements 테이블에 won_strokes 컬럼 추가 (없다면)
    try:
        c.execute("ALTER TABLE hanja_elements ADD COLUMN won_strokes INTEGER")
    except sqlite3.OperationalError:
        pass # 이미 존재함
        
    for hanja, strokes in WONHOIK_STROKES.items():
        c.execute("UPDATE hanja_elements SET won_strokes = ? WHERE hanja = ?", (strokes, hanja))
        # 만약 해당 한자가 테이블에 없으면 새로 삽입 (오행 정보는 일단 None)
        if c.rowcount == 0:
            c.execute("INSERT OR IGNORE INTO hanja_elements (hanja, won_strokes) VALUES (?, ?)", (hanja, strokes))
            
    conn.commit()
    conn.close()
    print("✅ Won-hoik stroke DB initialized.")

def get_won_strokes(hanja_char):
    """특정 한자의 원획 획수를 가져옴"""
    # 1. DB 조회
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT won_strokes FROM hanja_elements WHERE hanja = ?", (hanja_char,)).fetchone()
    conn.close()
    
    if row and row['won_strokes']:
        return row['won_strokes']
    
    # 2. DB에 없을 경우 기본 필획 반환 (임시 - 실제로는 라이브러리 연동 필요)
    # 여기서는 간단히 규칙만 적용해보고 안되면 0 반환
    return 0

if __name__ == "__main__":
    init_wonhoik()
