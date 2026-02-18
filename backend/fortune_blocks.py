"""
운세 확장 블록 모듈
- 맥락적 혈액형/MBTI 교차분석
- 혈액형/MBTI 전용 카테고리 생성
- 대운/나이대별 해석 블록
"""
from saju_db import query_stem, query_branch, query_ten_god, query_element, query_blood_type, query_mbti, query_classical_wisdom
from saju_calculator import STEM_ELEMENT, BRANCH_ELEMENT, BRANCH_ANIMAL


# ────────────────────────────────
# 맥락적 교차분석 (모든 카테고리에 삽입)
# ────────────────────────────────

def build_contextual_cross_analysis(category, saju, profile):
    """카테고리별 MBTI 맥락적 교차분석 블록 (~800자)"""
    # [Phase 8b] Blood Type removed as per user request
    mbti_type = profile.get("mbti", "")
    
    if not mbti_type:
        return ""
    
    mbti = query_mbti(mbti_type) if mbti_type else None
    
    dominant_god = _get_dominant(saju)
    god = query_ten_god(dominant_god)
    day_elem = saju["day_stem_element"]
    
    header = "### 🧠 사주 × MBTI 교차분석"
    lines = [f"{header}\n"]
    
    # MBTI 맥락 연결
    if mbti:
        lines.append(f"#### 🧠 {mbti['mbti']}({mbti['title']}) × {dominant_god}({god['hanja']})\n")
        
        if category in ["재물운", "신년운세"]:
            lines.append(f"{mbti['career_advice']}\n")
            lines.append(f"MBTI의 **{mbti['saju_god']}** 기질이 재물 관리에 미치는 영향: ")
            if "정" in mbti['saju_god']:
                lines.append(f"안정적이고 계획적인 재테크에 강합니다. 장기 투자와 적금형 자산 운용에서 빛을 발합니다.\n")
            else:
                lines.append(f"기회를 포착하는 직감이 뛰어납니다. 다만 충동적 결정을 피하고 데이터 기반 판단을 병행하세요.\n")
        
        elif category in ["애정운", "궁합"]:
            lines.append(f"{mbti['personality']}\n")
            lines.append(f"사주의 {dominant_god} 기운과 MBTI {mbti['mbti']}의 관계 스타일이 합쳐지면, ")
            if mbti['mbti'][0] == 'E':
                lines.append(f"적극적으로 인연을 만들어가는 타입입니다. 사교 모임이나 활동적인 만남에서 좋은 인연이 기다립니다.\n")
            else:
                lines.append(f"깊고 의미 있는 관계를 추구하는 타입입니다. 소규모 모임이나 취미 활동에서 진정한 인연을 만날 수 있습니다.\n")
        
        elif category in ["직업운"]:
            lines.append(f"{mbti['career_advice']}\n")
            if mbti['saju_god'] == dominant_god:
                lines.append(f"> 🎯 MBTI와 사주가 **같은 십성({dominant_god})**을 가리키고 있어, "
                           f"이 방향의 커리어에서 타고난 재능을 최대로 발휘할 수 있습니다!\n")
            else:
                lines.append(f"> 🔄 MBTI({mbti['saju_god']})와 사주({dominant_god})가 **서로 다른 십성**을 가리킵니다. "
                           f"두 가지 강점을 모두 활용하면 다재다능한 전문가로 성장할 수 있습니다.\n")
        
        elif category in ["건강운"]:
            lines.append(f"MBTI {mbti['mbti']} 유형의 스트레스 패턴을 사주와 교차 분석하면:\n")
            if mbti['mbti'][2] == 'T':
                lines.append(f"- 논리적 사고 과부하로 인한 **두통, 목 결림**에 주의하세요\n"
                           f"- 감정 표현을 자주 하여 내면의 압력을 해소하는 것이 건강에 좋습니다\n")
            else:
                lines.append(f"- 감정적 에너지 소모로 인한 **소화불량, 불면증**에 주의하세요\n"
                           f"- 객관적 분석 시간을 갖고 감정과 거리두기 연습이 도움됩니다\n")
        
        else:
            lines.append(f"{mbti['personality']}\n")
            lines.append(f"**커리어 시너지**: {mbti['career_advice']}\n")
    
    return "\n".join(lines)


# ────────────────────────────────
# 대운/나이대별 해석 (~600자)
# ────────────────────────────────

def build_life_stages(saju, profile):
    """대운과 나이대별 해석 블록"""
    day_elem = saju["day_stem_element"]
    dominant = _get_dominant(saju)
    god = query_ten_god(dominant)
    
    lines = ["### 📈 인생 주기별 운세 흐름\n"]
    
    # 대운 흐름 (간략)
    lines.append("#### 대운(大運) 10년 주기 흐름\n")
    
    cycle_map = {
        "목": [("초년(~25세)","수(水)의 자양을 받아 성장하는 시기. 학업과 기초 역량을 쌓는 것이 핵심입니다. 부모님의 지원이 큰 힘이 됩니다."),
               ("청년(25~35세)","목(木)의 기운이 왕성해지며 사회에 뿌리를 내리는 시기. 도전과 개척의 에너지가 넘칩니다."),
               ("장년(35~50세)","화(火)로 전환되며 성과가 빛나는 시기. 재능을 발휘하고 사회적 인정을 받는 전성기입니다."),
               ("중년(50~65세)","토(土)의 안정기에 접어듭니다. 그동안의 경험을 바탕으로 후진을 양성하고 지혜를 나누세요."),
               ("노년(65세~)","금(金)의 결실기. 인생의 열매를 수확하고 여유로운 삶을 즐기는 시기입니다.")],
        "화": [("초년(~25세)","목(木)의 에너지를 받아 열정이 점점 커지는 시기. 다양한 경험을 통해 자신의 길을 찾으세요."),
               ("청년(25~35세)","화(火) 기운이 극에 달하는 시기. 열정과 활동력으로 세상에 이름을 알릴 수 있습니다."),
               ("장년(35~50세)","토(土)로 전환되며 안정을 추구하는 시기. 가정과 사업의 기반을 탄탄히 다지세요."),
               ("중년(50~65세)","금(金)의 수확기. 재물의 결실을 맺고 자산을 체계적으로 관리하는 것이 중요합니다."),
               ("노년(65세~)","수(水)의 지혜기. 깊은 통찰로 주변에 빛을 비추는 존경받는 어른이 됩니다.")],
        "토": [("초년(~25세)","화(火)의 지원을 받아 따뜻한 환경에서 성장합니다. 안정적인 교육 환경이 중요합니다."),
               ("청년(25~35세)","토(土) 기운이 강해지며 사회적 기반을 다지는 시기. 부동산이나 안정적 자산에 관심을 가지세요."),
               ("장년(35~50세)","금(金)으로 전환되며 성과가 구체화됩니다. 전문성이 인정받고 수입이 안정됩니다."),
               ("중년(50~65세)","수(水)의 변화기. 새로운 도전이나 전환점이 올 수 있으니 유연하게 대처하세요."),
               ("노년(65세~)","목(木)의 재생기. 새로운 취미나 봉사활동으로 활력을 유지하세요.")],
        "금": [("초년(~25세)","토(土)의 보호를 받아 안정적으로 성장합니다. 규율과 체계 속에서 역량을 키우세요."),
               ("청년(25~35세)","금(金) 기운이 강해지며 결단력과 추진력이 극대화됩니다. 전문가의 길을 걷기 시작합니다."),
               ("장년(35~50세)","수(水)로 전환되며 지혜가 깊어지는 시기. 판단력이 빛을 발하며 리더로 성장합니다."),
               ("중년(50~65세)","목(木)의 확장기. 새로운 분야로의 진출이나 투자 확대가 유리합니다."),
               ("노년(65세~)","화(火)의 빛의 시기. 인생의 지혜가 빛나며 주변을 밝히는 존재가 됩니다.")],
        "수": [("초년(~25세)","금(金)의 지원을 받아 지적 호기심이 왕성한 시기. 학업에서 특히 두각을 나타냅니다."),
               ("청년(25~35세)","수(水) 기운이 극대화되어 지혜와 통찰력이 넘칩니다. 전략적 판단이 빛을 발합니다."),
               ("장년(35~50세)","목(木)으로 전환되며 그동안의 역량이 결실을 맺습니다. 사업 확장이나 승진의 기회가 옵니다."),
               ("중년(50~65세)","화(火)의 활력기. 사회적으로 존경받고 영향력이 커지는 시기입니다."),
               ("노년(65세~)","토(土)의 안정기. 마음의 평화를 찾고 여유로운 삶을 즐기는 시기입니다.")],
    }
    
    stages = cycle_map.get(day_elem, cycle_map["목"])
    for period, desc in stages:
        lines.append(f"- **{period}**: {desc}")
    
    # 향후 3년 핵심 키워드 (보너스 섹션)
    lines.append("\n#### 🎯 향후 3년(2026-2028) 핵심 전략\n")
    lines.append(f"현재 사주상 **{dominant}**의 기운이 강하게 작용하는 시기입니다. {god['keyword']}을(를) 중심으로 삶의 방향을 설정하세요.\n")
    
    focus_map = {
        "비견": "자아 확립과 독립적 기반 구축에 집중하세요. 새로운 동료를 만나거나 자신만의 브랜드를 런칭하기 좋은 시기입니다.",
        "겁재": "강한 승부욕이 도약의 발판이 됩니다. 경쟁 직종이나 고수익 투자에 도전해볼 만하지만 지출 관리도 병행해야 합니다.",
        "식신": "표현과 창작의 즐거움을 누리세요. 연구 개발이나 교육 분야에서 큰 성취가 예상됩니다. 건강 관리를 잊지 마세요.",
        "상관": "혁신과 변화를 주도할 때입니다. 기존의 틀을 깨고 새로운 아이디어로 승부하면 커다란 전환점이 찾아옵니다.",
        "편재": "재물 기회가 크게 찾아오는 해입니다. 적극적인 영업과 투자 확대에 유리하며, 활동 범위를 넓히는 것이 신의 한 수가 됩니다.",
        "정재": "성실과 신용이 곧 재산입니다. 안정적인 수입원을 확보하고 정밀한 자산 관리를 통해 기반을 단단히 굳힐 시기입니다.",
        "편관": "명예와 사회적 책임이 따르는 시기입니다. 리더십을 발휘하여 어려운 과제를 해결하면 지도자급으로 부상할 수 있습니다.",
        "정관": "승진과 자격 취득의 문이 열립니다. 조직 내에서 확실한 입지를 굳히고 시스템에 기반한 성취를 이룰 수 있는 길운입니다.",
        "편인": "지적 성장에 몰입하세요. 독특한 분야의 공부나 영적 통찰이 앞으로의 10년을 먹여 살릴 핵심 자산이 됩니다.",
        "정인": "후원과 도움의 손길이 끊이지 않습니다. 안정적인 지지 기반 위에서 학문적 성취나 자격증 취득에 최고의 시기입니다."
    }
    
    lines.append(f"> 🚀 **핵심 행동 지침**: {focus_map.get(dominant, focus_map['비견'])}\n")
    lines.append("인생의 큰 흐름은 파도와 같습니다. 높은 운을 탈 때는 과감하게, 조정을 받을 때는 내실을 다지는 지혜가 필요합니다. 당신의 사주는 현재 **상승하는 파도** 위에 있으니 자신감을 가지고 정진하십시오.\n")
    
    return "\n".join(lines)


