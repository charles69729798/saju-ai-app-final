"""
운세 조립 엔진 (Fortune Generator)
- DB 블록을 조합하여 카테고리별 6000자 운세 생성
- AI 없이 순수 DB 기반으로 동작
- 혈액형/MBTI 맥락적 교차분석 통합
"""
from saju_db import query_stem, query_branch, query_ten_god, query_element, query_blood_type, query_mbti, query_heavenly_stem
from saju_calculator import calculate_full_saju, STEM_ELEMENT, BRANCH_ELEMENT, BRANCH_ANIMAL
from fortune_blocks import (
    build_contextual_cross_analysis,
    build_life_stages,
    build_daily_practice,
    # gen_blood_category removed in Phase 8b
    gen_mbti_category,
    build_element_deep_analysis,
    build_ten_god_synergy,
    build_seasonal_fortune,
    build_relationship_dynamics,
    build_classical_wisdom_section,
    build_wealth_strategy,
    build_career_pathmap,
    build_love_dynamics,
    build_name_analysis_block,
)
import datetime


def get_dominant_god(god_count):
    """가장 강한 십성 반환"""
    if not god_count:
        return "비견"
    return max(god_count, key=god_count.get)


def generate_element_advice(weakest, strongest):
    """오행 균형 기반 개운법"""
    advice_map = {
        "목": {"color": "청색/녹색", "direction": "동쪽", "number": "3, 8", "food": "신맛 음식(레몬, 유자, 식초)", "activity": "산림욕, 등산, 원예"},
        "화": {"color": "빨강/보라", "direction": "남쪽", "number": "2, 7", "food": "쓴맛 음식(커피, 녹차, 씀바귀)", "activity": "햇볕 쬐기, 캠핑, 요리"},
        "토": {"color": "노랑/갈색", "direction": "중앙", "number": "5, 10", "food": "단맛 음식(꿀, 고구마, 대추)", "activity": "도자기, 텃밭 가꾸기, 명상"},
        "금": {"color": "흰색/은색", "direction": "서쪽", "number": "4, 9", "food": "매운맛 음식(고추, 생강, 마늘)", "activity": "호흡 운동, 노래, 금속 공예"},
        "수": {"color": "검정/남색", "direction": "북쪽", "number": "1, 6", "food": "짠맛 음식(해산물, 미역, 김)", "activity": "수영, 온천, 독서, 명상"},
    }
    return advice_map.get(weakest, advice_map["목"])


def get_yearly_fortune(day_stem_element, year=2026):
    """연운 분석"""
    # 2026년 = 병오년 (화기운 강한 해)
    year_element = "화"  # 2026 병오년
    
    relation_map = {
        ("목","화"): ("식상운", "당신의 재능과 표현력이 빛나는 해입니다. 새로운 기술을 배우거나 창작 활동을 시작하면 큰 성과를 얻을 수 있습니다. 식신생재(食神生財)의 흐름으로 기술이 곧 돈이 되는 시기입니다."),
        ("화","화"): ("비겁운", "비슷한 목표를 가진 동료나 경쟁자가 많아지는 해입니다. 협력하면 시너지가 나지만, 독자적인 영역을 확보하는 것도 중요합니다."),
        ("토","화"): ("인성운", "학업운과 자격증운이 좋은 해입니다. 새로운 공부를 시작하거나 자기계발에 투자하면 큰 성과가 있습니다. 어머니나 스승의 도움이 있을 수 있습니다."),
        ("금","화"): ("관성운", "직장이나 사회적 위치에 변화가 생기는 해입니다. 승진이나 새로운 직책을 맡을 수 있지만, 그만큼 책임과 압박도 증가합니다."),
        ("수","화"): ("재성운", "재물운이 활성화되는 해입니다. 새로운 수입원이 생기거나 투자 기회가 찾아올 수 있습니다. 다만 지출도 늘어날 수 있으니 균형있는 관리가 필요합니다."),
    }
    
    key = (day_stem_element, year_element)
    return relation_map.get(key, ("운행중", "올해는 안정적으로 현재의 상태를 유지하며 내실을 다지는 것이 좋습니다."))


def get_monthly_tips(day_stem_element):
    """월별 운세 팁"""
    tips = {
        "목": [
            ("1~2월", "봄의 기운이 시작되어 의욕이 샘솟는 시기. 새로운 계획 수립에 좋습니다."),
            ("3~4월", "본격적으로 활동력이 높아집니다. 중요한 프로젝트를 시작하기 최적의 시기."),
            ("5~6월", "화기운이 강해져 표현력이 빛납니다. 프레젠테이션이나 면접에 유리."),
            ("7~8월", "토기운과 만나 안정을 찾는 시기. 기반을 다지고 재정을 점검하세요."),
            ("9~10월", "금기운에 의해 도전받는 시기. 건강 관리에 신경 쓰고 무리하지 마세요."),
            ("11~12월", "수기운으로 에너지가 충전됩니다. 내년을 위한 준비와 휴식의 시간."),
        ],
        "화": [
            ("1~2월", "수기운이 강한 시기라 에너지가 억눌릴 수 있습니다. 내면의 힘을 기르세요."),
            ("3~4월", "목기운의 도움으로 활력이 살아납니다. 인맥을 넓히기 좋은 시기."),
            ("5~6월", "본격적으로 빛나는 시기! 자신감을 가지고 적극적으로 활동하세요."),
            ("7~8월", "토기운으로 성과가 나타나기 시작합니다. 노력의 결실을 거두세요."),
            ("9~10월", "금기운과 만나 재물운이 활성화됩니다. 투자나 거래에 좋은 시기."),
            ("11~12월", "수기운의 도전을 받습니다. 건강과 체력 관리가 중요한 시기."),
        ],
        "토": [
            ("1~2월", "수기운에 의해 내부 점검이 필요한 시기. 재정 상태를 꼼꼼히 확인하세요."),
            ("3~4월", "목기운의 도전으로 변화의 바람이 붑니다. 유연하게 대처하세요."),
            ("5~6월", "화기운의 지원을 받아 에너지가 충전됩니다. 학업운, 자격증운이 좋습니다."),
            ("7~8월", "토기운이 강해져 안정감이 극대화됩니다. 부동산 관련 일에 유리."),
            ("9~10월", "금기운으로 성과와 수확의 시기. 그동안의 노력이 결실을 맺습니다."),
            ("11~12월", "수기운에 주의하며 건강을 챙기세요. 소화기 관리가 특히 중요합니다."),
        ],
        "금": [
            ("1~2월", "수기운으로 지혜가 깊어지는 시기. 전략적 사고로 미래를 설계하세요."),
            ("3~4월", "목기운에 에너지를 쏟는 시기. 재물 지출이 늘 수 있으니 계획적으로."),
            ("5~6월", "화기운의 도전을 받습니다. 과도한 업무와 스트레스를 관리하세요."),
            ("7~8월", "토기운의 지원으로 안정을 되찾습니다. 든든한 후원자가 나타날 수 있습니다."),
            ("9~10월", "금기운이 극대화! 본인의 능력이 빛나는 최고의 시기입니다."),
            ("11~12월", "수기운으로 에너지를 방출합니다. 후배 양성이나 기부에 좋은 시기."),
        ],
        "수": [
            ("1~2월", "수기운이 극대화되어 지혜와 통찰이 깊어집니다. 중요한 결정에 좋은 시기."),
            ("3~4월", "목기운으로 에너지를 쏟아냅니다. 새로운 프로젝트 시작에 적합합니다."),
            ("5~6월", "화기운에 재물운이 활성화됩니다. 적극적인 영업과 거래가 유리합니다."),
            ("7~8월", "토기운의 압박을 받을 수 있습니다. 건강과 인간관계에 주의하세요."),
            ("9~10월", "금기운의 지원으로 학업운과 문서운이 좋습니다. 계약이나 시험에 유리."),
            ("11~12월", "수기운으로 돌아오는 시기. 에너지를 재충전하고 내년을 준비하세요."),
        ],
    }
    return tips.get(day_stem_element, tips["목"])


# ────────────────────────────────
# Style Transformer & Master Context
# ────────────────────────────────

