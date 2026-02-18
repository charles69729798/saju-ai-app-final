"""
사주팔자 계산 엔진
- 년/월/일/시 4주 천간지지 계산
- 십성 도출 (일간 기준)
- 오행 균형 분석
"""

# 천간/지지 배열
STEMS = ["갑","을","병","정","무","기","경","신","임","계"]
BRANCHES = ["자","축","인","묘","진","사","오","미","신","유","술","해"]

# 천간 오행 매핑
STEM_ELEMENT = {"갑":"목","을":"목","병":"화","정":"화","무":"토","기":"토","경":"금","신":"금","임":"수","계":"수"}
STEM_YINYANG = {"갑":"양","을":"음","병":"양","정":"음","무":"양","기":"음","경":"양","신":"음","임":"양","계":"음"}

# 지지 오행 매핑
BRANCH_ELEMENT = {"자":"수","축":"토","인":"목","묘":"목","진":"토","사":"화","오":"화","미":"토","신":"금","유":"금","술":"토","해":"수"}
BRANCH_ANIMAL = {"자":"쥐","축":"소","인":"호랑이","묘":"토끼","진":"용","사":"뱀","오":"말","미":"양","신":"원숭이","유":"닭","술":"개","해":"돼지"}

# 월주 천간 계산 (년간 기준)
MONTH_STEM_BASE = {"갑":2,"을":4,"병":6,"정":8,"무":0,"기":2,"경":4,"신":6,"임":8,"계":0}

# 십성 관계 매핑 (일간 오행 기준 → 타 오행의 십성)
# 비견/겁재, 식신/상관, 편재/정재, 편관/정관, 편인/정인
TEN_GOD_MAP = {
    "목": {"목":"비겁","화":"식상","토":"재성","금":"관성","수":"인성"},
    "화": {"화":"비겁","토":"식상","금":"재성","수":"관성","목":"인성"},
    "토": {"토":"비겁","금":"식상","수":"재성","목":"관성","화":"인성"},
    "금": {"금":"비겁","수":"식상","목":"재성","화":"관성","토":"인성"},
    "수": {"수":"비겁","목":"식상","화":"재성","토":"관성","금":"인성"},
}

# 비겁/식상/재성/관성/인성 → 음양에 따라 세분화
TEN_GOD_DETAIL = {
    "비겁": {"same": "비견", "diff": "겁재"},
    "식상": {"same": "식신", "diff": "상관"},
    "재성": {"same": "편재", "diff": "정재"},
    "관성": {"same": "편관", "diff": "정관"},
    "인성": {"same": "편인", "diff": "정인"},
}


def calculate_year_pillar(year):
    """년주 계산"""
    idx = (year - 4) % 60
    stem = STEMS[idx % 10]
    branch = BRANCHES[idx % 12]
    return stem, branch


def calculate_month_pillar(year, month, is_southern_hemisphere=False):
    """월주 계산 (남반구 계절 보정 포함)"""
    effective_month = month
    if is_southern_hemisphere:
        # 남반구는 계절이 반대이므로 6개월 시차 적용
        effective_month = (month + 6) % 12
        if effective_month == 0: effective_month = 12
        
    year_stem = calculate_year_pillar(year)[0]
    base = MONTH_STEM_BASE[year_stem]
    stem_idx = (base + effective_month - 1) % 10
    branch_idx = (effective_month + 1) % 12  # 인월(1월)=2, 묘월(2월)=3 ...
    return STEMS[stem_idx], BRANCHES[branch_idx]


def calculate_day_pillar(year, month, day, hour=0, use_yajashee=True):
    """일주 계산 (야자시 보정 포함)"""
    from datetime import date, timedelta
    base_date = date(1900, 1, 1)  # 1900.1.1 = 갑자일
    target = date(year, month, day)
    
    # 야자시(23:00 ~ 24:00) 보정: 다음날의 일진을 사용하거나, 
    # 전통 명리 방식에 따라 조율 (여기서는 다음날 일진을 사용하는 방식 적용 가능)
    if use_yajashee and hour >= 23:
        target += timedelta(days=1)
        
    diff = (target - base_date).days
    idx = (diff + 0) % 60
    return STEMS[idx % 10], BRANCHES[idx % 12]


def calculate_hour_pillar(day_stem, hour):
    """시주 계산"""
    # 일간에 따른 시간 천간 기준
    day_stem_idx = STEMS.index(day_stem)
    base = (day_stem_idx % 5) * 2
    
    # 시간 -> 지지 변환 (23~01=자, 01~03=축, ...)
    # 23시 이후는 다음날의 자시로 보기도 함
    hour_branch_idx = ((hour + 1) % 24) // 2
    
    stem_idx = (base + hour_branch_idx) % 10
    return STEMS[stem_idx], BRANCHES[hour_branch_idx]