# ────────────────────────────────
# 실천 가이드 (~400자)
# ────────────────────────────────

def build_daily_practice(saju, advice):
    """일상 실천 가이드 대폭 확장 (~800자)"""
    weakest = saju["elements"]["weakest"]
    elem = query_element(weakest)
    
    lines = [
        "### 🎯 행운을 부르는 24시간 실천 리추얼\n",
        "운세는 단순히 기다리는 것이 아니라 스스로 만들어가는 에너지의 흐름입니다. 사주에서 부족한 기운을 일상에서 채우는 '개운 루틴'을 통해 삶의 질을 획기적으로 높여보세요.\n",
        "| 시간대 | 실천 가이드 | 기대 효과 |",
        "|:---|:---|:---|",
        f"| 🌅 **기상 직후** | {advice['color']} 계열의 소품을 바라보며 긍정 확언 | 잠재의식을 깨우고 행운을 예열 |",
        f"| 🍽️ **의식주 실천** | {advice['food']} 포함 식사와 {advice['color']} 의상 착용 | 부족한 **{weakest}** 에너지 직접 보완 |",
        f"| 💼 **성공의 방위** | 업무나 미팅 시 **{advice['direction']}** 쪽을 향해 앉기 | 외부 에너지의 올바른 흡수와 순환 |",
        f"| 🏃 **체력과 활력** | 하루 20분 {advice['activity']} 루틴 실천 | 정체된 운의 흐름을 역동적으로 전환 |",
        f"| 🔢 **숫자의 비방** | 숫자 **{advice['number']}**을 비번이나 도어락에 활용 | 주변 사물과의 에너지 주파수 일치 |",
        "",
        "#### 🌈 성공을 위한 마인드셋\n",
        f"부족한 **{weakest}({elem['hanja']})**의 기운은 심리적으로 **{elem['emotion']}**의 조절과 직결됩니다. ",
        "매일 잠들기 전 5분간 감사 일기를 작성하며 마음의 평온을 유지하세요. ",
        f"당신의 일간인 {saju['day_stem']}의 에너지가 가장 맑게 투영될 때, 사주상의 모든 길운이 폭발적으로 작용하기 시작합니다.\n",
        f"> 📌 **개운(開運) 포인트**: 운을 여는 열쇠는 '꾸준함'입니다. 거창한 목표보다 위 표의 내용 중 **딱 한 가지만이라도 매일 실천**해보세요. 21일 뒤 당신은 완전히 달라진 행운의 변화를 체감하게 될 것입니다.\n"
    ]
    return "\n".join(lines)


# ────────────────────────────────
# 고전 명리 전문 해석 블록 (~600자)
# ────────────────────────────────

def build_classical_wisdom_section(saju, profile):
    """고전 명리(적천수, 자평진전 등) 원문 및 해석 블록"""
    # 순환 참조 방지를 위해 직접 계산
    god_count = saju.get("god_count", {})
    dominant = max(god_count, key=god_count.get) if god_count else "비견"
    day_elem = saju["day_stem_element"]
    
    # 데이터 조회
    god_wisdom = query_classical_wisdom("ten_gods", dominant)
    elem_wisdom = query_classical_wisdom("elements", day_elem)
    
    lines = [
        "### 📜 명리 고전 전문 해석 (Classical Insights)\n",
        "수천 년간 이어져 온 명리학의 정수인 **적천수(滴天髓)**와 **자평진전(子平眞詮)** 등 고전 서적을 바탕으로 당신의 운명을 심층 분석합니다.\n"
    ]
    
    if god_wisdom:
        lines.extend([
            f"#### 1. {dominant}에 관한 고전의 가르침\n",
            f"> **원문(原文)**: *{god_wisdom['original_text']}*\n",
            f"> **출처**: {god_wisdom['source']}\n",
            f"\n**현대적 해석**: {god_wisdom['modern_interpretation']}\n",
            f"당신의 삶에서 {dominant}의 기운이 작용하는 방식은 고전에서 강조하는 바와 같이 매우 중대한 의미를 지닙니다. "
            f"이러한 에너지를 어떻게 중화하고 승화시키느냐가 평생의 성취를 좌우하는 핵심 열쇠가 됩니다.\n"
        ])
        
    if elem_wisdom:
        lines.extend([
            f"#### 2. 일간 {day_elem} 오행의 본질적 기질\n",
            f"> **원문(原文)**: *{elem_wisdom['original_text']}*\n",
            f"> **출처**: {elem_wisdom['source']}\n",
            f"\n**현대적 해석**: {elem_wisdom['modern_interpretation']}\n",
            f"만물의 조화로운 순환 속에서 당신이 타고난 {day_elem}의 기운은 위의 구절처럼 특별한 개척의 사명을 띠고 있습니다.\n"
        ])
        
    lines.extend([
        "#### 3. 결론: 고전이 전하는 지혜\n",
        "명리는 단순히 미래를 예측하는 도구가 아니라, 하늘의 이치를 깨닫고 자신을 수양하는 학문입니다. ",
        "고전의 가르침을 통해 자신의 강점을 극대화하고 약점을 보완하는 '극기복례(克己復禮)'의 자세를 견지한다면, ",
        "어떤 험난한 운의 흐름 속에서도 반드시 평온과 번영을 찾을 수 있을 것입니다.\n"
    ])

    # 동적 푸터 생성
    footer_parts = []
    if profile.get('mbti'):
        footer_parts.append("현대적 MBTI")
    if profile.get('blood_type'):
        footer_parts.append("혈액형")
    
    if footer_parts:
        footer_text = f"이 분석은 {profile.get('name','사용자')}님의 사주와 {'/'.join(footer_parts)}을(를) 고려하여 고전의 원칙을 재해석한 결과입니다."
    else:
        footer_text = f"이 분석은 {profile.get('name','사용자')}님의 사주를 바탕으로 고전의 원칙을 재해석한 결과입니다."

    lines.append(f"\n> 💡 **참고**: {footer_text}\n")
    return "\n".join(lines)