def _apply_modern_style(text):
    """MZ-Premium 스타일 변환기: 보수적인 문체를 세련된 코칭 어조로 바꿉니다."""
    replacements = {
        "기운이 쇠퇴함": "에너지를 재충전하고 다음 스테이지를 준비하는 시기",
        "불공평한 대우": "나의 가치를 정당하게 인정받기 위한 전략적 조율",
        "무모해질 수 있습니다": "과감한 추진력이 자칫 리스크로 이어지지 않게 밸런스를 잡아야 할 때",
        "천직입니다": "당신의 잠재력이 가장 빛을 발할 수 있는 '커리어 홈그라운드'",
        "재물이 따라옵니다": "당신의 전문성이 곧 '수익 극대화'로 이어지는 선순환 구조",
        "운세가 불길함": "잠시 속도를 늦추고 내실을 다져야 하는 '멘탈 관리' 구간",
        "큰 성과가 있습니다": "눈에 띄는 '업적(Achievement)'을 달성하고 영향력을 높일 기회",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def _generate_hybrid_insight(saju, mbti_type):
    """사주 십신(十神)과 MBTI 데이터를 결합한 하이브리드 분석 리포트"""
    if not mbti_type: return ""
    
    dominant = get_dominant_god(saju["god_count"])
    mbti = mbti_type.upper()
    
    # 1. 태도 매칭 (I/E vs 비겁/식상)
    attitude = "외향적 에너지" if mbti.startswith("E") else "내향적 깊이"
    
    # 2. 핵심 시너지 조합
    synergy_map = {
        ("편관", "INFP"): "섬세한 이상주의 뒤에 숨겨진 '완벽주의적 책임감'. 스스로를 엄격하게 관리하며 비전(Vision)을 현실화하는 힘이 있습니다.",
        ("상관", "ENTP"): "폭발적인 창의성과 파격적인 실행력. 기존의 틀을 깨고 새로운 트렌드를 만드는 '트렌드 세터(Trend Setter)'의 전형입니다.",
        ("정인", "INFJ"): "깊은 통찰력과 지혜를 갖춘 '영적인 멘토'. 주변 사람들의 잠재력을 끌어내고 정신적인 안식처가 되어주는 기운입니다.",
        ("정재", "ISTJ"): "빈틈없는 치밀함과 압도적인 신뢰도. 주어진 시스템을 가장 완벽하게 운영하며 리스크 제로(Zero Risk)를 지향하는 마스터입니다.",
        ("편재", "ESTP"): "광활한 활동 반경과 본능적인 기회 포착 능력. 복잡한 시장 상황에서도 수익 모델을 찾아내는 '타고난 투자가' 기질입니다.",
    }
    
    insight = synergy_map.get((dominant, mbti), f"{mbti}의 성향과 {dominant}의 기질이 만나 독특한 행동 패턴을 만듭니다. {attitude}를 바탕으로 본인만의 세계를 구축하고 있습니다.")
    
    return f"\n\n### 🧬 DNA Hybrid Insight (Saju x MBTI)\n- **Hybrid Type**: {dominant} + {mbti}\n- **Analysis**: {insight}\n"


def _get_master_context(saju, user_profile):
    """
    모든 카테고리 기저에 흐르는 '종합 전략'을 도출합니다.
    논리적 정합성(Consistency)의 핵심.
    """
    dominant = get_dominant_god(saju["god_count"])
    weakest = saju["elements"]["weakest"]
    strongest = saju["elements"]["strongest"]
    relation_mode = user_profile.get("relation_type", "lover") # lover / boss
    
    # [Phase 8b] 오행-십성 논리 모순 해결 (Reconciliation)
    bridge_advice = _reconcile_logic(dominant, weakest, strongest, saju["day_stem_element"])
    
    # 2026년 환경 context
    env_theme = "강렬한 화(火)의 에너지와 변화의 해"
    
    # 모드에 따른 전략 차별화
    if relation_mode == "boss":
        strategy = f"비즈니스 현장에서의 '{dominant}'적 리더십 발휘"
        focus = "성과 창출 및 전략적 영향력"
    else:
        strategy = f"관계 속에서 '{dominant}'의 매력을 발산하는 소통법"
        focus = "감정적 교감 및 케미스트리"
    
    return {
        "dominant_god": dominant,
        "weakest_element": weakest,
        "strongest_element": strongest,
        "env_theme": env_theme,
        "master_strategy": f"{strategy} ({bridge_advice})",
        "focus": focus,
        "mode": relation_mode,
        "modern_vibe": "Premium AI Coach"
    }

def _reconcile_logic(dominant, weakest, strongest, day_elem, category="전체"):
    """오행과 십성 간의 조언 충돌을 해결하는 브릿지 로직"""
    # 십성-오행 매핑 및 상황별 조언 생성
    # 카테고리(category) 정보를 추가로 사용하여 맥락에 맞는 브릿지 전략 도출
    
    reconciliation_options = {
        "관성_과다": [
            f"사회적 책임({dominant})이 무거워질 수 있으니, {weakest}의 기운으로 여유를 찾으며 속도를 조절하세요",
            f"주변의 시선({dominant})에 민감해지기 쉬운 때입니다. {weakest}의 본질적 가치에 집중하며 내면의 중심을 잡으세요",
            f"완벽주의적 성향({dominant})이 독이 될 수 있습니다. {weakest}의 유연함을 빌려 자신을 조금 더 놓아주세요"
        ],
        "재성_과다": [
            f"재물 욕심({dominant})이 앞설 수 있는 시기입니다. {weakest}의 논리를 빌려 차분히 자산을 관리하며 실속을 챙기세요",
            f"결과 중심적 사고({dominant})가 관계를 해칠 수 있습니다. {weakest}의 포용력으로 과정의 아름다움을 느껴보세요",
            f"현실적 이득({dominant})보다 중요한 것은 {weakest}의 안정감입니다. 장기적인 안목으로 투자 포지션을 유지하세요"
        ],
        "식상_과다": [
            f"표현 욕구({dominant})가 넘쳐 에너지가 소모될 수 있습니다. {weakest}의 정적인 활동으로 내실을 기하며 지혜를 모으세요",
            f"말과 행동({dominant})이 앞서 오해를 살 수 있으니, {weakest}의 신중함으로 한 번 더 생각하고 움직이세요",
            f"창의적 에너지({dominant})가 분산되기 쉽습니다. {weakest}의 집중력을 발휘하여 하나의 목표에 영혼을 담으세요"
        ]
    }
    
    # 십성 기반 태그 결정
    key = "기본"
    if dominant in ["편관", "정관"] and strongest in ["화", "금"]: key = "관성_과다"
    elif dominant in ["편재", "정재"] and strongest in ["토", "수"]: key = "재성_과다"
    elif dominant in ["식신", "상관"] and strongest in ["목", "화"]: key = "식상_과다"
    
    import random
    # 고정된 시드(seed) 대신 카테고리 길이나 이름을 활용하여 일관적이면서도 다양한 선택
    idx = len(category) % 3
    reconciliation = reconciliation_options.get(key, ["자신의 강점을 믿고 나아가세요"] * 3)[idx]
    
    return reconciliation


def _build_header(saju, user_profile, category="전체", context=None):
    """
    Common header (~700 chars)
    """
    if not context:
        context = _get_master_context(saju, user_profile)
    
    name = user_profile.get("name", "")
    name_display = name
    job = user_profile.get("job", "")
    mbti = user_profile.get("mbti", "")
    relation_type = user_profile.get("relation_type", "lover")
    
    # [Fix] 관계 데이터가 있고 관련 테마일 때만 '궁합' 타이틀 적용
    title_suffix = "분석 결과"
    if user_profile.get("relation_data") and category in ["애정운", "궁합", "러브시그널"]:
        title_suffix = "궁합 분석 결과"
    
    lines = [
        f"## 🔮 {name_display}님의 {category} {title_suffix}\n",
        f"> **Master Insight**: {context['master_strategy']}를 중심으로 한 {context['env_theme']} 가이드입니다.\n"
    ]
    
    is_compact = category not in ["평생사주", "신년운세", "전체"]
    
    # Profile Table
    lines.append("| 항목 | 정보 |")
    lines.append("|:---|:---|")
    lines.append(f"| 일간(日干) | {saju['day_stem']}({STEM_ELEMENT[saju['day_stem']]}) |")
    
    if is_compact:
        info_parts = [p for p in [job, mbti] if p]
        if info_parts: lines.append(f"| 배경 | {' / '.join(info_parts)} |")
    else:
        if job: lines.append(f"| 직업 | {job} |")
        if mbti: lines.append(f"| MBTI | {mbti} |")
        lines.append(f"| 사주 | {saju['saju_text']} |")
    
    lines.append("")
    
    stem_info = query_heavenly_stem(saju["day_stem"])
    if stem_info:
        summary = stem_info.get('modern_summary', stem_info['personality'].split('.')[0])
        lines.append(f"> **MZ Summary**: {summary}\n")

    return "\n".join(lines)



def _build_element_section(saju):
    """Element analysis section (~600 chars)"""
    elems = saju["elements"]
    day_elem = saju["day_stem_element"]
    lines = ["### 📊 오행(五行) 균형 분석\n"]
    for elem in ["목","화","토","금","수"]:
        cnt = elems["count"][elem]
        bar = "█" * cnt + "░" * (8 - cnt)
        status = elems["balance"][elem]
        lines.append(f"- **{elem}({query_element(elem)['hanja']})**: {bar} {cnt}개 ({status})")
    
    weakest = elems["weakest"]
    strongest = elems["strongest"]
    w_info = query_element(weakest)
    s_info = query_element(strongest)
    
    lines.append(f"\n> 💡 **핵심 포인트**: {strongest}({s_info['hanja']}) 기운이 가장 강하고, "
                 f"{weakest}({w_info['hanja']}) 기운이 부족합니다. "
                 f"{weakest} 기운을 보충하면 전체 운의 균형이 좋아집니다.\n")
    
    # Remediation tips
    lines.append(f"**{weakest} 기운 보충법**:")
    lines.append(f"- 색상: {w_info['emotion']}을 안정시키는 {weakest} 계열 색상 활용")
    lines.append(f"- 장기: {w_info['body_organ']} 건강에 주의")
    lines.append(f"- 맛: {w_info['taste']}의 음식을 적절히 섭취")
    lines.append(f"- 숫자: {w_info['number']}을 활용\n")
    
    return "\n".join(lines)


def _build_ten_gods_section(saju):
    """십성 분석 섹션"""
    lines = ["### 🌟 십성(十星) 배치\n"]
    lines.append("| 위치 | 천간 | 지지 | 십성 |")
    lines.append("|:---:|:---:|:---:|:---:|")
    
    pillar_names = {"year":"년주(조상)","month":"월주(부모)","day":"일주(나)","hour":"시주(자녀)"}
    for key in ["year","month","day","hour"]:
        p = saju["pillars"][key]
        god = saju["ten_gods"][{"year":"년주","month":"월주","day":"일주","hour":"시주"}[key]]
        lines.append(f"| {pillar_names[key]} | {p['stem']} | {p['branch']} | {god} |")
    
    dominant = get_dominant_god(saju["god_count"])
    god_info = query_ten_god(dominant)
    if god_info:
        lines.append(f"\n**주도 십성: {dominant}({god_info['hanja']})** — {god_info['keyword']}")
        lines.append(f"\n{god_info['personality']}\n")
    
    return "\n".join(lines)


def _build_blood_section(blood_type):
    """혈액형 분석 섹션"""
    if not blood_type:
        return ""
    info = query_blood_type(blood_type)
    if not info:
        return ""
    lines = [
        f"### 🩸 혈액형 유전자형 분석 ({info['display_name']})\n",
        f"**사주 대응 십성**: {info['saju_god']}",
        f"\n{info['personality']}\n",
    ]
    return "\n".join(lines)


def _build_mbti_section(mbti_type):
    """MBTI 분석 섹션"""
    if not mbti_type:
        return ""
    info = query_mbti(mbti_type)
    if not info:
        return ""
    lines = [
        f"### 🧠 MBTI 교차분석 ({mbti_type} — {info['title']})\n",
        f"**사주 대응 십성**: {info['saju_god']}",
        f"\n{info['personality']}\n",
        f"**커리어 조언**: {info['career_advice']}\n",
    ]
    return "\n".join(lines)


def _build_category_section(category, saju, user_profile):
    """카테고리별 전문 분석"""
    dominant = get_dominant_god(saju["god_count"])
    god_info = query_ten_god(dominant)
    day_elem = saju["day_stem_element"]
    elems = saju["elements"]
    yearly = get_yearly_fortune(day_elem)
    monthly = get_monthly_tips(day_elem)
    advice = generate_element_advice(elems["weakest"], elems["strongest"])
    
    lines = []
    
    if category == "재물운":
        lines = _gen_wealth(god_info, dominant, saju, user_profile, yearly, monthly, advice)
    elif category == "애정운":
        lines = _gen_love(god_info, dominant, saju, user_profile, yearly, monthly, advice)
    elif category == "직업운":
        lines = _gen_career(god_info, dominant, saju, user_profile, yearly, monthly, advice)
    elif category == "건강운":
        lines = _gen_health(god_info, dominant, saju, user_profile, yearly, monthly, advice)
    elif category == "평생사주":
        lines = _gen_lifetime(god_info, dominant, saju, user_profile, yearly, monthly, advice)
    elif category == "오늘의운세":
        lines = _gen_today(god_info, dominant, saju, user_profile, advice)
    elif category == "이번달운세":
        lines = _gen_this_month(god_info, dominant, saju, user_profile, monthly, advice)
    elif category == "신년운세":
        lines = _gen_new_year(god_info, dominant, saju, user_profile, yearly, monthly, advice)
    elif category == "궁합":
        lines = _gen_compatibility(god_info, dominant, saju, user_profile, advice)
    elif category == "개운법":
        lines = _gen_luck_boost(god_info, dominant, saju, user_profile, advice, elems)
    elif category == "MBTI분석":
        lines = gen_mbti_category(saju, user_profile, advice)
    else:
        # Default fallback or "혈액형분석" redirect to lifetime
        lines = _gen_lifetime(god_info, dominant, saju, user_profile, yearly, monthly, advice)
    
    return "\n".join(lines)


def _gen_wealth(god, dominant, saju, profile, yearly, monthly, advice):
    """재물운 생성 - 중복 제거 및 특화 분석 집중"""
    job = profile.get("job", "")
    
    lines = [
        f"### 💰 재물운 심층 분석\n",
        f"#### 1. 사주 원국의 재물 구조",
        f"\n일간 {saju['day_stem']} 기운을 가진 당신의 **{dominant}** 성향은 재물 관리에서 다음과 같이 나타납니다.\n",
        f"{god['wealth']}\n",
        f"#### 2. 오행으로 본 자산 운용 전략\n",
    ]
    
    weakest = saju["elements"]["weakest"]
    if weakest in ["금","수"]:
        lines.append("현금 유동성 확보와 단기 대중 자산 관리에 집중하는 것이 유리한 사주입니다.\n")
    elif weakest in ["목","화"]:
        lines.append("성장형 자산이나 새로운 투자처를 발굴하는 공격적인 전략이 필요할 때입니다.\n")
    else:
        lines.append("부동산이나 실물 자산 같이 기초가 탄탄한 자산 위주로 포트폴리오를 구성하세요.\n")
    
    if job:
        lines.append(f"#### 3. {job} 종사자를 위한 재물 팁\n")
        lines.append(f"현재 하시는 일({job})의 특성을 고려할 때, {dominant}의 기운을 활용한 수입 극대화 전략이 필요합니다.\n")
    
    return lines


def _gen_love(god, dominant, saju, profile, yearly, monthly, advice):
    """애정운 - 특화 분석 중심"""
    marital = profile.get("marital_status", "미혼")
    
    lines = [
        f"### 💕 애정운 심층 분석\n",
        f"#### 1. {marital}자를 위한 관계 조언\n",
        f"일간 {saju['day_stem']}의 기운을 가진 당신은 연애에서 **{dominant}**적인 면모를 보입니다.\n",
        f"{god['love']}\n",
    ]
    
    day_branch = saju["pillars"]["day"]["branch"]
    branch_info = query_branch(day_branch)
    if branch_info:
        lines.append(f"\n당신의 내부(일지)에 자리한 **{day_branch}({branch_info['animal']})** 기운은 배우자 또는 인연운에서 중요한 역할을 합니다. {branch_info['personality'][:100]}...\n")
    
    return lines


def _gen_career(god, dominant, saju, profile, yearly, monthly, advice):
    """직업운"""
    job = profile.get("job", "")
    education = profile.get("education", "")
    
    lines = [
        f"### 💼 직업운 심층 분석\n",
        f"#### 1. 사주로 본 직업 적성\n",
        f"일간 {saju['day_stem']}({saju['day_stem_element']}) + 주도 십성 **{dominant}({god['hanja']})**:\n",
        f"{god['career']}\n",
    ]
    
    if job:
        lines.append(f"#### 2. 현재 직업 분석: {job}\n")
        lines.append(f"현재 종사하시는 **{job}** 직업은 {dominant}의 기운과 ")
        
        career_match = {
            "비견": ["프리랜서","자영업","전문직","컨설턴트"],
            "겁재": ["영업","마케팅","투자","스포츠"],
            "식신": ["연구","개발","요리","교사","기술"],
            "상관": ["크리에이터","기획","디자인","예술","변호사"],
            "편재": ["사업","무역","영업관리","투자"],
            "정재": ["회계","세무","은행","재무","보험계리사"],
            "편관": ["경찰","군인","CEO","위기관리"],
            "정관": ["공무원","대기업","관리자","PM"],
            "편인": ["AI 연구","철학","심리상담","특수기술"],
            "정인": ["교수","교사","연구원","작가","컨설턴트"],
        }
        
        matched = any(keyword in job for keyword in career_match.get(dominant, []))
        if matched:
            lines.append(f"**높은 궁합**을 보입니다! 현재 직업이 사주와 잘 맞아 자연스럽게 능력을 발휘할 수 있습니다.\n")
        else:
            lines.append(f"다른 방향에서 시너지를 찾을 수 있습니다. {dominant}의 기운을 현재 직업에 접목하면 더 좋은 성과를 낼 수 있습니다.\n")
    
    lines.extend([
        f"\n#### 3. 2026년 직업운 전망\n",
        f"**{yearly[0]}**: {yearly[1]}\n",
        f"#### 4. 월별 커리어 흐름\n",
    ])
    for period, tip in monthly:
        lines.append(f"- **{period}**: {tip}")
    
    # 신규: 커리어 로드맵 추가
    lines.append(build_career_pathmap(saju))

    lines.extend([
        f"\n#### 5. 직업 개운법 🍀\n",
        f"- 🎨 **파워 컬러**: {advice['color']}",
        f"- 🧭 **유리한 방위**: {advice['direction']}",
        f"- 🏃 **커리어 부스터**: {advice['activity']}",
        f"\n> 💡 **핵심 조언**: {god['keyword']}의 기운을 살려 전문성을 높이세요.\n",
    ])
    return lines


def _gen_health(god, dominant, saju, profile, yearly, monthly, advice):
    """건강운"""
    weakest = saju["elements"]["weakest"]
    strongest = saju["elements"]["strongest"]
    elem_info = query_element(weakest)
    strong_info = query_element(strongest)
    day_elem = saju["day_stem_element"]
    
    # 오행별 장기 매핑
    organ_map = {"목":"간장/담낭/눈/근육/손톱","화":"심장/소장/혀/혈관/안면","토":"비장/위장/입술/살/피부","금":"폐/대장/코/피부/체모","수":"신장/방광/귀/뼈/치아"}
    
    lines = [
        f"### 🏥 건강운 심층 분석\n",
        f"#### 1. 사주 원국의 건강 구조\n",
        f"일간 {saju['day_stem']}({day_elem}) + 주도 십성 **{dominant}({god['hanja']})**:\n",
        f"{god['health']}\n",
        f"#### 2. 오행과 장기의 관계\n",
        f"| 오행 | 관련 장기 | 사주 내 개수 | 상태 |\n",
        f"|:---:|:---|:---:|:---:|\n",
    ]
    for e in ["목","화","토","금","수"]:
        cnt = saju["elements"]["count"][e]
        status = "⚠️ 부족" if cnt == 0 else "🟡 약함" if cnt == 1 else "🟢 적정" if cnt <= 3 else "🔴 과다"
        lines.append(f"| {e} | {organ_map[e]} | {cnt}개 | {status} |")
    
    lines.extend([
        f"\n#### 3. 핵심 건강 취약점\n",
        f"**부족한 오행: {weakest}({elem_info['hanja']})**\n",
        f"- **주의 장기**: {elem_info['body_organ']}\n",
        f"- **관련 감정**: {elem_info['emotion']}\n",
        f"- {weakest} 기운이 약하면 {elem_info['body_organ']}에 무리가 올 수 있습니다. "
        f"특히 {weakest}이(가) 극을 받는 계절에는 해당 장기의 부담이 커지므로 "
        f"미리 예방적 건강 관리가 필요합니다.\n",
        f"**과다한 오행: {strongest}({strong_info['hanja']})**\n",
        f"- {strongest} 기운이 과하면 {strong_info['body_organ']} 관련 증상이 나타날 수 있습니다. "
        f"에너지 과잉을 적절히 발산하는 것이 중요합니다.\n",
    ])
    
    # 십성별 스트레스 패턴
    lines.append(f"#### 4. 십성별 스트레스 패턴\n")
    stress_map = {
        "비견": ("경쟁 스트레스", "타인과의 비교에서 오는 긴장감. 자신만의 페이스를 유지하고 비교를 줄이세요."),
        "겁재": ("과도한 활동 스트레스", "무리한 신체·정신 활동에서 오는 번아웃. 규칙적인 휴식과 수면이 필수입니다."),
        "식신": ("과식/소화 스트레스", "음식으로 스트레스를 풀려는 경향. 규칙적인 식사와 소화기 관리가 중요합니다."),
        "상관": ("감정 과부하 스트레스", "예민한 감성에서 오는 정서적 소진. 창작 활동이나 예술로 감정을 승화시키세요."),
        "편재": ("과잉 활동 스트레스", "너무 많은 일을 동시에 처리하려는 성향. 우선순위를 정하고 에너지를 분배하세요."),
        "정재": ("완벽주의 스트레스", "모든 것을 꼼꼼히 관리하려는 성향에서 오는 피로. 중요한 것에만 집중하세요."),
        "편관": ("책임감 스트레스", "과도한 책임과 의무에서 오는 압박. 위임과 분담을 통해 부담을 줄이세요."),
        "정관": ("체면 스트레스", "사회적 기대에 맞추려는 노력에서 오는 긴장. 진정한 자기 모습을 인정하세요."),
        "편인": ("사고 과부하 스트레스", "끊임없는 생각과 분석에서 오는 정신적 피로. 명상과 산책으로 머리를 비우세요."),
        "정인": ("걱정/불안 스트레스", "가족과 주변 사람에 대한 과도한 걱정. 적절한 거리두기와 자기 돌봄이 필요합니다."),
    }
    s_type, s_desc = stress_map.get(dominant, stress_map["비견"])
    lines.extend([
        f"**{dominant} 주도 사주의 스트레스 유형**: {s_type}\n",
        f"{s_desc}\n",
    ])
    
    lines.append(f"#### 5. 계절별 건강 관리\n")
    for period, tip in monthly:
        lines.append(f"- **{period}**: {tip}")
    
    lines.extend([
        f"\n#### 6. 맞춤형 건강 루틴\n",
        f"| 시간 | 추천 활동 |",
        f"|:---|:---|",
        f"| 🌅 기상 시 | 가벼운 스트레칭 + {advice['food']} 포함 아침식사 |",
        f"| 🌞 오전 | {advice['activity']} 또는 가벼운 산책 20분 |",
        f"| 🍽️ 점심 | {weakest} 기운 보충 음식 섭취, 15분 낮잠 |",
        f"| 🌆 오후 | {advice['direction']} 방향으로 짧은 외출 또는 환기 |",
        f"| 🌙 취침 전 | {advice['color']} 계열 조명, 명상 10분 |",
        f"\n#### 7. 건강 개운법 🍀\n",
        f"- 🍽️ **추천 음식**: {advice['food']}",
        f"- 🏃 **추천 운동**: {advice['activity']}",
        f"- 🎨 **건강 색상**: {advice['color']}",
        f"- 🧭 **건강한 방위**: {advice['direction']}",
        f"\n> 💡 **핵심 조언**: {weakest}({elem_info['hanja']}) 기운 보충이 건강의 열쇠입니다. "
        f"매일 {advice['food']}을 포함한 균형 잡힌 식사와 {advice['activity']}을 실천하세요.\n",
    ])
    return lines


def _gen_lifetime(god, dominant, saju, profile, yearly, monthly, advice):
    """평생사주 (종합)"""
    lines = [
        f"### 🌏 평생사주 종합 분석\n",
        f"#### 1. 타고난 성격과 기질\n",
        f"일간 **{saju['day_stem']}({saju['day_stem_element']}/{saju['day_stem_yinyang']})**에 주도 십성 **{dominant}({god['hanja']})**의 조합:\n",
    ]
    
    stem_info = query_stem(saju["day_stem"])
    if stem_info:
        lines.append(f"{stem_info['personality']}\n")
    lines.append(f"{god['personality']}\n")
    
    lines.extend([
        f"#### 2. 직업/재물/애정 종합\n",
        f"**💼 직업**: {god['career']}\n",
        f"**💰 재물**: {god['wealth']}\n",
        f"**💕 애정**: {god['love']}\n",
        f"**🏥 건강**: {god['health']}\n",
        f"#### 3. 2026년 종합 운세\n",
        f"**{yearly[0]}**: {yearly[1]}\n",
        f"#### 4. 월별 운세\n",
    ])
    for period, tip in monthly:
        lines.append(f"- **{period}**: {tip}")
    
    lines.extend([
        f"\n#### 5. 종합 개운법 🍀\n",
        f"- 🎨 **행운 색상**: {advice['color']}",
        f"- 🧭 **행운 방위**: {advice['direction']}",
        f"- 🔢 **행운 숫자**: {advice['number']}",
        f"- 🍽️ **행운 음식**: {advice['food']}",
        f"- 🏃 **추천 활동**: {advice['activity']}",
    ])
    return lines


def _gen_today(god, dominant, saju, profile, advice):
    """오늘의 운세"""
    today = datetime.date.today()
    from saju_calculator import calculate_year_pillar
    today_stem, today_branch = calculate_year_pillar(today.year)
    day_elem = saju["day_stem_element"]
    weakest = saju["elements"]["weakest"]
    
    lines = [
        f"### 📅 오늘의 운세 ({today.strftime('%Y년 %m월 %d일')})\n",
        f"#### 1. 오늘의 기운\n",
        f"일간 {saju['day_stem']}({day_elem}) 기준으로 오늘은 **{dominant}({god['hanja']})**의 기운이 작용합니다.\n",
        f"{god['personality']}\n",
        f"오늘은 {dominant}의 에너지가 강하게 흐르는 날입니다. "
        f"이 기운을 잘 활용하면 평소보다 나은 결과를 얻을 수 있습니다.\n",
        f"#### 2. 시간대별 에너지 흐름\n",
        f"| 시간대 | 에너지 | 추천 활동 |",
        f"|:---|:---:|:---|",
    ]
    
    hour_map = {
        "목": [
            ("06-09시(묘시)", "🟢 상승", "새로운 계획 수립, 건강한 루틴 시작"),
            ("09-12시(사시)", "🟡 안정", "중요한 업무 처리, 문서 작업"),
            ("12-15시(미시)", "🔴 하강", "가벼운 식사, 짧은 휴식"),
            ("15-18시(유시)", "🟡 회복", "팀 미팅, 협업 작업"),
            ("18-21시(해시)", "🟢 충전", "자기 계발, 운동, 독서"),
        ],
        "화": [
            ("06-09시(묘시)", "🟡 준비", "명상, 하루 계획 점검"),
            ("09-12시(사시)", "🟢 최고", "프레젠테이션, 중요 회의"),
            ("12-15시(미시)", "🟢 활성", "영업, 대인관계 활동"),
            ("15-18시(유시)", "🟡 조정", "서류 정리, 후속 작업"),
            ("18-21시(해시)", "🔵 안정", "가족 시간, 취미 활동"),
        ],
        "토": [
            ("06-09시(묘시)", "🟡 안정", "루틴 점검, 건강 관리"),
            ("09-12시(사시)", "🟢 상승", "재무 계획, 투자 검토"),
            ("12-15시(미시)", "🟢 최고", "중요한 결정, 계약"),
            ("15-18시(유시)", "🟡 유지", "팀워크, 네트워킹"),
            ("18-21시(해시)", "🔵 충전", "명상, 가벼운 산책"),
        ],
        "금": [
            ("06-09시(묘시)", "🟡 준비", "정리정돈, 계획 수립"),
            ("09-12시(사시)", "🟡 안정", "분석 업무, 데이터 작업"),
            ("12-15시(미시)", "🟢 상승", "협상, 계약, 중요 미팅"),
            ("15-18시(유시)", "🟢 최고", "핵심 업무 마무리"),
            ("18-21시(해시)", "🟡 정리", "성과 점검, 내일 준비"),
        ],
        "수": [
            ("06-09시(묘시)", "🔵 충전", "직감적 결정, 창의적 사고"),
            ("09-12시(사시)", "🟡 상승", "전략 수립, 기획 업무"),
            ("12-15시(미시)", "🟡 안정", "점심 네트워킹, 가벼운 미팅"),
            ("15-18시(유시)", "🟢 활성", "학습, 자격 시험 공부"),
            ("18-21시(해시)", "🟢 최고", "중요한 대화, 깊은 사색"),
        ],
    }
    hours = hour_map.get(day_elem, hour_map["목"])
    for time, energy, act in hours:
        lines.append(f"| {time} | {energy} | {act} |")
    
    lines.extend([
        f"\n#### 3. 오늘의 영역별 조언\n",
        f"**💼 업무운**\n",
        f"{god['career']}\n",
        f"오늘 업무에서는 {dominant}의 특성을 살려 ",
    ])
    if dominant in ["식신","상관"]:
        lines.append(f"창의적 아이디어를 적극 제안하세요. 독특한 시각이 높은 평가를 받습니다.\n")
    elif dominant in ["정관","편관"]:
        lines.append(f"리더십을 발휘하세요. 주도적으로 나서면 팀 성과가 올라갑니다.\n")
    elif dominant in ["정재","편재"]:
        lines.append(f"실질적 성과에 집중하세요. 숫자와 데이터로 뒷받침하면 설득력이 높아집니다.\n")
    else:
        lines.append(f"본인의 전문성을 발휘하세요. 꼼꼼한 준비가 좋은 결과를 만듭니다.\n")
    
    lines.extend([
        f"**💰 재물운**\n",
        f"{god['wealth']}\n",
        f"오늘의 재물 흐름은 ",
    ])
    if today.day % 2 == 0:
        lines.append(f"안정적입니다. 계획된 지출은 괜찮지만 충동 구매는 자제하세요. "
                     f"숫자 {advice['number']}과 관련된 금액에 행운이 있습니다.\n")
    else:
        lines.append(f"예상치 못한 소득이 있을 수 있습니다. 작은 기회도 놓치지 마세요. "
                     f"다만 큰 투자 결정은 내일로 미루는 것이 안전합니다.\n")
    
    lines.extend([
        f"**💕 대인관계**\n",
        f"{god['love']}\n",
        f"오늘 인간관계에서는 {dominant}의 기운이 작용하여 ",
    ])
    if dominant in ["비견","겁재"]:
        lines.append(f"동료와의 경쟁보다 협력에 초점을 맞추세요. 양보가 더 큰 이익을 가져옵니다.\n")
    elif dominant in ["식신","정인"]:
        lines.append(f"따뜻한 말 한마디가 관계를 크게 개선합니다. 점심을 함께 하면 좋겠습니다.\n")
    else:
        lines.append(f"진솔한 소통이 관계를 깊게 만듭니다. 경청하는 자세가 신뢰를 쌓습니다.\n")
    
    job = profile.get("job", "")
    if job:
        lines.extend([
            f"**🎯 {job} 종사자 오늘의 팁**\n",
            f"- {dominant} 기운을 활용하여 업무 효율을 극대화하세요",
            f"- {advice['color']} 계열 소품을 데스크에 두면 집중력이 높아집니다",
            f"- 점심에 {advice['food']}을 드시면 오후 에너지가 올라갑니다\n",
        ])
    
    lines.extend([
        f"#### 4. 오늘의 개운법 🍀\n",
        f"| 항목 | 추천 |",
        f"|:---|:---|",
        f"| 🎨 색상 | {advice['color']} |",
        f"| 🔢 숫자 | {advice['number']} |",
        f"| 🍽️ 음식 | {advice['food']} |",
        f"| 🧭 방위 | {advice['direction']} |",
        f"| 🏃 활동 | {advice['activity']} |",
        f"\n> 💡 **오늘의 한마디**: {dominant}의 기운이 흐르는 오늘, "
        f"부족한 {weakest} 기운을 {advice['food']}으로 보충하고 "
        f"{advice['color']} 색상으로 행운을 끌어당기세요!\n",
    ])
    return lines


def _gen_this_month(god, dominant, saju, profile, monthly, advice):
    """이번달 운세"""
    now = datetime.date.today()
    month = now.month
    period_idx = min((month - 1) // 2, 5)
    period, tip = monthly[period_idx]
    day_elem = saju["day_stem_element"]
    weakest = saju["elements"]["weakest"]
    
    lines = [
        f"### 📆 이번 달 운세 ({now.strftime('%Y년 %m월')})\n",
        f"#### 1. {now.month}월의 기운\n",
        f"{tip}\n",
        f"이번 달은 {dominant}({god['hanja']})의 기운이 주도적으로 작용합니다. "
        f"일간 {saju['day_stem']}({day_elem})과의 상호작용을 살펴보면, "
        f"이 시기에 집중해야 할 영역과 주의해야 할 부분이 명확해집니다.\n",
        f"#### 2. 이번 달 영역별 상세\n",
        f"**💼 직업운**\n",
        f"{god['career']}\n",
    ]
    
    if dominant in ["정관","편관","정재"]:
        lines.append(f"이번 달은 조직 내 안정과 성과에 집중하는 것이 유리합니다. "
                     f"상사의 신뢰를 얻을 기회가 있으니, 맡은 바 책임을 완수하세요.\n")
    elif dominant in ["식신","상관","편재"]:
        lines.append(f"새로운 아이디어나 사업 기회가 포착되는 달입니다. "
                     f"평소와 다른 접근 방식을 시도하면 좋은 반응을 얻을 수 있습니다.\n")
    else:
        lines.append(f"본업에 충실하면서 부업이나 자기계발도 병행하기 좋은 시기입니다. "
                     f"역량 강화에 투자한 시간이 나중에 큰 보상으로 돌아옵니다.\n")
    
    lines.extend([
        f"**💰 재물운**\n",
        f"{god['wealth']}\n",
        f"**💕 관계운**\n",
        f"{god['love']}\n",
        f"**🏥 건강운**\n",
        f"{god['health']}\n",
        f"#### 3. 주간별 에너지 흐름\n",
        f"| 주차 | 에너지 | 핵심 전략 |",
        f"|:---:|:---:|:---|",
        f"| 1주차(1~7일) | 🟡 준비 | 계획 수립과 정보 수집에 집중. 큰 결정은 자제 |",
        f"| 2주차(8~14일) | 🟢 상승 | 적극적 행동의 시기. 미팅, 계약, 제안에 최적 |",
        f"| 3주차(15~21일) | 🟢 최고 | 에너지 절정기. 중요한 프로젝트 마무리에 집중 |",
        f"| 4주차(22~말일) | 🟡 정리 | 성과 점검과 다음 달 준비. 건강 관리 강화 |",
    ])
    
    job = profile.get("job", "")
    if job:
        lines.extend([
            f"\n#### 4. {job} 종사자 이번 달 전략\n",
            f"- **1주차**: {job} 관련 새로운 트렌드와 동향을 파악하세요",
            f"- **2주차**: 핵심 프로젝트나 실적에 집중하여 성과를 만드세요",
            f"- **3주차**: {dominant}의 기운을 활용하여 네트워킹을 확장하세요",
            f"- **4주차**: 이번 달 성과를 정리하고 다음 달 목표를 설정하세요\n",
        ])
    
    lines.extend([
        f"#### 5. 연간 흐름 속 이번 달 위치\n",
    ])
    for p, t in monthly:
        marker = " 👈 **현재**" if p == period else ""
        lines.append(f"- **{p}**: {t}{marker}")
    
    lines.extend([
        f"\n#### 6. 이번 달 개운법 🍀\n",
        f"| 항목 | 추천 |",
        f"|:---|:---|",
        f"| 🎨 행운 색상 | {advice['color']} |",
        f"| 🧭 행운 방위 | {advice['direction']} |",
        f"| 🔢 행운 숫자 | {advice['number']} |",
        f"| 🍽️ 행운 음식 | {advice['food']} |",
        f"| 🏃 추천 활동 | {advice['activity']} |",
        f"\n> 💡 **이번 달 핵심**: {dominant}의 에너지를 잘 활용하면 "
        f"직업과 재물 모두에서 좋은 성과를 낼 수 있습니다. "
        f"부족한 {weakest} 기운 보충에 신경 쓰세요.\n",
    ])
    return lines


def _gen_new_year(god, dominant, saju, profile, yearly, monthly, advice):
    """신년운세"""
    lines = [
        f"### 🎆 2026년 신년 운세\n",
        f"#### 1. 2026년 병오(丙午)년 총운\n",
        f"2026년은 **병오(丙午)년**으로 화(火) 기운이 매우 강한 해입니다. "
        f"태양(丙)과 말(午)의 에너지가 결합하여 열정, 활동, 표현의 해가 됩니다.\n",
        f"화(火)의 해에는 빠른 변화와 열정적인 에너지가 지배합니다. "
        f"새로운 시작, 사업 확장, 자기 표현에 유리하지만 과열에 주의해야 합니다. "
        f"차분하게 계획하고 단계적으로 실행하는 것이 성공의 열쇠입니다.\n",
        f"#### 2. 일간 {saju['day_stem']}({saju['day_stem_element']}) 기준 운세\n",
        f"**{yearly[0]}**: {yearly[1]}\n",
        f"#### 3. 분기별 운세\n",
    ]
    for period, tip in monthly:
        lines.append(f"- **{period}**: {tip}")
    
    lines.extend([
        f"\n#### 4. 2026년 핵심 조언\n",
        f"**💼 직업**: {god['career']}\n",
        f"**💰 재물**: {god['wealth']}\n",
        f"**💕 관계**: {god['love']}\n",
        f"**🏥 건강**: {god['health']}\n",
        f"#### 5. 2026년 개운법 🍀\n",
        f"- 🎨 **올해의 색상**: {advice['color']}",
        f"- 🧭 **올해의 방위**: {advice['direction']}",
        f"- 🔢 **올해의 숫자**: {advice['number']}",
        f"- 🍽️ **올해의 음식**: {advice['food']}",
        f"- 🏃 **올해의 활동**: {advice['activity']}",
    ])
    return lines


def _gen_compatibility(god, dominant, saju, profile, advice):
    """궁합"""
    day_branch = saju["pillars"]["day"]["branch"]
    
    # 삼합 (가장 좋은 궁합)
    samhap = {"자":["진","신"],"축":["사","유"],"인":["오","술"],"묘":["미","해"],
              "진":["자","신"],"사":["축","유"],"오":["인","술"],"미":["묘","해"],
              "신":["자","진"],"유":["축","사"],"술":["인","오"],"해":["묘","미"]}
    
    # 육합
    yukhap = {"자":"축","축":"자","인":"해","묘":"술","진":"유","사":"신",
              "오":"미","미":"오","신":"사","유":"진","술":"묘","해":"인"}
    
    good_match = samhap.get(day_branch, [])
    best_match = yukhap.get(day_branch, "")
    
    lines = [
        f"### 💑 궁합 분석\n",
        f"#### 1. 배우자궁 분석\n",
        f"일지(배우자궁): **{day_branch}({BRANCH_ANIMAL[day_branch]})**\n",
    ]
    branch_info = query_branch(day_branch)
    if branch_info:
        lines.append(f"{branch_info['personality']}\n")
    
    lines.extend([
        f"#### 2. 최고의 궁합 (삼합)\n",
        f"- **{good_match[0]}({BRANCH_ANIMAL[good_match[0]]})띠**, **{good_match[1]}({BRANCH_ANIMAL[good_match[1]]})띠**와 삼합으로 최고의 궁합!\n",
        f"#### 3. 좋은 궁합 (육합)\n",
        f"- **{best_match}({BRANCH_ANIMAL[best_match]})띠**와 육합으로 좋은 인연\n",
        f"#### 4. 십성으로 본 이상형\n",
        f"{god['love']}\n",
        f"#### 5. 궁합 개운법 🍀\n",
        f"- 🎨 **인연의 색상**: {advice['color']}",
        f"- 🧭 **인연의 방위**: {advice['direction']}",
    ])
    return lines


def _gen_luck_boost(god, dominant, saju, profile, advice, elems):
    """개운법"""
    weakest = elems["weakest"]
    elem_info = query_element(weakest)
    strongest = elems["strongest"]
    strong_info = query_element(strongest)
    day_elem = saju["day_stem_element"]
    
    lines = [
        f"### 🍀 종합 개운법\n",
        f"#### 1. 오행 보완 전략\n",
        f"사주에서 **{weakest}({elem_info['hanja']})** 기운이 가장 부족합니다. "
        f"이를 보충하면 전체 운의 균형이 좋아집니다.\n",
        f"반대로 **{strongest}({strong_info['hanja']})** 기운이 과다하므로 "
        f"이를 적절히 발산하면 에너지 순환이 원활해집니다.\n",
        f"#### 2. 생활 속 개운법\n",
        f"| 항목 | 추천 |",
        f"|:---|:---|",
        f"| 🎨 색상 | {advice['color']} |",
        f"| 🧭 방위 | {advice['direction']} |",
        f"| 🔢 숫자 | {advice['number']} |",
        f"| 🍽️ 음식 | {advice['food']} |",
        f"| 🏃 활동 | {advice['activity']} |",
        f"\n#### 3. 영역별 개운 전략\n",
        f"**💰 재물운 개운법**\n",
        f"- 지갑 색상을 {advice['color']} 계열로 바꾸세요",
        f"- 통장 개설 시 {advice['direction']} 방향의 은행 지점을 이용하세요",
        f"- 중요한 금전 거래는 숫자 {advice['number']}이 포함된 날짜에 진행하세요",
        f"- {advice['food']}을 먹은 후 중요한 재물 관련 결정을 내리세요\n",
        f"**💼 직업운 개운법**\n",
        f"- 출근 시 {advice['color']} 계열의 넥타이/스카프/액세서리를 착용하세요",
        f"- 중요한 미팅이나 면접은 {advice['direction']} 방위의 장소에서 진행하세요",
        f"- 명함이나 서류에 {advice['number']} 관련 디자인 요소를 넣으세요",
        f"- {advice['activity']}을 출근 전 루틴으로 만들면 업무 효율이 올라갑니다\n",
        f"**💕 대인관계 개운법**\n",
        f"- 모임은 {advice['direction']} 방향에 있는 장소를 선택하세요",
        f"- {advice['food']}로 상대를 대접하면 관계가 좋아집니다",
        f"- 약속 시간에 {advice['number']}을 활용하세요 (예: 3시, 8시 등)\n",
        f"#### 4. 풍수 인테리어 가이드\n",
    ]

    # 풍수 가이드
    feng_shui = {
        "목": "거실에 키 큰 관엽식물을 두세요. 동쪽 창가에 작은 화분을 놓으면 좋습니다. 나무 소재의 가구를 선택하고 녹색 쿠션이나 커튼을 활용하세요.",
        "화": "남쪽에 간접 조명이나 캔들을 배치하세요. 빨간색/보라색 소품을 포인트로 사용하고, 자연광이 잘 드는 환경을 만드세요.",
        "토": "집 중앙에 도자기나 돌 소품을 배치하세요. 노란색/갈색 계열의 러그나 쿠션을 활용하고, 안정감 있는 낮은 가구를 선택하세요.",
        "금": "서쪽에 금속 소재의 인테리어를 배치하세요. 흰색/은색 계열의 시계나 액자를 걸고, 깔끔하고 정돈된 공간을 유지하세요.",
        "수": "북쪽에 작은 수반이나 가습기를 두세요. 검정색/남색 계열의 소품을 활용하고, 물소리가 나는 분수대나 음악을 틀어두세요.",
    }
    lines.append(f"{feng_shui.get(weakest, feng_shui['목'])}\n")
    
    lines.extend([
        f"#### 5. 알아두면 좋은 상생/상극 관계\n",
        f"| 관계 | 오행 | 의미 |",
        f"|:---:|:---:|:---|",
        f"| 나를 생하는 | {elem_info['generated_by']} | 에너지를 공급해주는 오행. 이 기운을 함께 보충하세요 |",
        f"| 내가 생하는 | {elem_info['generates']} | 에너지를 받아가는 오행. 너무 소모하지 않도록 주의 |",
        f"| 나를 극하는 | {elem_info['controlled_by']} | 나를 약하게 하는 오행. 과도한 노출을 피하세요 |",
        f"| 내가 극하는 | {elem_info['controls']} | 내가 통제하는 오행. 재물과 관련됩니다 |",
        f"\n#### 6. 일상 실천 체크리스트\n",
        f"- [ ] 아침: {advice['color']} 계열 옷 선택",
        f"- [ ] 점심: {advice['food']} 포함 식사",
        f"- [ ] 오후: {advice['direction']} 방향 산책 10분",
        f"- [ ] 저녁: {advice['activity']} 30분",
        f"- [ ] 취침 전: 감사 일기 3줄 작성\n",
        f"> 💡 **핵심 포인트**: 개운법의 본질은 꾸준한 실천입니다. "
        f"매일 작은 변화를 쌓아가면 큰 운의 흐름이 바뀝니다. "
        f"부족한 {weakest}({elem_info['hanja']}) 기운 보충에 집중하세요.\n",
    ])
    return lines


# ────────────────────────────────
# 메인 운세 생성 함수 (Expert/Strategic Overhaul)
# ────────────────────────────────

def generate_fortune(birth_date, birth_time, category, user_profile=None):
    """
    전문가/전략가 중심의 카테고리 최적화 운세 생성 (~6000자)
    MZ-Premium 스타일 변환 및 마스터 컨텍스트 엔진 적용
    """
    if user_profile is None:
        user_profile = {}
    
    # 1. 사주 계산 및 공통 데이터 준비 (글로벌 보정 포함)
    is_sh = user_profile.get("is_southern_hemisphere", False)
    saju = calculate_full_saju(birth_date, birth_time, is_sh)
    saju["mbti"] = user_profile.get("mbti", "")
    
    # 2. [Master Context] 모든 분석의 기저 논리 (Context-Aware)
    context = _get_master_context(saju, user_profile)
    dominant = context["dominant_god"]
    elems = saju["elements"]
    advice = generate_element_advice(elems["weakest"], elems["strongest"])
    
    # 3. [Advanced Analysis] 하이브리드 & 네임 DNA
    hybrid_insight = _generate_hybrid_insight(saju, user_profile.get("mbti", ""))
    
    from seongmyeonghak import analyze_name_balance
    name_hanja = user_profile.get("name_hanja", "")
    name_analysis = analyze_name_balance(name_hanja, elems)
    
    sections = []
    
    # 2. 헤더 [MZ-Premium 특화]
    sections.append(_build_header(saju, user_profile, category, context))
    
    # 3. [Exclusive Content] 하이브리드 & 네임 분석 결과 삽입
    # 맥락적 교차분석 (모든 카테고리 적용)
    cross_analysis = build_contextual_cross_analysis(category, saju, user_profile)
    if cross_analysis:
        sections.append(cross_analysis)

    if hybrid_insight:
        sections.append(hybrid_insight)
    
    if name_analysis.get("status") == "success":
        sections.append(f"### 🔠 Name DNA Analysis: {name_hanja}\n" + name_analysis["analysis_text"])
    
    # ── 배경 데이터 ──
    yearly_default = ("2026년 운세 전망", "병오년의 기운이 강하게 들어와 열정과 성취의 기운이 교차하는 한 해가 될 것입니다.")
    monthly_default = [("1~6월", "운기가 상승하며 새로운 기회를 포착하는 시기입니다."), ("7~12월", "노력한 만큼의 결과를 얻고 내실을 다지는 시기입니다.")]

    # 3. 카테고리별 특화 섹션 (중복 제거 로직 적용)
    god_info = query_ten_god(dominant)
    
    # [Redundancy Control] Only include header information that's necessary for the category
    # If not Lifetime, we don't repeat the full Element/Ten-God deep dives in the same way.
    
    if category == "재물운":
        sections.append(build_wealth_strategy(saju, user_profile))
        sections.append(build_wealth_portfolio_analysis(saju))
        sections.append(_gen_wealth(god_info, dominant, saju, user_profile, yearly_default, monthly_default, advice))
        
    elif category == "직업운":
        sections.append(build_career_pathmap(saju))
        sections.append(build_career_performance_guide(saju, user_profile))
        sections.append(_gen_career(god_info, dominant, saju, user_profile, yearly_default, monthly_default, advice))
        
    elif category == "건강운":
        sections.append(build_preventive_health_rituals(saju))
        sections.append(_gen_health(god_info, dominant, saju, user_profile, yearly_default, monthly_default, advice))
        
    elif category in ["궁합", "애정운"]:
        sections.append(build_love_dynamics(saju, user_profile))
        sections.append(build_relationship_timing_chart(saju))
        
        if user_profile.get("relation_data"):
            r_data = user_profile["relation_data"]
            target_name = r_data.get("target_name", "상대방")
            target_date = r_data.get("target_birth_date")
            target_time = r_data.get("target_birth_time", "12:00")
            target_mbti = r_data.get("target_mbti", "")
            relation_code = r_data.get("relation_code", "LOVER")
            
            rel_report = _build_relationship_context(saju, target_date, target_time, relation_code, target_name, target_mbti, category)
            sections.append(rel_report)
            sections.append(f"### 👩‍❤️‍👨 {user_profile.get('name')} ❤️ {target_name} 궁합 정밀 분석\n")
            
        sections.append(_gen_love(god_info, dominant, saju, user_profile, yearly_default, monthly_default, advice))

    elif category == "평생사주":
        # [Summary Mode] Combine only the core DNA essentials
        sections.append("### 🧬 본캐 DNA 설계도 요약\n귀하의 타고난 기질은 오행과 십성의 독특한 배합으로 구성되어 있습니다.")
        sections.append(_build_element_section(saju)[:500] + "...") # Shave
        sections.append(_build_ten_gods_section(saju)[:500] + "...") # Shave
        sections.append(build_name_analysis_block(saju, user_profile))
        sections.append("\n### 🌐 인생의 주요 스탯(Stat) 요약")
        sections.append(f"- **재물 기반**: 안정적 자산 운용에 최적화된 그릇\n- **성공 동력**: {dominant}의 강력한 추진력")
        sections.append(build_classical_wisdom_section(saju, user_profile))
        sections.append(f"\n### 🗺️ 인생 로드맵 (Roadmap)\n현재 대운은 귀하의 {elems['weakest']} 기운을 보완하며 전성기로 나아가는 흐름입니다.")

    elif category == "신년운세":
        sections.append(["### 📅 2026년(병오년) 총평", 
                         "올해는 '붉은 말'의 해로, 역동적이고 화려한 변화가 예상되는 시기입니다.",
                         f"귀하의 사주와 병오년의 천간/지지가 만나 {dominant}의 에너지가 증폭됩니다."])
        sections.append(build_seasonal_fortune(category, saju, user_profile))
        
        monthly_detail = [
            "#### 🗓️ 월별 상세 운세 가이드",
            "| 월 | 가이드 |",
            "|:---|:---|",
            "| 상반기 | 새로운 시도와 빌드업 |",
            "| 하반기 | 성과 수확 및 안정화 |"
        ]
        sections.append("\n".join(monthly_detail))
        sections.append(build_daily_practice(saju, advice))
        
    elif category == "단기운세" or category in ["오늘의운세", "이번달운세"]:
        sections.append(_gen_today(god_info, dominant, saju, user_profile, advice) if "오늘" in category else _gen_this_month(god_info, dominant, saju, user_profile, monthly_default, advice))
        
    elif category == "개운법":
        sections.append(_gen_luck_boost(god_info, dominant, saju, user_profile, advice, elems))
        sections.append(build_daily_practice(saju, advice))
        
    elif category == "MBTI분석":
        sections.append(gen_mbti_category(saju, user_profile, advice))

    # 4. 최종 조립 및 스타일 변환
    raw_text = "\n\n---\n\n".join([s.strip() if isinstance(s, str) else "\n".join(s).strip() for s in sections if s])
    
    # [Style Transformer] MZ-Premium 어조 적용
    fortune_text = _apply_modern_style(raw_text)
    
    # 푸터 추가 (코칭 멘트)
    footer_parts = []
    if user_profile.get('mbti'):
        footer_parts.append("현대적 MBTI")
    if user_profile.get('blood_type'):
        footer_parts.append("혈액형")
    
    if footer_parts:
        footer_note = f"이 분석은 {user_profile.get('name','사용자')}님의 사주와 {'/'.join(footer_parts)}을(를) 고려하여 재해석한 결과입니다."
    else:
        footer_note = f"이 분석은 {user_profile.get('name','사용자')}님의 사주를 바탕으로 재해석한 결과입니다."

    # [Phase 9] Dynamic & Context-Aware Coach Tips
    coach_tip = _generate_dynamic_coach_tip(category, context, saju)

    footer = f"\n\n---\n### 🗝️ Coach's Last Tip\n{coach_tip}\n\n> 💡 **참고**: {footer_note}"
    fortune_text += footer

    return {
        "status": "success",
        "fortune": fortune_text,
        "saju": saju,
        "char_count": len(fortune_text),
    }


def _generate_dynamic_coach_tip(category, context, saju):
    """카테고리별 유동적이고 데이터 기반인 코칭 팁 생성"""
    # [Fix] 공백 제거로 키 매칭 정확도 향상
    category = category.strip()

    dominant = context["dominant_god"]
    weakest = context["weakest_element"]
    strategy = context["master_strategy"]
    
    # 카테고리별 전략적 프리픽스
    prefixes = {
        "재물운": f"💰 **머니 플렉스 전략**: {dominant}의 치밀한 기질을 재테크에 투생하세요. ",
        "직업운": f"🚀 **커리어 치트키**: {dominant}의 추진력이 당신을 커리어 정점으로 이끌 것입니다. ",
        "애정운": f"💕 **러브 시그널**: 관계의 핵심은 {dominant}의 포용력과 {weakest}의 유연함입니다. ",
        "궁합": f"👩‍❤️‍👨 **케미 가이드**: 서로의 다름을 인정하는 {dominant}의 지혜가 최고의 시너지를 만듭니다. ",
        "건강운": f"💪 **HP 관리 비법**: 당신의 기운을 정화하는 {weakest} 에너지를 일상에 채우세요. ",
        "평생사주": f"🧬 **본캐 마스터 플랜**: {dominant}의 기세를 믿고 장기적인 {strategy}를 실전하세요. ",
        "신년운세": f"🔮 **연간 스포일러**: 2026년 화(火)의 기운을 {dominant}의 지혜로 제어하며 승리하세요. ",
        "MBTI분석": f"🧠 **뇌 구조 동기화**: {saju.get('mbti', '자신')}의 성향과 {dominant}의 사주 DNA가 만나는 지점이 당신의 필승 구역입니다. ",
        "개운법": f"🍀 **행운 부스터**: {weakest}의 기운을 상징하는 행동과 사물이 당신의 운을 극대화합니다. "
    }
    
    prefix = prefixes.get(category, f"✨ **맞춤형 가이드**: {dominant}의 기운을 활용하세요. ")
    
    # [Fix] 데이터 기반 동적 본문 (카테고리별 다변화)
    bodies = {
        "재물운": f"단기적인 수익보다는 {dominant}의 안목으로 자산의 기초를 다지세요. {weakest}의 기운이 보태질 때 재물 그릇이 커집니다.",
        "직업운": f"결과에 조급해하기보다 {strategy}를 루틴으로 만드세요. 작은 성취가 모여 {dominant}의 거대한 성공을 만듭니다.",
        "애정운": f"상대방의 속도에 맞추는 {weakest}의 유연함이 필요합니다. {dominant}의 진심은 행동으로 보여줄 때 가장 강력합니다.",
        "궁합": f"서로의 오행이 충돌할 때는 {strategy}를 통해 완충지대를 만드세요. 인내하는 {dominant}의 지혜가 시너지를 깨웁니다.",
        "건강운": f"신체 에너지가 {weakest}에 집중될 수 있도록 휴식을 배치하세요. {dominant}의 강인함도 결국 휴식에서 나옵니다.",
        "평생사주": f"{strategy}를 인생의 나침반으로 삼으세요. {dominant}의 기질을 꾸준히 반복하는 것이 운명을 개척하는 가장 확실한 길입니다.",
        "신년운세": f"올해의 변화는 {dominant}의 철저한 대비로부터 시작됩니다. {weakest}의 기운을 보완하는 취미를 가져보세요.",
        "MBTI분석": f"{saju.get('mbti', '자신')}의 사회적 가면과 {dominant}의 사주적 본질이 조화를 이룰 때, 당신의 매력은 극대화됩니다.",
        "개운법": f"일상의 작은 행동(풍수, 색상) 하나가 {weakest}의 운을 깨웁니다. {strategy}를 몸에 익히는 습관을 들여보세요."
    }
    
    body = bodies.get(category)
    
    # [Validation] Ensure body matches category context
    if not body:
         body = f"{strategy}를 꾸준히 반복하는 것이 운의 흐름을 바꾸는 가장 빠른 방법입니다. 오늘부터 작은 실행을 시작하세요."
    
    # [Keyword Assertion Debug] (Optional: can be removed in prod)
    # keywords = {
    #     "재물운": ["자산", "수익", "돈", "재물"],
    #     "직업운": ["커리어", "성공", "루틴", "결과"],
    #     "애정운": ["상대방", "마음", "진심", "유연함"]
    # }
    # required = keywords.get(category, [])
    # if required and not any(k in body for k in required):
    #     body += f" (Note: {category}에 맞는 보완이 필요합니다.)"

    return prefix + body


# ── 도움 함수: 신규 블록들 (Fortune Generator 내부 정의 혹은 스텁) ──
def build_wealth_portfolio_analysis(saju):
    # 포트폴리오 심층 가이드 스텁
    return "#### 💎 전략적 자산 포트폴리오 구성\n- 코어 자산(70%): 부동산/국채 위주 안정성 확보\n- 위성 자산(30%): 기술주/신산업 등 고수익 자산 배치\n"

def build_career_performance_guide(saju, profile):
    return "#### 🚀 비즈니스 퍼포먼스 가이드\n- 협상 시: 경청 후 데이터로 압도\n- 업무 시: 오전 10시-11시 사이 핵심 결단 지향\n"

def build_relationship_timing_chart(saju):
    return "#### ⏳ 인연의 타이밍 분석\n- 2026년 하반기: 새로운 귀인이 나타날 확률 85%\n- 주의 시기: 월운이 극으로 치닫는 시기 소통 주의\n"

def build_preventive_health_rituals(saju):
    return "#### 🍵 홀리스틱 건강 관리 비방\n- 부족한 오행 강화 체조 매일 15분\n- 명상과 호흡을 통한 과잉 기운 발산\n"


def get_mbti_synergy(user_mbti, target_mbti, relation_code):
    """MBTI 융합 시너지 문장 생성"""
    if not user_mbti or not target_mbti:
        return "MBTI 정보가 입력되면 더욱 정교한 성격 케미 분석이 가능합니다."
    
    # 전략적 하이브리드 문장 DB (예시)
    synergies = {
        ("ENTP", "INFJ"): "당신의 ENTP적 호기심이 상대방의 INFJ적 신비주의를 자극하여 끝없는 영감을 주고받는 관계가 됩니다.",
        ("ENTP", "ESTJ"): "아이디어와 실행력의 폭발적 만남! 다만 박민수님의 파격이 최현석님의 규율과 충돌할 수 있으니 주의하세요.",
        ("ENFP", "INTJ"): "자유로운 영혼의 에너지가 냉철한 분석력을 만나 완벽한 상보적 관계를 형성합니다.",
        ("INFP", "ENFJ"): "진심 어린 공감과 따뜻한 리더십이 만나 서로를 성장시키는 치유의 관계가 됩니다."
    }
    
    pair = (user_mbti, target_mbti)
    if pair in synergies:
        return synergies[pair]
    
    # 동적 생성 (지표별)
    traits = []
    if user_mbti[0] != target_mbti[0]: traits.append("외향과 내향의 상호보완")
    if user_mbti[1] == target_mbti[1]: traits.append("세상을 보는 관점의 일치")
    if user_mbti[2] == 'T' and target_mbti[2] == 'F': traits.append("이성과 감성의 완벽한 밸런스")
    
    summary = " / ".join(traits) if traits else "서로의 다름을 인정할 때 빛나는 관계"
    return f"{summary}: 당신의 {user_mbti} 기질과 상대의 {target_mbti} 기질이 묘한 텐션을 만듭니다."

def _build_star_premium_report(user_saju, target_saju, relation_code, target_name, target_mbti):
    """
    [Premium] STAR 전용 심층 리포트 생성기
    4가지 필수 섹션 구성
    """
    from saju_calculator import get_ten_god, STEM_ELEMENT, BRANCH_ELEMENT, BRANCH_ANIMAL
    
    user_day_stem = user_saju["day_stem"]
    target_day_stem = target_saju["day_stem"]
    target_day_branch = target_saju["pillars"]["day"]["branch"]
    ten_god = get_ten_god(user_day_stem, target_day_stem)
    user_mbti = user_saju.get("mbti", "Unknown")
    
    # 1. Target Focus: 이 사람의 본질
    stem_desc = {
        "갑": "당당하고 추진력 있는 '거목'", "을": "유연하고 생명력 넘치는 '덩굴'",
        "병": "화려하고 열정적인 '태양'", "정": "따뜻하고 섬세한 '등불'",
        "무": "묵직하고 포용력 있는 '대지'", "기": "부드럽고 생산적인 '전원'",
        "경": "강단 있고 정의로운 '원석'", "신": "섬세하고 빛나는 '보석'",
        "임": "깊고 포용력 있는 '바다'", "계": "맑고 지혜로운 '이슬'"
    }.get(target_day_stem, "신비로운 기운")
    
    focus_text = f"**{target_name}님**은 사주상 **{target_day_stem}({stem_desc})**의 기운을 타고났습니다. "
    focus_text += f"{target_mbti} 특유의 기질이 더해져, 겉으로는 화려해 보여도 내면에는 자신만의 확고한 철학과 때로는 고독한 고뇌를 즐기는 **'입체적 페르소나'**를 지니고 있죠. "
    focus_text += f"무대 위의 아우라는 우연이 아닌, {BRANCH_ANIMAL[target_day_branch]}의 영민함이 깃든 결과입니다."

    # 2. Like & Dislike: 취향 저격 가이드 (오행/MBTI 믹스)
    target_elems = target_saju["elements"]
    weakest = target_elems["weakest"]
    strongest = target_elems["strongest"]
    
    likes = [
        f"**{weakest} 기운의 힐링**: 부족한 {weakest} 기운을 채워주는 자연스러운 만남이나 아이템",
        f"**지적 대화**: {target_mbti}적 호기심을 자극하는 깊이 있는 주제",
        "**프라이빗한 감성**: 북적이는 곳보다 둘만의 결이 느껴지는 아지트"
    ]
    hates = [
        f"**{strongest}의 과부하**: 이미 넘치는 {strongest} 기운을 더 압박하는 급한 태도",
        "**가벼운 언행**: 자신의 가치관을 존중하지 않는 무례함",
        "**통제와 구속**: 자유로운 영혼을 가두려는 모든 시도"
    ]
    
    # 3. Vibe Check: 나와의 케미 서사
    synergy = get_mbti_synergy(user_mbti, target_mbti, "STAR")
    vibe_text = f"당신({user_day_stem})과 상대방({target_day_stem})은 **'{ten_god}'**의 관계로 연결되어 있습니다. "
    if ten_god in ["정인", "편인"]: vibe_text += "상대방이 당신에게 정신적 영감을 주는 '뮤즈'와 같은 존재군요. "
    elif ten_god in ["식신", "상관"]: vibe_text += "당신이 상대방의 잠재력을 끌어올려 주는 '프로듀서' 같은 텐션입니다. "
    else: vibe_text += "서로의 에너지가 폭발적으로 교차하며 새로운 세계를 여는 '러닝 메이트' 바이브입니다. "
    vibe_text += f"\n\n{synergy}"

    # 4. Real Signal: 관계 공략팁
    comm_style = "텍스트(톡)" if target_mbti[2] == 'T' else "대화(감성 보이스)"
    tactics = [
        f"**소통 공식**: {comm_style} 위주로, 결과보다는 '과정의 공감'을 담아 메시지를 던지세요.",
        "**화해의 기술**: 논리적 분석보다는 '내가 네 편임'을 확실히 인지시켜주는 지지 선언이 먼저입니다.",
        "**갓생 루틴**: 함께 전시를 보거나 새로운 취미를 공유하며 '성장하는 자극'을 주는 것이 핵심입니다."
    ]

    return f"""
### 🌟 [PREMIUM SECTION] {target_name}님과의 STAR 시그널 리포트

#### [1. Target Focus: 이 사람의 본질]
> "{focus_text}"
#본질분석 #{target_mbti} #페르소나

#### [2. Like & Dislike: 취향 저격 가이드]
**✅ Green Flags (이런 것에 끌려요)**
- {" / ".join(likes)}

**❌ Red Flags (이런 건 힘들어요)**
- {" / ".join(hates)}
#취향저격 #GreenFlag #공략법

#### [3. Vibe Check: 나와의 케미 서사]
{vibe_text}
#운명적서사 #티키타카 #케미폭발

#### [4. Real Signal: 관계 공략팁]
{"\n".join([f"- {t}" for t in tactics])}
#실전팁 #갓생메이트 #시그널캐치

---
"""

if __name__ == "__main__":
    result = generate_fortune("1980-05-15", "14:00", "재물운", {"name": "박철세", "job": "보험계리사", "mbti": "ISTJ", "blood_type": "AO"})
    print(result["fortune"])


def _build_relationship_context(user_saju, target_date, target_time, relation_code, target_name, target_mbti, category="전체", target_gender='U'):
    """
    [Phase 2] 문맥 인식 관계 분석 로직 (Gen Z Update)
    - 나와 상대방의 일간(Day Stem) 십성 관계 분석
    - Gender(성별) 정보를 활용한 뉘앙스 조정 (Option)
    - DB의 interpretation_context 조회
    - 긍정 강화(Positive Spin) 적용
    """
    from saju_calculator import calculate_full_saju, get_ten_god
    from saju_db import query_interpretation_context
    
    # [Fix] Private Mode 또는 데이터 부족 시 관계 리포트 생성 안함
    if not target_date or relation_code == 'private' or not target_name:
        return ""
    
    # [Logic Fix] 비즈니스/재물/직업 등 연관 없는 테마에서는 '절대' 관계 리포트 생성 금지 (Secret Code 방지)
    # 애정운, 궁합, 러브시그널, STAR 관계가 아니면 빈 문자열 반환
    if category not in ['애정운', '궁합', '러브시그널'] and relation_code != 'STAR':
        return ""


    # 1. 상대방 사주 계산
    try:
        target_saju = calculate_full_saju(target_date, target_time)
    except:
        return "" # 계산 실패 시 빈 문자열 반환

    # 2. 십성 관계 도출 (User 기준 Target의 십성)
    user_day_stem = user_saju["day_stem"]
    target_day_stem = target_saju["day_stem"]
    ten_god = get_ten_god(user_day_stem, target_day_stem)
    
    # 십성 영문 매핑 (DB 조회용)
    ten_god_map_en = {
        "비견": "Friend", "겁재": "RobWealth", 
        "식신": "EatingGod", "상관": "HurtingOfficer",
        "편재": "IndirectWealth", "정재": "DirectWealth", 
        "편관": "SevenKillings", "정관": "DirectOfficer", 
        "편인": "IndirectResource", "정인": "DirectResource"
    }
    ten_god_en = ten_god_map_en.get(ten_god, "Friend")
    
    # 3. DB에서 문맥별 해석 조회
    db_result = query_interpretation_context("TenGods", ten_god_en, relation_code)
    
    # 4. 결과 텍스트 생성
    if db_result:
        advice = db_result["advice_text"]
        price = db_result["price_to_unlock"]
        is_positive = db_result["is_positive"]
    else:
        # DB에 데이터가 없을 경우 기본 폴백 로직
        advice = f"상대방은 당신에게 '{ten_god}'의 기운을 뿜어내고 있습니다. 서로의 다름을 케미로 승화시키는 공략법이 필요합니다."
        price = 500 # [Demo] 기본적으로 잠금 기능 활성화
        is_positive = 1

    # 5. Fandom/Star Premium Branch (Phase 3 Update)
    if relation_code == "STAR":
        return _build_star_premium_report(user_saju, target_saju, relation_code, target_name, target_mbti)

    # 5. Fandom/Star 긍정 강화 로직 (텐션 Up) - Normal fallback
    if relation_code == "STAR" and not is_positive:
        advice = f"[🔥 텐션 UP] {advice} \n\n✨ 하지만 걱정 NO! 이 긴장감이 오히려 서로를 떡상시키는 '자극제'가 될 수 있습니다. 당신과 {target_name}님은 환상의 티키타카 파트너입니다!"

    # [Phase 10] Tema-specific lead-in text
    lead_in_map = {
        "LOVER": "🗝️ 상대방의 숨겨진 사랑법과 집착 포인트(T/F)에 따른 공략 공식...",
        "BOSS": "🗝️ 상사와의 소통 효율을 200% 올리는 '데이터 기반' 심리 공략법...",
        "FRIEND": "🗝️ 베프의 속마음과 당신을 보는 진짜 시그널...",
        "PEER": "🗝️ 동료와의 협업 시너지를 위한 결정적 한 방...",
        "STAR": "🗝️ 최애와의 운명적 연결고리와 성덕이 되는 필승 전략..."
    }
    lead_in = lead_in_map.get(relation_code, "🗝️ 상대방의 숨겨진 성격과 공략 공식을 공개합니다.")

    # 6. 블러(Blur) 처리 준비 (테스트 중이므로 내용 노출)
    # blur_class = "blurred-text" if price > 0 else ""
    blur_class = "" # Revealed for testing as requested
    unlock_btn = f"""
<div class="lead-in-text">{lead_in}</div>
<button class='unlock-btn' onclick='unlockContent({price})'>🗝️ {target_name}의 비밀 코드 열기 ({price}원)</button>
""" if price > 0 else ""
    
    relation_emoji = {
        "LOVER": "💕", "BOSS": "💼", "FRIEND": "🤝", "PEER": "👯", "STAR": "🌟"
    }.get(relation_code, "🔗")

    # 7. MBTI Synergy Sentence (Hybrid)
    user_mbti = user_saju.get("mbti", "") # user_saju might not have mbti if it's from calculate_full_saju
    # But wait, user_mbti is better provided from params if available.
    # For now, let's use a generic MBTI synergy if possible.
    
    mbti_synergy = get_mbti_synergy(user_saju.get("mbti", ""), target_mbti, relation_code)

    return f"""
### 🧪 {relation_emoji} {relation_code} 케미 리포트: {target_name}님과의 시그널
**⚡ 핵심 시그널:** {ten_god} ({ten_god_en})

> "상대방은 당신에게 **{ten_god}** 바이브를 줍니다."

**[🧠 MBTI 하이브리드 인사이트]**
{mbti_synergy}

**[🔥 공략 치트키]**
<div class="advice-box {blur_class}">
{advice}
</div>{unlock_btn}

---
"""