def get_ten_god(day_stem, target_stem):
    """일간 기준 타 천간의 십성 판별"""
    day_elem = STEM_ELEMENT[day_stem]
    target_elem = STEM_ELEMENT[target_stem]
    day_yy = STEM_YINYANG[day_stem]
    target_yy = STEM_YINYANG[target_stem]
    
    category = TEN_GOD_MAP[day_elem][target_elem]
    
    if day_yy == target_yy:
        return TEN_GOD_DETAIL[category]["same"]
    else:
        return TEN_GOD_DETAIL[category]["diff"]


def analyze_elements(pillars):
    """오행 균형 분석"""
    count = {"목":0, "화":0, "토":0, "금":0, "수":0}
    
    for stem, branch in pillars:
        count[STEM_ELEMENT[stem]] += 1
        count[BRANCH_ELEMENT[branch]] += 1
    
    total = sum(count.values())
    
    # 가장 강한/약한 오행
    strongest = max(count, key=count.get)
    weakest = min(count, key=count.get)
    
    # 균형도
    balance = {}
    for elem, cnt in count.items():
        pct = round(cnt / total * 100)
        if pct >= 30:
            balance[elem] = "과다"
        elif pct >= 20:
            balance[elem] = "적당"
        elif pct >= 10:
            balance[elem] = "약간 부족"
        else:
            balance[elem] = "매우 부족"
    
    return {
        "count": count,
        "strongest": strongest,
        "weakest": weakest,
        "balance": balance,
        "total": total,
    }


def calculate_full_saju(birth_date, birth_time, is_southern_hemisphere=False):
    """전체 사주팔자 계산 (글로벌 옵션 포함)"""
    year, month, day = map(int, birth_date.split("-"))
    hour = int(birth_time.split(":")[0])
    
    year_pillar = calculate_year_pillar(year)
    month_pillar = calculate_month_pillar(year, month, is_southern_hemisphere)
    # 야자시 고려한 일주 계산
    day_pillar = calculate_day_pillar(year, month, day, hour)
    hour_pillar = calculate_hour_pillar(day_pillar[0], hour)
    
    pillars = [year_pillar, month_pillar, day_pillar, hour_pillar]
    
    # 일간 (나의 본성)
    day_stem = day_pillar[0]
    
    # 십성 분석
    ten_gods_result = {}
    for i, (stem, branch) in enumerate(pillars):
        pillar_name = ["년주","월주","일주","시주"][i]
        god = get_ten_god(day_stem, stem)
        if i == 2:  # 일주 천간은 자기 자신
            god = "일간(나)"
        ten_gods_result[pillar_name] = god
    
    # 십성 빈도 계산
    god_count = {}
    for pillar_name, god in ten_gods_result.items():
        if god != "일간(나)":
            god_count[god] = god_count.get(god, 0) + 1
    
    # 오행 분석
    element_analysis = analyze_elements(pillars)
    
    # 띠
    animal = BRANCH_ANIMAL[year_pillar[1]]
    
    # 사주 텍스트 생성
    location_tag = " [남반구 보정]" if is_southern_hemisphere else ""
    saju_text = f"{year_pillar[0]}{year_pillar[1]}년 {month_pillar[0]}{month_pillar[1]}월 {day_pillar[0]}{day_pillar[1]}일 {hour_pillar[0]}{hour_pillar[1]}시{location_tag}"
    
    return {
        "pillars": {
            "year": {"stem": year_pillar[0], "branch": year_pillar[1]},
            "month": {"stem": month_pillar[0], "branch": month_pillar[1]},
            "day": {"stem": day_pillar[0], "branch": day_pillar[1]},
            "hour": {"stem": hour_pillar[0], "branch": hour_pillar[1]},
        },
        "day_stem": day_stem,
        "day_stem_element": STEM_ELEMENT[day_stem],
        "day_stem_yinyang": STEM_YINYANG[day_stem],
        "animal": animal,
        "ten_gods": ten_gods_result,
        "god_count": god_count,
        "elements": element_analysis,
        "saju_text": saju_text,
        "is_southern_hemisphere": is_southern_hemisphere
    }


if __name__ == "__main__":
    # 테스트: 남반구 출생자 (예: 호주 시드니 1월생 -> 북반구 7월의 기운)
    print("--- 북반구 1월 ---")
    res_n = calculate_full_saju("2000-01-10", "12:00", False)
    print(res_n['saju_text'])
    
    print("\n--- 남반구 1월 (보정) ---")
    res_s = calculate_full_saju("2000-01-10", "12:00", True)
    print(res_s['saju_text'])