# ────────────────────────────────
# 혈액형 전용 카테고리 (~2500자)
# ────────────────────────────────

# gen_blood_category removed as per user request (Phase 8b)


# ────────────────────────────────
# [Expert Analysis] 전문 자력 기반 심층 전략
# ────────────────────────────────

def build_wealth_strategy(saju, profile):
    """심층 재물운 및 자산 관리 전략 (~1000자)"""
    from saju_db import query_pillar_60
    dominant = _get_dominant(saju)
    weakest = saju["elements"]["weakest"]
    strongest = saju["elements"]["strongest"]
    
    # 일주(Day Pillar) 기반 심층 해석 추가
    pillar_name = saju["pillars"]["day"]["stem"] + saju["pillars"]["day"]["branch"]
    pillar_info = query_pillar_60(pillar_name)
    
    lines = ["### 💰 전문적 재물운 & 자산 포트폴리오 전략\n"]
    lines.append(f"성공한 투자자의 관점에서 {profile.get('name', '고객')}님의 **{pillar_name}(日柱)** 원국을 분석한 결과, 다음과 같은 자산 형성 로드맵이 도출됩니다.\n")
    
    # 1. 일주 기반 재물 기질
    if pillar_info:
        lines.append(f"#### 1. {pillar_name} 기운의 재물 DNA\n")
        lines.append(f"> {pillar_info['wealth_strategy']}\n")
    else:
        lines.append("#### 1. 타고난 '부(富)의 그릇' 진단\n")
        if dominant in ["편재", "정재"]:
            lines.append(f"정밀한 자금 설계가 강점인 **재성(財星) 주도형** 자산가입니다. 돈의 흐름을 읽는 감각이 탁월하며, 실질적인 수익 창출에 최적화되어 있습니다.\n")
        elif dominant in ["식신", "상관"]:
            lines.append(f"아이디어와 기술이 곧 부가 되는 **식상생재(食傷生財)형**입니다. 자신만의 시스템이나 브랜드를 통해 자동 수익을 창출하는 능력이 뛰어납니다.\n")
        else:
            lines.append(f"주변 환경과 명예를 활용하여 부를 일구는 스타일입니다. 안정적인 시스템 하에서 자산을 증식하는 것이 유리합니다.\n")

    # 2. 투자 포트폴리오
    lines.append(f"\n#### 2. 오행 기반 맞춤 투자 인덱스\n")
    asset_map = {
        "목": "신생 성장주, 교육, 친환경 에너지",
        "화": "IT/반도체, 엔터테인먼트, 가상자산",
        "토": "실물 부동산, 전통적 가치주, 금 거래",
        "금": "채권, 배당주, 안정적 금융 인프라",
        "수": "유통/물류, 수입/수출, 배당성장주"
    }
    lines.append(f"- **공격적 포트폴리오(기세 활용)**: {asset_map.get(strongest)} (강점 극대화)\n")
    lines.append(f"- **방어적 포트폴리오(기운 보완)**: {asset_map.get(weakest)} (리스크 분산)\n")
    
    return "\n".join(lines)


# ────────────────────────────────
# [Special Analysis] 비즈니스 포지셔닝 및 커리어 로드맵 (Career Pathmap)
# ────────────────────────────────

def build_career_pathmap(saju):
    """비즈니스 전략가 관점의 커리어 로드맵 (~800자)"""
    from saju_db import query_pillar_60
    dominant = _get_dominant(saju)
    god = query_ten_god(dominant)
    
    # 일주(Day Pillar) 기반 심층 해석 추가
    pillar_name = saju["pillars"]["day"]["stem"] + saju["pillars"]["day"]["branch"]
    pillar_info = query_pillar_60(pillar_name)
    
    lines = ["### 💼 비즈니스 포지셔닝 및 커리어 로드맵\n"]
    
    if pillar_info:
        lines.append(f"#### 🚀 {pillar_name}의 비즈니스 퍼포먼스 전략\n")
        lines.append(f"> {pillar_info['career_strategy']}\n")
    else:
        lines.append(f"당신의 사주 원국에서 추출된 **{dominant}** 에너지는 비즈니스 현장에서 강력한 무기가 됩니다.\n")
    
    org_type = {
        "관성": "체계적인 대형 조직 및 제도권 비즈니스",
        "재성": "실적 중심의 영업, 유통, 투자 현장",
        "식상": "자율적인 전문직, 창업, 아이디어 기반 조직",
        "인성": "연구, 교육, 전문 컨설팅 및 문서 중심 조직",
        "비겁": "독립적인 프리랜서, 1인 기업, 경쟁적 스포츠/영업"
    }
    
    # 카테고리 판별
    cat = "비겁"
    if dominant in ["식신", "상관"]: cat = "식상"
    elif dominant in ["편재", "정재"]: cat = "재성"
    elif dominant in ["편관", "정관"]: cat = "관성"
    elif dominant in ["편인", "정인"]: cat = "인성"
    
    lines.append(f"#### 🏢 최적의 조직 환경: **{org_type.get(cat)}**\n")
    lines.append(f"> {god['career'][:150]}...\n")
    
    return "\n".join(lines)


# ────────────────────────────────
# [Special Analysis] 관계 역학 및 인적 네트워크 전략 (Relationship Dynamics)
# ────────────────────────────────

def build_love_dynamics(saju, profile):
    """관계 역학 및 대인관계 전략 (~800자)"""
    from saju_db import query_pillar_60
    dominant = _get_dominant(saju)
    day_branch = saju["pillars"]["day"]["branch"]
    pillar_name = saju["pillars"]["day"]["stem"] + saju["pillars"]["day"]["branch"]
    pillar_info = query_pillar_60(pillar_name)
    
    lines = ["### 🤝 관계 역학 및 인적 네트워크 전략\n"]
    lines.append(f"성공적인 삶의 80%는 인간관계에서 결정됩니다. 당신의 관계 패턴을 역학적으로 분석합니다.\n")
    
    if pillar_info:
        lines.append(f"#### 🌐 {pillar_name}의 관계 메커니즘\n")
        lines.append(f"> {pillar_info['love_strategy']}\n")
    else:
        lines.append(f"#### 🌐 나의 관계 아이덴티티: **일지 {day_branch}** 기운\n")
        if day_branch in ["자", "오", "묘", "유"]:
            lines.append("- 타인의 중심이 되고 싶어 하는 리더십과 매력이 공존합니다.\n")
        elif day_branch in ["인", "신", "사", "해"]:
            lines.append("- 변화를 두려워하지 않는 역동적 관계를 지향합니다.\n")
        else:
            lines.append("- 안정과 신의를 최우선으로 하는 묵직한 관계를 형성합니다.\n")
        
    lines.append(f"📍 **네트워킹 팁**: 부족한 {saju['elements']['weakest']} 기운을 가진 인연과 협력하면 운이 배가됩니다.\n")
    
    return "\n".join(lines)


