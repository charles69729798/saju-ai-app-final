"""
사주 지식 SQLite 데이터베이스 (Full Version)
- 10+개 테이블, 현대적 어조 및 고전 지식 통합
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "saju_knowledge.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def update_schema():
    """스키마 업데이트 (신규 테이블 등)"""
    from celeb_models import update_celeb_schema
    update_celeb_schema()

def init_db():
    """DB 초기화 및 데이터 삽입"""
    if os.path.exists(DB_PATH):
        # 만약 테이블이 부족하다면 여기서 추가 로직 수행 (생략 가능)
        return
    
    conn = get_db()
    c = conn.cursor()
    
    # ── 1. 천간 테이블 ──
    c.execute("""CREATE TABLE heavenly_stems (
        id INTEGER PRIMARY KEY, name TEXT, hanja TEXT,
        element TEXT, yin_yang TEXT, color TEXT, direction TEXT,
        season TEXT, personality TEXT, body_part TEXT, modern_summary TEXT
    )""")
    
    stems = [
        (1,"갑","甲","목","양","청색","동","봄","곧고 정직하며 리더십이 강한 큰 나무의 기운. 개척 정신과 진취적 성격을 지님","머리/간", "성장을 주도하는 '갓생' 메이커"),
        (2,"을","乙","목","음","연두","동","봄","유연하고 적응력이 뛰어난 풀과 덩굴의 기운. 온화하지만 끈질긴 생명력","목/간", "유연함 속에 감춰진 '외유내강' 프로"),
        (3,"병","丙","화","양","적색","남","여름","태양처럼 밝고 화려한 기운. 열정적이고 외향적이며 남을 비추는 성격","눈/심장", "세상을 비추는 서치라이트, '본투비 인플루언서'"),
        (4,"정","丁","화","음","분홍","남","여름","촛불처럼 은은하고 섬세한 기운. 내면의 열정이 강하고 집중력이 뛰어남","혀/심장", "은은하게 타오르는 '내면의 불꽃'"),
        (5,"무","戊","토","양","황색","중앙","환절기","큰 산처럼 듬직하고 포용력 있는 기운. 신뢰감을 주며 중심을 잡아줌","코/위장", "흔들리지 않는 멘탈, '든든한 기둥'"),
        (6,"기","己","토","음","갈색","중앙","환절기","기름진 밭처럼 만물을 품는 기운. 꼼꼼하고 실속 있으며 내실을 다짐","입술/비장", "디테일 끝판왕, '세심한 가드너'"),
        (7,"경","庚","금","양","백색","서","가을","강철처럼 단단하고 결단력 있는 기운. 의리 있고 정의감이 강함","폐/대장", "확실한 결단력, '스마트한 해결사'"),
        (8,"신","辛","금","음","은색","서","가을","보석처럼 섬세하고 예리한 기운. 심미안이 뛰어나고 완벽주의 성향","폐/피부", "섬세한 감각, '프리미엄 보석'"),
        (9,"임","壬","수","양","흑색","북","겨울","큰 바다처럼 넓고 깊은 기운. 지혜롭고 포용적이며 자유로운 영혼","신장/귀", "무한한 가능성, '지혜의 바다'"),
        (10,"계","癸","수","음","남색","북","겨울","이슬비처럼 부드럽고 촉촉한 기운. 직감과 영감이 뛰어나고 감성적","신장/방광", "직관과 감성, '유연한 물결'"),
    ]
    c.executemany("INSERT INTO heavenly_stems VALUES (?,?,?,?,?,?,?,?,?,?,?)", stems)
    
    # ── 2. 지지 테이블 ──
    c.execute("""CREATE TABLE earthly_branches (
        id INTEGER PRIMARY KEY, name TEXT, hanja TEXT,
        element TEXT, yin_yang TEXT, animal TEXT,
        month INTEGER, hour_start INTEGER, hour_end INTEGER,
        season TEXT, personality TEXT
    )""")
    
    branches = [
        (1,"자","子","수","양","쥐",11,23,1,"겨울","총명하고 재치 있으며 사교적. 밤의 기운으로 내면이 깊고 비밀이 많음"),
        (2,"축","丑","토","음","소",12,1,3,"겨울","우직하고 성실하며 인내력이 강함. 느리지만 꾸준히 목표를 향해 나아감"),
        (3,"인","寅","목","양","호랑이",1,3,5,"봄","용맹하고 진취적이며 리더십이 강함. 모험을 즐기고 도전 정신이 왕성"),
        (4,"묘","卯","목","음","토끼",2,5,7,"봄","온화하고 예술적 감각이 뛰어남. 사교적이지만 내면이 여린 편"),
        (5,"진","辰","토","양","용",3,7,9,"봄","야망이 크고 카리스마가 있음. 변화무쌍하고 예측하기 어려운 독특한 매력"),
        (6,"사","巳","화","음","뱀",4,9,11,"여름","지혜롭고 관찰력이 예리함. 직감이 뛰어나고 전략적 사고를 잘 함"),
        (7,"오","午","화","양","말",5,11,13,"여름","활동적이고 열정적이며 에너지가 넘침. 화려하고 주목받는 것을 좋아함"),
        (8,"미","未","토","음","양",6,13,15,"여름","온순하고 헌신적이며 예술적 감각이 있음. 가정과 평화를 중시"),
        (9,"신","申","금","양","원숭이",7,15,17,"가을","영리하고 재치 있으며 임기응변에 능함. 다재다능하고 호기심이 왕성"),
        (10,"유","酉","금","음","닭",8,17,19,"가을","꼼꼼하고 완벽주의적이며 시간 관념이 철저. 자기 표현이 강하고 솔직"),
        (11,"술","戌","토","양","개",9,19,21,"가을","충직하고 의리 있으며 정의감이 강함. 경계심이 있지만 한번 믿으면 끝까지"),
        (12,"해","亥","수","음","돼지",10,21,23,"겨울","낙천적이고 너그러우며 복이 많음. 순수하고 솔직하며 배려심이 깊음"),
    ]
    c.executemany("INSERT INTO earthly_branches VALUES (?,?,?,?,?,?,?,?,?,?,?)", branches)
    
    # ── 3. 오행 테이블 ──
    c.execute("""CREATE TABLE five_elements (
        id INTEGER PRIMARY KEY, name TEXT, hanja TEXT,
        generates TEXT, controls TEXT, generated_by TEXT, controlled_by TEXT,
        body_organ TEXT, emotion TEXT, taste TEXT, number TEXT
    )""")
    
    elements = [
        (1,"목","木","화","토","수","금","간/담","분노→추진력","신맛","3, 8"),
        (2,"화","火","토","금","목","수","심장/소장","기쁨→열정","쓴맛","2, 7"),
        (3,"토","土","금","수","화","목","위장/비장","사려→안정","단맛","5, 10"),
        (4,"금","金","수","목","토","화","폐/대장","슬픔→결단","매운맛","4, 9"),
        (5,"수","水","목","화","금","토","신장/방광","두려움→지혜","짠맛","1, 6"),
    ]
    c.executemany("INSERT INTO five_elements VALUES (?,?,?,?,?,?,?,?,?,?,?)", elements)

    # ── 4. 십성 테이블 ──
    c.execute("""CREATE TABLE ten_gods (
        id INTEGER PRIMARY KEY, name TEXT, hanja TEXT,
        category TEXT, keyword TEXT, personality TEXT,
        career TEXT, wealth TEXT, love TEXT, health TEXT,
        modern_summary TEXT
    )""")
    
    ten_gods_data = [
        (1,"비견","比肩","비겁","독립/경쟁/자존심",
         "주관이 뚜렷하고 독립심이 강합니다. 자기 영역을 확고히 지키며 경쟁에서 물러서지 않는 강인한 성격입니다.",
         "프리랜서, 1인 창업, 전문직이 적합합니다.", "본인의 기술로 직접 버는 재물운입니다.",
         "친구 같은 편안한 연애를 선호합니다.", "스트레스 관리와 근육 건강 주의.", "독립적인 '마이웨이' 리더"),
        (2,"겁재","劫財","비겁","경쟁/욕심/추진력",
         "승부욕이 매우 강하고 목표를 위해 과감하게 행동합니다. 타인에게 지기 싫어하며 독점욕이 강합니다.",
         "영업, 투자, 경쟁이 심한 분야가 적합합니다.", "한꺼번에 큰 재물을 얻거나 잃을 수 있는 굴곡이 있습니다.",
         "열정적이지만 소유욕이 강한 연애 스타일입니다.", "심장 및 갑작스러운 사고 주의.", "불꽃 같은 '승부사'"),
        (3,"식신","食神","식상","표현/여유/창의성",
         "온화하고 낙천적이며 표현력이 좋습니다. 연구하고 창작하는 것을 즐기며 의식주 복이 타고났습니다.",
         "연구원, 예술가, 교육자, 요식업이 적합합니다.", "꾸준하고 안정적인 소득원이 따릅니다.",
         "다정다감하고 헌신적인 사랑을 합니다.", "소화기 및 비만 관리 주의.", "즐거움을 찾는 '예술가'"),
        (4,"상관","傷官","식상","파격/천재성/비판",
         "두뇌 회전이 빠르고 기존의 틀을 깨는 혁신적인 성향입니다. 언변이 뛰어나고 예술적 감각이 독보적입니다.",
         "기획, 광고, 비평가, 연예인이 적합합니다.", "아이디어와 재치로 큰 부를 창출합니다.",
         "화려하고 드라마틱한 연애를 꿈꿉니다.", "호흡기 및 신경계 질환 주의.", "틀을 깨는 '아이디어 뱅크'"),
        (5,"편재","偏財","재성","활동/투기/유통",
         "스케일이 크고 활동 범위가 넓습니다. 고정된 소득보다 유동적인 큰 재물을 추구하며 모험을 즐깁니다.",
         "사업가, 무역, 금융 투자가 적합합니다.", "한 방의 재물운이 있으며 돈의 흐름을 잘 읽습니다.",
         "사교적이고 이성에게 호감을 잘 얻는 타입입니다.", "간 기능 및 피로 완화 주의.", "영역을 넓히는 '사업가'"),
        (6,"정재","正財","재성","성실/신용/치밀",
         "꼼꼼하고 실속 있으며 경제 관념이 철저합니다. 성실함을 바탕으로 신용을 쌓으며 안정적인 삶을 추구합니다.",
         "금융, 회계, 관리직, 공무원이 적합합니다.", "차곡차곡 쌓이는 안정적인 자산 형성이 강점입니다.",
         "신중하고 안정적인 결혼 생활에 최적화된 성격입니다.", "위장 및 피부 건강 관리 주의.", "내실 있는 '자산가'"),
        (7,"편관","偏官","관성","카리스마/책임/권력",
         "강한 리더십과 책임감을 가진 전형적인 우두머리 기질입니다. 어려움을 뚫고 나가는 힘이 대단합니다.",
         "군/경, 법조인, 고위직 리더가 적합합니다.", "명예를 통해 재물이 따라오는 유형입니다.",
         "카리스마 있고 상대를 이끄는 연애 스타일입니다.", "심혈관계 및 고혈압 주의.", "지휘하는 '카리스마 리더'"),
        (8,"정관","正官","관성","명예/질서/모범",
         "책임감이 강하고 원칙을 준수하는 모범생 타입입니다. 예의 바르고 주변의 신뢰를 한몸에 받습니다.",
         "공무원, 대기업 임원, 학자가 적합합니다.", "안정적인 급여와 직위를 통한 재물이 보장됩니다.",
         "진지하고 책임감 있는 결혼 생활을 추구합니다.", "경직된 몸과 어깨 결림 관리 주의.", "정도(正道)를 걷는 '바른 생활 리더'"),
        (9,"편인","偏인","인성","직감/특수기술/영감",
         "남다른 통찰력과 직감을 가진 전략가입니다. 신비로운 분야나 특수 기술에 능하며 생각이 깊습니다.",
         "AI 전문가, 심리상담, 점술, 특수 연구직이 적합합니다.", "독창적인 아이디어나 기술로 돈을 법니다.",
         "정신적 교감을 중시하며 신비로운 인연이 많습니다.", "불면증 및 신경 예민 관리 주의.", "영감을 가진 '전략가'"),
        (10,"정인","正印","인성","지혜/학문/자격",
         "학구적이고 인자하며 타인을 가르치고 돕는 것을 좋아합니다. 자격증과 학위운이 매우 좋습니다.",
         "교수, 작가, 멘토, 공인 자격직이 적합합니다.", "문서(부동산, 계약)를 통한 재물운이 유리합니다.",
         "따뜻하고 모성/부성애가 넘치는 연애를 합니다.", "두뇌 피로와 시력 저하 주의.", "지혜로운 '멘토'"),
    ]
    c.executemany("INSERT INTO ten_gods VALUES (?,?,?,?,?,?,?,?,?,?,?)", ten_gods_data)
    
    # ── 5. 혈액형 매핑 ──
    c.execute("""CREATE TABLE blood_type_mapping (
        id INTEGER PRIMARY KEY, genotype TEXT, display_name TEXT, 
        personality TEXT, career TEXT, wealth TEXT, love TEXT, saju_god TEXT
    )""")
    
    blood_data = [
        (1, "A", "신중한 A형", "섬세하고 책임감이 강하며 사회적 규범을 준수합니다.", "공공기관, 대기업 관리직", "성실한 저축 기반 자산 형성", "배려하고 신중한 연애", "정관"),
        (2, "B", "자유로운 B형", "독립적이고 창의적이며 본인만의 색깔이 뚜렷합니다.", "예술, 기술, 전문직", "아이디어 기반의 소득", "열정적이고 솔직한 사랑", "상관"),
        (3, "O", "열정적인 O형", "목표 지향적이고 리더십이 있으며 사교적입니다.", "영업, 기획, 사업가", "적극적 투자를 통한 재물 증식", "주도적이고 활기찬 연애", "편재"),
        (4, "AB", "이성적인 AB형", "분석적이고 합리적이며 공과 사가 분명합니다.", "연구, 비평, 전략 수립", "치밀한 계획에 따른 재테크", "담백하고 지적인 교감", "편인"),
    ]
    c.executemany("INSERT INTO blood_type_mapping VALUES (?,?,?,?,?,?,?,?)", blood_data)
    
    # ── 6. MBTI 매핑 ──
    c.execute("""CREATE TABLE mbti_mapping (
        id INTEGER PRIMARY KEY, mbti TEXT, title TEXT, 
        personality TEXT, career_advice TEXT, saju_god TEXT
    )""")
    
    mbti_data = [
        (1, "INFJ", "통찰력 있는 선지자", "내면의 신념이 강하며 사람들의 잠재력을 끌어내려 노력합니다.", "상담, 교육, 문학", "정인"),
        (2, "ENFP", "재기발랄한 활동가", "자유로운 영혼이며 열정적으로 새로운 가능성을 개척합니다.", "마케팅, 홍보, 예술", "상관"),
        (3, "INTJ", "용의주도한 전략가", "미래를 내다보는 체계적인 분석가로 독립심이 강합니다.", "IT 보안, 전략 기획, 연구", "편인"),
        (4, "ESFJ", "사교적인 외교관", "사람들을 잘 돌보고 질서 있는 환경에서 협력하는 것을 즐깁니다.", "서비스업, 인사 관리, 교육", "정재"),
        # (기타 MBTI 생략, 필요 시 추가 삽입 지원 가능)
    ]
    c.executemany("INSERT INTO mbti_mapping VALUES (?,?,?,?,?,?)", mbti_data)

    # ── 7. 고전 지식 (Classical Wisdom) ──
    c.execute("""CREATE TABLE classical_wisdom (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        target_name TEXT,
        source TEXT,
        original_text TEXT,
        modern_interpretation TEXT
    )""")

    wisdom_data = [
        ("ten_gods", "비견", "명리정종", "比肩者, 兄弟之象. 身旺遇之, 必主爭財.", "비견은 형제의 형상이니, 몸이 왕성한 자가 이를 만나면 필히 재물을 다투게 된다. 현대적으로는 독자적인 전문성을 길러야 함을 뜻합니다."),
        ("elements", "목", "적천수", "甲木參天, 脫胎要火.", "갑목이 높이 솟으니 꽃을 피우려면 불(火)의 도움이 절실하다. 성장을 위해 적절한 발산이 필요함을 의미합니다."),
        ("elements", "화", "적천수", "丙火猛烈, 欺霜侮雪.", "병화는 타오르는 불길 같아서 서리와 눈을 업신여긴다. 강한 열정과 카리스마의 근원이 됩니다."),
    ]
    c.executemany("INSERT INTO classical_wisdom (category, target_name, source, original_text, modern_interpretation) VALUES (?,?,?,?,?)", wisdom_data)

    # ── 8. 60갑자 일주 보강 ──
    c.execute("""CREATE TABLE pillars_60_ganji (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        career_strategy TEXT,
        wealth_strategy TEXT,
        love_strategy TEXT,
        general_personality TEXT
    )""")

    pillars = [
        ("갑자", "방송, 교육, IT 기획. 소통형 조직이 유리.", "문서 중심의 자산 형성. 지적 재산권 수익 최적화.", "정신적 공감 중시. 친구 같은 배우자운.", "총명하고 깔끔하며 본인만의 세계가 뚜렷함."),
        ("갑술", "부동산, 전문직, 종교/철학. 성실한 커리어.", "실물 자산(땅, 건물) 중심의 안정적 투자.", "헌신적이지만 가끔 독단적일 수 있음.", "산 위의 소나무. 듬직하고 기예가 많음."),
        # (테스트용 필수 일주 약 10+개 보강)
    ]
    c.executemany("INSERT OR REPLACE INTO pillars_60_ganji (name, career_strategy, wealth_strategy, love_strategy, general_personality) VALUES (?,?,?,?,?)", pillars)

    # ── 9. 지명/한자 오행 보강 ──
    c.execute("""CREATE TABLE IF NOT EXISTS hanja_elements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hanja TEXT UNIQUE,
        name TEXT,
        element TEXT,
        won_strokes INTEGER
    )""")

    # ── 10. NotebookLM Cache ──
    c.execute("""CREATE TABLE IF NOT EXISTS notebooklm_cache (
        query_hash TEXT PRIMARY KEY,
        prompt TEXT,
        response TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    conn.commit()
    conn.close()
    print(f"✅ DB Full Initialized: {DB_PATH}")

def query_heavenly_stem(name):
    conn = get_db()
    row = conn.execute("SELECT * FROM heavenly_stems WHERE name=?", (name,)).fetchone()
    conn.close()
    return dict(row) if row else None

def query_earthly_branch(name):
    conn = get_db()
    row = conn.execute("SELECT * FROM earthly_branches WHERE name=?", (name,)).fetchone()
    conn.close()
    return dict(row) if row else None

def query_five_element(name):
    conn = get_db()
    row = conn.execute("SELECT * FROM five_elements WHERE name=?", (name,)).fetchone()
    conn.close()
    return dict(row) if row else None

def query_ten_god(name):
    conn = get_db()
    row = conn.execute("SELECT * FROM ten_gods WHERE name=?", (name,)).fetchone()
    conn.close()
    return dict(row) if row else None

def query_classical_wisdom(category, name):
    conn = get_db()
    row = conn.execute("SELECT * FROM classical_wisdom WHERE category=? AND target_name=?", (category, name)).fetchone()
    conn.close()
    return dict(row) if row else None

def query_pillar_60(name):
    conn = get_db()
    row = conn.execute("SELECT * FROM pillars_60_ganji WHERE name=?", (name,)).fetchone()
    conn.close()
    return dict(row) if row else None

def query_blood_type(genotype):
    target = genotype
    if genotype in ["AA", "AO"]: target = "A"
    if genotype in ["BB", "BO"]: target = "B"
    conn = get_db()
    row = conn.execute("SELECT * FROM blood_type_mapping WHERE genotype=?", (target,)).fetchone()
    conn.close()
    return dict(row) if row else None

def query_mbti(mbti_type):
    conn = get_db()
    row = conn.execute("SELECT * FROM mbti_mapping WHERE mbti=?", (mbti_type,)).fetchone()
    conn.close()
    return dict(row) if row else None

def query_celebs(category=None, search=None):
    conn = get_db()
    query = "SELECT * FROM celeb_saju WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if search:
        query += " AND name LIKE ?"
        params.append(f"%{search}%")
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def query_celeb_by_id(celeb_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM celeb_saju WHERE id = ?", (celeb_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def query_hanja_element(hanja_char):
    conn = get_db()
    row = conn.execute("SELECT * FROM hanja_elements WHERE hanja=?", (hanja_char,)).fetchone()
    conn.close()
    return dict(row) if row else None

def query_interpretation_context(category, key, context_code):
    """
    [Phase 2] 관계 해석 컨텍스트 조회 (Mock)
    """
    # Simple Mock Logic until DB table is ready
    return {
        "advice_text": f"상대방의 {key} 기운이 당신에게 강렬한 인상을 남깁니다. 서로의 차이를 인정하면 더욱 깊은 관계로 발전할 수 있습니다.",
        "price_to_unlock": 500,
        "is_positive": 1
    }

def get_notebooklm_cache(query_hash):
    conn = get_db()
    try:
        row = conn.execute("SELECT * FROM notebooklm_cache WHERE query_hash=?", (query_hash,)).fetchone()
        return dict(row) if row else None
    except sqlite3.OperationalError:
        return None
    finally:
        conn.close()

def save_notebooklm_cache(query_hash, prompt, response):
    conn = get_db()
    try:
        conn.execute("CREATE TABLE IF NOT EXISTS notebooklm_cache (query_hash TEXT PRIMARY KEY, prompt TEXT, response TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        conn.execute("INSERT OR REPLACE INTO notebooklm_cache (query_hash, prompt, response) VALUES (?, ?, ?)",
                     (query_hash, prompt, response))
        conn.commit()
    finally:
        conn.close()

# Aliases for backward compatibility
query_stem = query_heavenly_stem
query_branch = query_earthly_branch
query_element = query_five_element

if __name__ == "__main__":
    init_db()
