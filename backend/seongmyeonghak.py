from saju_db import query_hanja_element

def analyze_name_balance(hanja_name, saju_elements):
    """
    한자 이름의 원획(Traditional Strokes)과 오행을 사주와 결합하여 분석합니다.
    - Won-hoik 기반 획수 조화 (수리길흉)
    - 오행 보완 (DNA Blueprint)
    """
    name_elements = []
    found_chars = []
    total_strokes = 0
    char_details = []
    
    for char in hanja_name:
        res = query_hanja_element(char)
        if res:
            elem = res['element'] or "알수없음"
            strokes = res['won_strokes'] or 0 # 필획 대신 원획 사용
            name_elements.append(elem)
            total_strokes += strokes
            found_chars.append(f"{char}({elem}, {strokes}획)")
            char_details.append({"char": char, "element": elem, "strokes": strokes})
    
    if not name_elements:
        return {
            "status": "skip",
            "message": "분석 가능한 인명용 한자가 이름에 포함되어 있지 않습니다."
        }
    
    # 2. 오행 보완도 분석 (DNA Blueprint)
    weakest = saju_elements.get("weakest")
    strongest = saju_elements.get("strongest")
    
    name_counts = {}
    for elem in name_elements:
        name_counts[elem] = name_counts.get(elem, 0) + 1
    
    is_complementary = weakest in name_counts
    
    # 3. 수리(Strokes) 분석 (단순 예시 로직)
    # 성명학에서 획수의 합에 따른 길흉 판단 (81수리 등)
    # 여기서는 간단히 짝수/홀수 조화나 특정 합계의 길흉 리포트 생성
    stroke_msg = f"이름의 원획 총합은 **{total_strokes}획**입니다. "
    if total_strokes % 2 == 0:
        stroke_msg += "안정적이고 조화로운 수리 기운을 담고 있습니다."
    else:
        stroke_msg += "활동적이고 진취적인 에너지가 강한 수리 구성입니다."

    analysis_lines = []
    analysis_lines.append(f"🧬 **Name DNA Blueprint**: {' '.join(found_chars)}")
    analysis_lines.append(f"⚖️ **수리 분석**: {stroke_msg}")
    
    if is_complementary:
        analysis_lines.append(f"✅ **오행 보완**: 사주의 부족한 **{weakest}** 기운을 이름에서 잘 채워주고 있습니다.")
    else:
        analysis_lines.append(f"⚠️ **오행 보완**: 사주의 **{weakest}** 기운이 이름에 부족합니다. 보완이 권장됩니다.")
        
    # 종합 평점
    score = 75
    if is_complementary: score += 15
    if total_strokes > 0: score += 5
    
    return {
        "status": "success",
        "char_details": char_details,
        "total_strokes": total_strokes,
        "is_complementary": is_complementary,
        "analysis_text": "\n".join(analysis_lines),
        "score": min(score, 100)
    }