# ────────────────────────────────
# MBTI 전용 카테고리 (~2500자)
# ────────────────────────────────

def gen_mbti_category(saju, profile, advice):
    """[Phase 8b] Trendy MBTI 뇌구조(Brain Map) 심층 분석"""
    mbti_type = profile.get("mbti", "")
    if not mbti_type:
        return ["### 🧠 MZ 트렌드 MBTI 뇌구조 리포트\n", "> ⚠️ MBTI 정보를 입력해주세요.\n"]
    
    mbti = query_mbti(mbti_type)
    dominant = _get_dominant(saju)
    god = query_ten_god(dominant)
    day_elem = saju["day_stem_element"]
    
    lines = [
        f"### 🧠 MZ 트렌드 MBTI 뇌구조 리포트: {mbti_type} — {mbti['title']}\n",
        f"#### 1. 당신의 '갓생' 뇌구조 (Brain Map Insight)\n",
        f"당신의 MBTI **{mbti_type}**와 사주 주도 십성 **{dominant}**이 결합된 현재의 심리적 뇌구조입니다.\n",
        f"```mermaid\n",
        f"graph TD\n",
        f'  A["🧠 {mbti_type}의 뇌구조"] --> B["{god["keyword"]} (주도 세포: 45%)"]\n',
        f'  A --> C["{mbti["title"]} (사회적 페르소나: 25%)"]\n',
        f'  A --> D["{advice["activity"]} (도파민 생성소: 15%)"]\n',
        f'  A --> E["금전 감각 (성장 세포: 10%)"]\n',
        f'  A --> F["기타 고민 (휴식 모드: 5%)"]\n',
        f"```\n",
        f"#### 2. 핵심 세포별 심층 분석\n",
        f"**🚀 갓생 세포 ({dominant})**: 사주의 핵심 에너지가 당신의 일상을 지배합니다. 현재 당신의 뇌는 어떻게 하면 '{god['keyword']}'을(를) 현실에서 가장 힙하게 구현할지 고민 중입니다.\n",
        f"**🎭 사회적 페르소나 ({mbti_type})**: 타인에게 보여지는 당신의 모습입니다. {mbti['personality'][:150]}... 이 성향은 사주의 원형 기질을 보호하는 강력한 갑옷 역할을 합니다.\n",
        f"**⚡ 도파민 생성소 ({advice['activity']})**: 스트레스 해소와 운세 상승의 핵심 루틴입니다. 이 활동을 할 때 당신의 운은 비로소 깨어납니다.\n",
        f"#### 3. 하이브리드 성공 공식\n",
        f"MBTI의 {mbti['saju_god']} 기질과 사주의 {dominant} 기운이 만났을 때, 당신의 **현대적 성공 공식**은 다음과 같습니다:\n",
        f"> 💡 **공통 분모**: {mbti['career_advice']}\n",
        f"당신은 사주의 클래식한 지혜와 MBTI의 현대적 감각을 동시에 소유한 '하이브리드 전략가'입니다. 특히 **{mbti_type[0]}형의 에너지**와 **{dominant}의 뒷심**을 결합할 때 그 어떤 난관도 힙하게 돌파할 수 있습니다.\n",
        f"#### 4. 멘탈 케어 및 운세 부스팅 팁 🍀\n",
        f"| 구분 | MZ 맞춤 가이드 | 기대 효과 |\n",
        f"|:---|:---|:---|\n",
        f"| 🎨 컬러 | {advice['color']} 오오티디(OOTD) | 에너지 정화 및 자신감 UP |\n",
        f"| 🧭 방향 | {advice['direction']} 뷰(View) 카페 | 영감 획득 및 운세 반전 |\n",
        f"| 🍽️ 음식 | {advice['food']} 혼밥/데이트 | 스트레스 광속 해소 |\n",
        f"\n> 📌 **MZ 코치의 한 마디**: \"{mbti_type}님, 당신의 뇌구조는 이미 성공한 갓생러의 표본입니다. 사주의 흐름을 타고 자신만의 리듬으로 나아가세요. 당신의 모든 선택이 곧 행운입니다.\"\n"
    ]
    return lines


# ────────────────────────────────
# 추가 확장 블록 (6000자 달성용)
# ────────────────────────────────

def build_element_deep_analysis(category, saju, profile):
    """오행 상생/상극 심층 해석 (~800자)"""
    day_elem = saju["day_stem_element"]
    elems = saju["elements"]
    weakest = elems["weakest"]
    strongest = elems["strongest"]
    w_info = query_element(weakest)
    s_info = query_element(strongest)

    lines = ["### 🌊 오행 상생·상극 심층 해석\n"]

    # 상생 흐름
    lines.append("#### 상생(相生) 에너지 흐름\n")
    cycle = {"목":"화","화":"토","토":"금","금":"수","수":"목"}
    lines.append(f"당신의 일간 **{day_elem}**은(는) **{cycle[day_elem]}**을(를) 생(生)해줍니다. "
                 f"이는 {day_elem}의 에너지가 자연스럽게 {cycle[day_elem]}으로 흘러가며, "
                 f"표현·발산·창조의 통로가 된다는 의미입니다.\n")

    gen_by = {"목":"수","화":"목","토":"화","금":"토","수":"금"}
    lines.append(f"반대로, **{gen_by[day_elem]}**이(가) 당신에게 에너지를 공급합니다. "
                 f"{gen_by[day_elem]}의 기운을 보충하면 일간의 힘이 자연스럽게 강화됩니다.\n")

    # 상극 관계
    lines.append("#### 상극(相剋) 긴장 관계\n")
    controls = {"목":"토","화":"금","토":"수","금":"목","수":"화"}
    controlled = {"목":"금","화":"수","토":"목","금":"화","수":"토"}
    lines.append(f"일간 {day_elem}은(는) **{controls[day_elem]}**을(를) 극(剋)하여 통제하고, "
                 f"**{controlled[day_elem]}**에 의해 극을 받습니다.\n")

    if category in ["재물운","직업운","신년운세"]:
        lines.append(f"사주에서 재물(재성)은 일간이 극하는 오행입니다. "
                     f"당신의 재성은 **{controls[day_elem]}**이므로, "
                     f"{controls[day_elem]} 기운이 활성화되는 시기에 재물 기회가 찾아옵니다. ")
        if elems["count"].get(controls[day_elem], 0) >= 2:
            lines.append(f"현재 사주에 {controls[day_elem]}이(가) {elems['count'].get(controls[day_elem],0)}개로 재물 기반이 탄탄합니다.\n")
        else:
            lines.append(f"다만 사주에 {controls[day_elem]}이(가) 부족하므로, 재물 확보에 더 적극적인 노력이 필요합니다.\n")

    elif category in ["건강운"]:
        lines.append(f"건강 측면에서 {controlled[day_elem]}(극을 받는 오행)의 기운이 과하면 "
                     f"일간이 약해질 수 있습니다. {controlled[day_elem]} 기운이 강한 계절이나 환경에서는 "
                     f"특히 **{w_info['body_organ']}** 건강에 세심한 주의가 필요합니다.\n")

    elif category in ["애정운"]:
        lines.append(f"애정에서 일간이 극하는 오행({controls[day_elem]})은 남성에게 '재성(아내)'을, "
                     f"일간을 극하는 오행({controlled[day_elem]})은 여성에게 '관성(남편)'을 의미합니다. "
                     f"이 오행의 강약이 배우자와의 관계 역학에 직접 영향을 미칩니다.\n")

    # 오행 과불급 조언
    lines.append(f"\n> 🔑 **균형 포인트**: 가장 강한 **{strongest}({s_info['hanja']})**의 과잉 에너지를 "
                 f"{cycle[strongest]}(으)로 흘려보내고, 부족한 **{weakest}({w_info['hanja']})**을(를) "
                 f"{gen_by[weakest]}의 힘으로 보충하는 것이 전체 운의 조화를 이루는 핵심입니다.\n")

    return "\n".join(lines)


def build_ten_god_synergy(category, saju, profile):
    """십성 조합 시너지 해석 (~700자)"""
    god_count = saju.get("god_count", {})
    if len(god_count) < 2:
        return ""

    dominant = _get_dominant(saju)
    god = query_ten_god(dominant)
    sorted_gods = sorted(god_count.items(), key=lambda x: -x[1])

    lines = ["### ⚡ 십성 조합 시너지 분석\n"]

    if len(sorted_gods) >= 2:
        g1_name = sorted_gods[0][0]
        g2_name = sorted_gods[1][0]
        g1 = query_ten_god(g1_name)
        g2 = query_ten_god(g2_name)

        lines.append(f"사주에서 **{g1_name}({g1['hanja']})**과 **{g2_name}({g2['hanja']})**이 주축을 이룹니다.\n")

        # 조합별 시너지 해석
        combo = frozenset([g1["category"], g2["category"]])

        synergy_map = {
            frozenset(["비겁","식상"]): ("자기 역량을 끊임없이 표현하고 발산하는 조합입니다. "
                "독립적으로 자신의 기술과 재능을 세상에 알리는 것이 성공의 열쇠입니다. "
                "프리랜서, 크리에이터, 1인 미디어 등에서 빛을 발합니다."),
            frozenset(["비겁","재성"]): ("강한 자아와 재물 감각이 결합된 조합입니다. "
                "직접 사업을 운영하며 돈을 버는 것에 특화되어 있습니다. "
                "다만 주변과의 재물 분쟁에 주의하고, 파트너십보다 독자적 운영이 유리합니다."),
            frozenset(["식상","재성"]): ("재주로 돈을 버는 '식신생재(食神生財)'의 최고 조합입니다! "
                "기술·재능·아이디어를 자산으로 전환하는 능력이 탁월합니다. "
                "특허, 콘텐츠 수익, 기술 창업 등에서 큰 성과를 기대할 수 있습니다."),
            frozenset(["재성","관성"]): ("재물을 통해 사회적 지위를 얻는 조합입니다. "
                "경제적 성공이 곧 사회적 인정으로 이어지며, "
                "금융, 경영, 부동산 분야에서 높은 성취를 이룰 수 있습니다."),
            frozenset(["관성","인성"]): ("직위와 학문이 결합된 '관인상생(官印相生)' 조합입니다. "
                "조직 내에서 학력과 자격을 바탕으로 승진하며, "
                "교수, 고위 공무원, 대기업 임원의 길이 열려 있습니다."),
            frozenset(["인성","비겁"]): ("학문과 자아가 결합하여 전문가의 길을 걷는 조합입니다. "
                "깊은 지식을 바탕으로 독자적 영역을 구축하며, "
                "연구직, 박사급 전문가, 컨설턴트로서 최고의 성과를 냅니다."),
            frozenset(["식상","관성"]): ("창의성과 규율 사이에서 긴장이 존재하는 조합입니다. "
                "혁신적 아이디어를 체계적으로 실행하는 능력이 핵심입니다. "
                "기존 조직을 혁신하는 역할(CTO, 기획실장)에서 빛을 발합니다."),
            frozenset(["비겁","관성"]): ("강한 자아와 사회적 압력이 공존하는 조합입니다. "
                "도전과 경쟁 속에서 성장하며, 위기를 기회로 바꾸는 능력이 탁월합니다. "
                "스포츠, 군·경, 벤처 분야에서 성공 가능성이 높습니다."),
        }

        desc = synergy_map.get(combo, f"{g1_name}의 {g1['keyword']}와 {g2_name}의 {g2['keyword']}가 "
               f"독특한 시너지를 만들어냅니다. 두 가지 강점을 의식적으로 활용하면 다방면에서 성과를 낼 수 있습니다.")
        lines.append(f"{desc}\n")

        if category in ["직업운","재물운","평생사주"]:
            lines.append(f"**{g1_name}+{g2_name} 추천 전략**: ")
            if g1["category"] in ["식상","재성"] or g2["category"] in ["식상","재성"]:
                lines.append(f"기술과 재물이 연결되는 방향으로 커리어를 설계하세요. "
                            f"본인의 전문성을 수익화하는 것이 가장 효과적인 전략입니다.\n")
            elif g1["category"] in ["관성","인성"] or g2["category"] in ["관성","인성"]:
                lines.append(f"자격증·학위·조직 내 경력을 체계적으로 쌓아가세요. "
                            f"안정적인 기반 위에서 점진적으로 영향력을 확대하는 것이 유리합니다.\n")
            else:
                lines.append(f"독자적 영역을 구축하되, 네트워크를 활용하여 시너지를 만드세요.\n")

    return "\n".join(lines)


def build_seasonal_fortune(category, saju, profile):
    """계절별 상세 운세 (~600자)"""
    day_elem = saju["day_stem_element"]
    dominant = _get_dominant(saju)

    season_map = {
        "목": {
            "봄(3~5월)": ("🟢 최강 시즌", "목 기운이 왕성해져 모든 일이 순조롭습니다. 새로운 프로젝트, 이직, 사업 시작에 최적입니다. 자신감을 갖고 적극적으로 움직이세요."),
            "여름(6~8월)": ("🟡 발산기", "축적된 에너지를 표현하는 시기입니다. 프레젠테이션, 면접, 계약에 유리합니다. 다만 과열에 주의하고 체력 관리를 병행하세요."),
            "가을(9~11월)": ("🔴 조심기", "금극목(金剋木)으로 도전받는 시기입니다. 무리한 확장보다 기존 사업을 다지세요. 건강검진을 받고 면역력에 신경 쓰세요."),
            "겨울(12~2월)": ("🔵 충전기", "수생목(水生木)으로 에너지가 충전되는 시기입니다. 공부, 자기계발, 내년 계획 수립에 최적입니다. 조용히 실력을 쌓으세요."),
        },
        "화": {
            "봄(3~5월)": ("🟡 준비기", "목생화(木生火)로 점점 에너지가 올라옵니다. 인맥을 넓히고 협업 관계를 구축하세요. 서서히 가속 페달을 밟을 준비를 하세요."),
            "여름(6~8월)": ("🟢 최강 시즌", "화 기운이 극대화되어 빛나는 시기입니다. 리더십을 발휘하고 주도적으로 나서세요. 성과가 가장 크게 나타나는 시기입니다."),
            "가을(9~11월)": ("🟡 수확기", "성과를 정리하고 재물을 관리하는 시기입니다. 과도한 지출을 줄이고 저축을 늘리세요."),
            "겨울(12~2월)": ("🔴 조심기", "수극화(水剋火)로 에너지가 약해집니다. 무리하지 말고 충분히 쉬면서 다가올 봄을 준비하세요. 건강이 최우선입니다."),
        },
        "토": {
            "봄(3~5월)": ("🔴 조심기", "목극토(木剋土)로 변화의 바람이 부는 시기입니다. 기존 기반이 흔들릴 수 있으니 유연하게 대처하고 핵심을 지키세요."),
            "여름(6~8월)": ("🟡 상승기", "화생토(火生土)로 든든한 지원을 받습니다. 인맥의 도움이 크고, 학업이나 자격 취득에 좋습니다. 안정적으로 기반을 확장하세요."),
            "가을(9~11월)": ("🟢 수확기", "토생금(土生金)으로 노력의 결실을 맺는 시기입니다. 재물이 늘어나고 기존에 건 투자의 수익이 나타납니다."),
            "겨울(12~2월)": ("🟡 조정기", "수 기운에 도전받을 수 있으니 건강을 챙기세요. 소화기 관리가 중요하고 과식과 스트레스를 조절하세요."),
        },
        "금": {
            "봄(3~5월)": ("🟡 투자기", "재물 지출이 늘 수 있지만 미래를 위한 투자입니다. 교육, 인맥, 기술에 아끼지 마세요. 장기적 관점에서 접근하세요."),
            "여름(6~8월)": ("🔴 조심기", "화극금(火剋金)으로 도전받는 시기입니다. 업무 스트레스가 높아지니 적절한 휴식을 취하세요. 큰 결정은 이 시기를 피하세요."),
            "가을(9~11월)": ("🟢 최강 시즌", "금 기운이 극대화되어 능력이 빛나는 시기입니다. 승진, 계약, 중요 프로젝트 수주에 최적입니다."),
            "겨울(12~2월)": ("🟡 발산기", "금생수(金生水)로 지혜와 통찰이 깊어집니다. 전략적 사고로 다음 해를 설계하세요."),
        },
        "수": {
            "봄(3~5월)": ("🟡 발산기", "수생목(水生木)으로 에너지를 새 프로젝트에 쏟습니다. 새로운 시도에 유리하지만 에너지 소모에 주의하세요."),
            "여름(6~8월)": ("🟡 재물기", "화 기운에 재물운이 활성화됩니다. 적극적 영업과 거래가 유리합니다. 다만 충동 구매는 자제하세요."),
            "가을(9~11월)": ("🟡 학습기", "금생수(金生水)로 학업운과 자격증운이 좋습니다. 시험, 계약, 문서 관련된 일에 행운이 따릅니다."),
            "겨울(12~2월)": ("🟢 최강 시즌", "수 기운이 극대화되어 지혜와 직감이 최고조입니다. 중요한 결정과 전략 수립에 최적입니다."),
        },
    }

    seasons = season_map.get(day_elem, season_map["목"])

    lines = ["### 🍂 계절별 상세 운세\n"]

    for season, (grade, desc) in seasons.items():
        lines.append(f"**{season}** {grade}\n{desc}\n")

    return "\n".join(lines)


def build_relationship_dynamics(category, saju, profile):
    """대인관계 역학 분석 (~500자)"""
    dominant = _get_dominant(saju)
    god = query_ten_god(dominant)
    day_elem = saju["day_stem_element"]

    lines = ["### 👥 대인관계 역학 분석\n"]

    # 십성별 대인관계 패턴
    rel_map = {
        "비견": ("동료·친구형", "동등한 위치에서 경쟁하며 성장하는 관계를 선호합니다. 수평적 관계에서 시너지가 나지만, 지나친 경쟁심은 관계를 해칠 수 있으니 서로의 영역을 존중하세요.", "동료, 동기, 업계 네트워크"),
        "겁재": ("경쟁·승부형", "강렬한 에너지로 주변을 끌어당기지만 갈등도 잦습니다. 승부욕을 건설적으로 승화시키면 최고의 파트너십을 만들 수 있습니다.", "스포츠 동료, 비즈니스 라이벌"),
        "식신": ("멘토·양육형", "타인을 가르치고 돌보는 것에 보람을 느낍니다. 후배나 제자에게 인기가 많으며, 음식과 문화를 나누는 관계에서 행복을 찾습니다.", "후배, 제자, 맛집 동료"),
        "상관": ("영감·자극형", "독특한 관점으로 주변에 영감을 주지만 권위에 도전하는 성향이 있습니다. 창의적 커뮤니티에서 빛을 발하며, 자유로운 소통이 가능한 관계가 이상적입니다.", "예술가 친구, 창업 동료"),
        "편재": ("사교·네트워크형", "넓은 인맥과 활발한 사교 생활이 특징입니다. 다양한 분야의 사람들과 교류하며 기회를 만들어냅니다. 인맥이 곧 자산입니다.", "비즈니스 파트너, 사교 모임"),
        "정재": ("헌신·의리형", "한번 맺은 관계를 오래 유지하며, 신뢰를 가장 중요하게 여깁니다. 소수의 깊은 관계를 선호하고 약속을 철저히 지킵니다.", "오랜 친구, 가족, 직장 동료"),
        "편관": ("카리스마·리더형", "강한 존재감으로 자연스럽게 리더 역할을 맡습니다. 존경과 두려움을 동시에 받으며, 결정적 순간에 의지가 되는 사람입니다.", "조직 리더, 선배, 멘토"),
        "정관": ("신뢰·모범형", "사회적 규범과 예의를 중시하며 주변의 귀감이 됩니다. 공식적 관계에서 빛을 발하고 신뢰를 기반으로 영향력을 확대합니다.", "직장 상사, 공식 네트워크"),
        "편인": ("독립·영감형", "혼자만의 시간을 중요하게 여기며 독특한 매력으로 소수의 사람을 끌어당깁니다. 깊은 정신적 교감을 나눌 수 있는 관계를 원합니다.", "지적 친구, 영적 동반자"),
        "정인": ("보호·교육형", "주변 사람들에게 따뜻한 울타리가 됩니다. 가르치고 보살피는 관계에서 보람을 느끼며, 어머니와 같은 포용력을 가지고 있습니다.", "스승, 어머니, 제자"),
    }

    rtype, desc, best = rel_map.get(dominant, rel_map["비견"])
    lines.extend([
        f"**대인관계 유형**: {rtype}\n",
        f"{desc}\n",
        f"**최적의 인연**: {best}\n",
    ])

    # 직장과 가정에서의 관계
    job = profile.get("job", "")
    marital = profile.get("marital_status", "")
    if job:
        lines.append(f"**직장에서**: {job} 종사자로서 {dominant}의 기운은 ")
        if dominant in ["정관","정재","정인"]:
            lines.append(f"조직 내 신뢰와 안정감을 제공합니다. 상사와 동료에게 믿음직한 존재로 인정받습니다.\n")
        elif dominant in ["상관","편재","겁재"]:
            lines.append(f"혁신과 변화를 이끄는 역할을 합니다. 새로운 아이디어로 조직에 활력을 불어넣습니다.\n")
        else:
            lines.append(f"독자적 영역에서 전문성을 발휘합니다. 자율성이 보장될수록 더 큰 성과를 냅니다.\n")

    if marital == "기혼":
        children = profile.get("children_count", 0)
        lines.append(f"**가정에서**: {dominant}의 기운은 가정에서 ")
        if dominant in ["식신","정인","정재"]:
            lines.append(f"따뜻하고 헌신적인 가장/어머니의 모습으로 나타납니다. ")
        else:
            lines.append(f"독립적이면서도 책임감 있는 파트너로서의 모습을 보입니다. ")
        if children and int(children) > 0:
            lines.append(f"자녀 {children}명과의 관계에서 {dominant}의 교육관이 뚜렷히 드러나며, "
                        f"적절한 자율성과 규율의 균형이 중요합니다.\n")
        else:
            lines.append(f"배우자와의 관계에서 상호 존중과 소통이 행복의 핵심입니다.\n")

    return "\n".join(lines)



# ────────────────────────────────
# 심층 경쟁 우위 블록 (New)
# ────────────────────────────────

def build_wealth_strategy(saju, profile):
    """심층 재물운 및 자산 관리 전략 (~800자)"""
    dominant = _get_dominant(saju)
    god = query_ten_god(dominant)
    # 용신 대용으로 '가장 부족한 오행(weakest)'을 보완하는 것을 전략으로 삼음 (안정성 추구)
    # 또는 '가장 강한 오행(strongest)'을 활용하는 공격적 투자 (수익성 추구)
    weakest = saju["elements"]["weakest"]
    strongest = saju["elements"]["strongest"]
    
    lines = ["### 💰 심층 재물운 & 자산 포트폴리오 전략\n"]
    
    # 1. 재물 그릇의 크기와 성향
    lines.append("#### 1. 타고난 '부(富)의 그릇' 진단\n")
    if dominant in ["편재", "정재"]:
        lines.append(f"당신은 사주 자체가 '재물 창고'로 설계된 **재성(財星) 주도형**입니다. 돈의 흐름을 읽는 감각이 타고났으며, 자산을 불리는 데 천부적인 재능이 있습니다. 다만 '재다신약(財多身弱)'의 가능성이 있으니 체력 관리가 곧 재물 관리입니다.\n")
    elif dominant in ["식신", "상관"]:
        lines.append(f"당신은 재물을 만들어내는 '수단'이 발달한 **식상생재(食傷生財)형**입니다. 아이디어와 기술 자체가 자산이 되며, 남들이 못 보는 틈새 시장을 공략하여 부를 창출합니다. 무형 자산(지적재산권, 브랜드) 확보에 주력하세요.\n")
    elif dominant in ["비견", "겁재"]:
        lines.append(f"당신은 사람과 경쟁을 통해 파이를 키우는 **자수성가형**입니다. 초기 자본금 확보에는 시간이 걸리지만, 한번 탄력을 받으면 폭발적으로 성장합니다. 동업보다는 본인의 이름으로 승부하는 것이 유리합니다.\n")
    elif dominant in ["정관", "편관"]:
        lines.append(f"당신은 명예와 시스템을 통해 부를 얻는 **관인상생(官印相生)형**입니다. 고위험 투자보다는 브랜드 가치가 높은 부동산이나 안정적인 대기업 주식, 연금형 자산이 맞습니다. 사회적 지위가 곧 재력으로 연결됩니다.\n")
    else: # 인성
        lines.append(f"당신은 문서와 지혜로 부를 축적하는 **문서 부자형**입니다. 현금 흐름보다는 부동산 등기 권리증, 자격증, 저작권 등 '서류상 자산'이 가장 안전하고 큰 수익을 줍니다.\n")

    # 2. 맞춤형 투자 포트폴리오 (구체적 자산 추천)
    lines.append(f"\n#### 2. 오행 기반 맞춤 투자 포트폴리오\n")
    lines.append("당신의 사주 에너지 균형을 맞추는 최적의 투자처입니다.\n")
    
    asset_map = {
        "목": "**성장주 & 교육**: 바이오, 헬스케어, 교육 관련 주식이나 신도시 부동산 개발 투자가 유리합니다.",
        "화": "**미디어 & 기술**: IT, 콘텐츠, 엔터테인먼트, 전기차 배터리 등 화려하고 변동성 큰 시장에서 수익을 냅니다.",
        "토": "**부동산 & 원자재**: 아파트, 토지, 리츠(REITs) 등 땅과 관련된 전통적 자산이나 건자재 관련주가 안정적입니다.",
        "금": "**채권 & 귀금속**: 금/은 현물, 국채, 금융주, 반도체 등 단단하고 가치가 보존되는 자산이 맞습니다.",
        "수": "**유통 & 해외**: 해운, 물류, 식음료, 해외 주식(미국장) 등 유동성이 크고 순환이 빠른 시장을 공략하세요."
    }
    
    # 전략: 강한 기운으로 밀고 나갈 것인가(공격), 부족한 기운을 채울 것인가(방어)
    lines.append(f"- **공격적 투자(High Risk)**: 당당한 기세({strongest})를 활용한다면 -> {asset_map.get(strongest)}\n")
    lines.append(f"- **안정적 투자(Low Risk)**: 부족한 기운({weakest})을 보완한다면 -> {asset_map.get(weakest)}\n")
    
    # 3. 금융 행동 심리학 코칭
    lines.append(f"\n#### 3. '돈이 새는 구멍' 막는 솔루션\n")
    if dominant in ["겁재", "상관", "편재"]:
        lines.append(f"**⚠️ 위함 신호**: '일확천금'의 유혹. 기분파적인 지출.\n")
        lines.append(f"**✅ 처방**: 수입의 50%는 들어오자마자 묶이는 '강제 저축 시스템'을 만드세요. 신용카드보다는 체크카드를 사용하여 현금 흐름을 눈으로 확인해야 합니다.\n")
    elif dominant in ["정재", "정인", "정관"]:
        lines.append(f"**⚠️ 위험 신호**: 지나친 신중함으로 인한 '기회 비용' 상실.\n")
        lines.append(f"**✅ 처방**: 자산의 10~20%는 과감하게 트렌디한 ETF나 성장주에 '없어도 되는 돈'이라 생각하고 투자해보세요. 작은 성공 경험이 부의 감각을 깨워줍니다.\n")
    else:
        lines.append(f"**⚠️ 위험 신호**: 귀가 얇아 생기는 '지인 투자 사기'.\n")
        lines.append(f"**✅ 처방**: 지인과의 돈 거래는 절대 금물입니다. 투자는 오직 본인이 공부하고 확신이 든 곳에만 하세요. 전문가 상담을 정기적으로 받는 것이 좋습니다.\n")

    return "\n".join(lines)


def build_career_pathmap(saju):
    """커리어 로드맵 및 조직 적합도 분석 (~800자)"""
    dominant = _get_dominant(saju)
    god = query_ten_god(dominant)
    day_elem = saju["day_stem_element"]

    lines = ["### 🚀 커리어 로드맵 & 조직 적합도 분석\n"]
    
    # 1. 조직 적합도 (Company Fit)
    lines.append("#### 1. 나에게 맞는 '조직의 형태'\n")
    
    org_type = ""
    if dominant in ["정관", "정인"]:
        org_type = "🏛️ **대기업/공공기관형 (Stable & System)**\n체계적인 시스템과 명확한 위계질서가 있는 곳에서 안정감을 느낍니다. 복지가 좋고 네임밸류가 있는 간판이 본인의 자존감을 높여줍니다."
    elif dominant in ["편관", "비견"]:
        org_type = "⚔️ **군/경/특수조직/외국계형 (Challenge & Power)**\n강력한 권한이 주어지거나, 실력으로 승부하는 치열한 환경에서 두각을 나타냅니다. 연공서열보다는 성과 중심의 조직이 맞습니다."
    elif dominant in ["식신", "상관"]:
        org_type = "🦄 **스타트업/R&D/크리에이티브형 (Innovation & Autonomy)**\n자율성이 보장되지 않으면 숨이 막힙니다. 복장과 출퇴근이 자유롭고, 본인의 아이디어를 즉각 실행할 수 있는 수평적 조직이 최적입니다."
    elif dominant in ["편재", "정재", "겁재"]:
        org_type = "💼 **사업/영업/프리랜서형 (Result & Profit)**\n월급보다는 인센티브, 혹은 내 사업을 통해 '일한 만큼 가져가는' 구조가 동기부여가 됩니다. 억압된 조직 생활보다는 야생의 시장이 더 편할 수 있습니다."
    elif dominant in ["편인"]:
        org_type = "🎓 **전문직/연구소/특수기술형 (Expertise & Niche)**\n남들이 쉽게 접근하지 못하는 특수 분야나 고도의 전문 지식이 필요한 영역에서 '대체 불가능한 존재'가 되어야 합니다."
        
    lines.append(f"{org_type}\n")
    
    # 2. 직무 적성 매핑 (Job Mapping)
    lines.append(f"\n#### 2. 사주로 본 '천직(天職)' 키워드\n")
    lines.append(f"당신의 주무기인 **{dominant}({god['keyword']})**을(를) 현대 직업으로 치환하면 다음과 같습니다.\n")
    
    job_keywords = {
        "비견": "프리랜서, 전문직, 예체능, 대리점주",
        "겁재": "에이전트, 로비스트, 투자 전문가, 엔터테인먼트",
        "식신": "요식업, 교육, R&D 연구원, 제조/생산 전문가",
        "상관": "마케터, 기획자, 유튜버, 강사, 디자이너",
        "편재": "무역, 유통, 금융 트레이더, 벤처 사업가",
        "정재": "회계사, 은행원, 세무사, 공무원(재경직)",
        "편관": "경찰, 군인, 법조인, 엔지니어, 외과의사",
        "정관": "행정 공무원, 인사(HR), 경영지원, 대기업 사무직",
        "편인": "의사, 약사, 작가, IT 개발자, 데이터 분석가",
        "정인": "교수, 교사, 출판/번역, 부동산 전문가"
    }
    lines.append(f"- **추천 직군**: {job_keywords.get(dominant)}\n")
    lines.append(f"- **업무 강점**: {god['career'][:100]}...\n")
    
    # 3. 커리어 위기 관리 (Slump Management)
    lines.append(f"\n#### 3. 슬럼프 극복 & 번아웃 예방\n")
    if dominant in ["식신", "상관"]:
        lines.append("창작의 고통과 '인정 욕구' 결핍이 번아웃의 주원인입니다. 결과물이 바로 안 나와도 과정 자체를 즐기는 마인드셋 훈련이 필요합니다. 주기적인 '멍 때리기' 여행을 추천합니다.\n")
    elif dominant in ["관성", "인성"]:
        lines.append("과도한 책임감과 '완벽주의'가 발목을 잡습니다. 업무를 타인에게 위임하는 법을 배우고, 퇴근 후에는 업무 알림을 완전히 끄는 '디지털 디톡스'가 생존 필수 조건입니다.\n")
    else:
        lines.append("인간관계 스트레스와 경쟁 과열이 원인입니다. 회사 내의 정치 싸움에서 한 발짝 물러나, '나만의 전문성' 강화에 집중하면 자연스럽게 문제는 해결됩니다.\n")
        
    return "\n".join(lines)


def build_love_dynamics(saju, profile):
    """관계 역동성 분석 및 싸움/화해 솔루션 (~800자)"""
    dominant = _get_dominant(saju)
    day_elem = saju["day_stem_element"]
    day_branch = saju["pillars"]["day"]["branch"]
    weakest = saju["elements"]["weakest"]
    
    lines = ["### 💘 관계 역동성(Dynamics) & 솔루션\n"]
    
    # 1. 나의 연애 스타일 진단
    lines.append(f"#### 1. 나의 관계 맺기 스타일: '일지 {day_branch}'\n")
    
    style_desc = ""
    # 간단한 일지 해석 (자오묘유, 인신사해, 진술축미)
    if day_branch in ["자", "오", "묘", "유"]:
        style_desc = "**도화(Peach Blossom) 스타일**: 본능적으로 이성을 끄는 매력이 있습니다. 사랑에 빠지면 열정적이지만, 싫증도 잘 느끼는 편입니다. 상대방에게 끊임없이 새로운 모습을 보여주는 '밀당의 고수'입니다."
    elif day_branch in ["인", "신", "사", "해"]:
        style_desc = "**역마(Movement) 스타일**: 활동적이고 변화무쌍한 연애를 선호합니다. 정적인 데이트보다는 함께 여행을 가거나 새로운 취미를 배우는 '동지적 관계'에서 깊은 사랑을 느낍니다."
    else: # 진술축미
        style_desc = "**화개(Arts/Religion) 스타일**: 겉으로는 무뚝뚝해 보이지만 속은 깊은 정이 있습니다. 화려한 이벤트보다는 진심 어린 편지 한 통에 감동하며, 한 번 마음을 주면 끝까지 지키는 '의리파'입니다."
        
    lines.append(f"{style_desc}\n")
    
    # 2. 갈등 패턴 시뮬레이션
    lines.append(f"\n#### 2. 갈등 패턴 시뮬레이션: '이럴 때 싸운다'\n")
    if dominant in ["비견", "겁재"]:
        lines.append(f"**💣 폭탄 지점**: '자존심 대결'.\n당신은 연인이라도 간섭이나 지적을 받으면 참지 못합니다. 상대방의 사소한 조언을 '공격'으로 받아들이는 순간 싸움이 시작됩니다. '너가 뭘 알아?'라는 말이 나오는 순간 관계는 끝납니다.\n")
        lines.append(f"**💊 화해 처방**: 논리적 반박보다는, 일단 자리를 피해서 감정을 식히세요. 그리고 먼저 '미안하지만 내 자존심이 좀 다쳤어'라고 솔직하게 약점을 인정하면 상대는 오히려 당신을 안아줄 것입니다.\n")
    elif dominant in ["식신", "상관"]:
        lines.append(f"**💣 폭탄 지점**: '말로 주는 상처'.\n화가 나면 필터 없이 내뱉는 독설이 문제입니다. 당신은 뒤끝이 없어서 금방 잊지만, 상대방 가슴에는 평생 지워지지 않는 멍이 듭니다.\n")
        lines.append(f"**💊 화해 처방**: 말로 해결하려 하지 말고, 맛있는 음식이나 작은 선물로 분위기를 푸세요. 당신의 애교와 재치는 최고의 무기입니다. 백 마디 변명보다 한 번의 따뜻한 스킨십이 낫습니다.\n")
    elif dominant in ["편관", "정관"]:
        lines.append(f"**💣 폭탄 지점**: '통제와 강요'.\n상대방을 내 기준에 맞추려 하고, '이건 상식적으로 아니지 않아?'라며 가르치려 듭니다. 연인은 당신의 부하직원이 아닙니다.\n")
        lines.append(f"**💊 화해 처방**: '그럴 수도 있겠다'라는 말을 하루에 10번씩 연습하세요. 맞고 틀리고를 따지지 말고, 그냥 상대방의 감정에 공감해주는 리액션만으로도 기적 같은 평화가 찾아옵니다.\n")
    elif dominant in ["편인", "정인"]:
        lines.append(f"**💣 폭탄 지점**: '회피와 징징댐'.\n갈등이 생기면 입을 닫고 동굴로 들어가거나, '나만 억울해'라며 피해자 코스프레를 할 수 있습니다. 침묵 시위는 상대를 미치게 만듭니다.\n")
        lines.append(f"**💊 화해 처방**: 글로 쓰세요. 말로 하기 힘들면 편지나 톡으로라도 당신의 생각을 정리해서 전해야 합니다. 상대방은 독심술사가 아닙니다.\n")
    else: # 재성
        lines.append(f"**💣 폭탄 지점**: '계산적인 태도'.\n무의식중에 '내가 이만큼 해줬는데 너는?'이라며 거래하듯 사랑을 따질 수 있습니다. 현실적인 문제(돈, 시간)로 쪼는 순간 로맨스는 사망입니다.\n")
        lines.append(f"**💊 화해 처방**: 가성비를 따지지 않는 '낭비'를 해보세요. 비효율적인 데이트가 때로는 사랑을 증명합니다. 계산 없이 퍼주는 경험이 당신의 연애 등급을 높여줍니다.\n")

    # 3. 이상형 구체화
    lines.append(f"\n#### 3. 운명의 짝(Ideal Match)\n")
    lines.append(f"단순히 예쁘고 멋진 사람이 아닙니다. 당신의 **{weakest}(약한 기운)**을 채워주고, **{dominant}(강한 기운)**를 감당할 수 있는 사람은 다음과 같습니다.\n")
    
    tokens = {
        "목": "순수하고 어린아이 같은 천진난만함을 가진 사람",
        "화": "밝고 명랑하며 감정 표현이 솔직한 에너자이저",
        "토": "믿음직스럽고 묵묵히 내 말을 들어주는 든든한 나무 같은 사람",
        "금": "세련되고 맺고 끊음이 확실하며 자기 관리가 철저한 사람",
        "수": "지적이고 차분하며 내면의 깊이가 있는 신비로운 사람"
    }
    
    lines.append(f"👉 **Key Person**: {tokens.get(saju['elements']['weakest'], '마음이 따뜻한 사람')}\n")

    return "\n".join(lines)


def _get_dominant(saju):
    """가장 강한 십성"""
    gc = saju.get("god_count", {})
    if not gc:
        return "비견"
    return max(gc, key=gc.get)
# ────────────────────────────────
# 성명학 (이름 오행 분석)
# ────────────────────────────────

def build_name_analysis_block(saju, profile):
    """이름의 한자 오행과 사주의 조화를 분석하는 블록 (~600자)"""
    from seongmyeonghak import analyze_name_balance
    
    hanja_name = profile.get("name_hanja", "")
    if not hanja_name:
        # 프로필에 한자 이름이 없으면 일반 이름 필드에서 한자만 추출 시도
        full_name = profile.get("name", "")
        import re
        hanja_name = "".join(re.findall(r'[一-龥]', full_name))
        
    if not hanja_name:
        return ""
        
    saju_elements = saju["elements"]
    res = analyze_name_balance(hanja_name, saju_elements)
    
    if res["status"] == "skip":
        return ""
        
    lines = [
        "### 📛 성명학(姓名學): 이름과 사주의 조화\n",
        f"분석된 한자 이름: **{hanja_name}**\n",
        res["analysis_text"],
        "\n",
        f"#### 성명학 조화 지수: **{res['score']}점**\n",
        "> 💡 **성명학 팁**: 좋은 이름은 사주에서 부족한 기운(용신/희신)을 보완하여 삶의 흐름을 원활하게 돕는 역할을 합니다. "
        "만약 실명에서 기운이 보충되지 않는다면, 호(號)나 예명을 통해 부족한 기운을 채우는 것도 좋은 방법입니다.\n"
    ]
    
    return "\n".join(lines)
