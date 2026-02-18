"""
Flask 기반 사주 AI 상담 API 서버 (DB 전용 버전)
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

from saju_db import (
    init_db, update_schema, query_element, query_stem, 
    query_branch, query_ten_god, query_celebs, query_celeb_by_id
)
from saju_calculator import calculate_full_saju
from fortune_generator import generate_fortune
from hanja_service import get_hanja_candidates

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# DB 초기화 및 스키마 업데이트
init_db()
update_schema()

# 카테고리 목록 (Phase 8b Refined)
CATEGORIES = [
    {"id": "평생사주", "name": "🧬 본캐 분석 (DNA Blueprint)", "priority": "필수"},
    {"id": "오늘의운세", "name": "⚡ 오늘의 바이브 (Today's Vibe)", "priority": "필수"},
    {"id": "이번달운세", "name": "📆 먼슬리 체크 (Monthly Check)", "priority": "중요"},
    {"id": "신년운세", "name": "🔮 2026년 스포일러 (Yearly Spoiler)", "priority": "필수"},
    {"id": "재물운", "name": "💰 머니 플렉스 (Wealth Flex)", "priority": "필수"},
    {"id": "애정운", "name": "💞 러브 시그널 (Love Chemistry)", "priority": "필수"},
    {"id": "직업운", "name": "🚀 커리어 치트키 (Career Path)", "priority": "필수"},
    {"id": "건강운", "name": "💪 HP 관리 (Health Status)", "priority": "중요"},
    {"id": "개운법", "name": "🍀 행운 부스터 (Luck Booster)", "priority": "중요"},
    {"id": "MBTI분석", "name": "🧠 뇌 구조 (MBTI Sync)", "priority": "중요"},
]


@app.route('/')
def root():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api')
def api_info():
    return jsonify({
        "message": "사주 AI 상담 API 서버 (DB 전용 오프라인 버전)",
        "version": "2.0.0",
        "mode": "offline_db",
        "endpoints": ["/api/categories", "/api/saju/calculate", "/api/saju/analyze"]
    })


@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify({"categories": CATEGORIES})


@app.route('/api/hanja', methods=['GET'])
def get_hanja():
    char = request.args.get('char', '')
    if not char:
        return jsonify({"candidates": []})
    
    candidates = get_hanja_candidates(char)
    return jsonify({"candidates": candidates})


@app.route('/api/celebs', methods=['GET'])
def get_celebs():
    category = request.args.get('category')
    search = request.args.get('search')
    celebs = query_celebs(category, search)
    return jsonify({"celebs": celebs})


@app.route('/api/celebs/<int:celeb_id>', methods=['GET'])
def get_celeb_detail(celeb_id):
    celeb = query_celeb_by_id(celeb_id)
    if not celeb:
        return jsonify({"status": "error", "message": "스타를 찾을 수 없습니다."}), 404
        
    # 스타 사주 계산 결과 포함
    saju = calculate_full_saju(celeb['birth_date'], celeb['birth_time'])
    return jsonify({
        "status": "success",
        "celeb": celeb,
        "saju_detail": saju
    })


@app.route('/api/saju/calculate', methods=['POST'])
def calculate_saju():
    data = request.json
    saju = calculate_full_saju(data['birth_date'], data['birth_time'])
    return jsonify({
        "status": "success",
        "saju": saju["saju_text"],
        "detail": saju,
    })


@app.route('/api/saju/analyze', methods=['POST'])
def analyze_saju():
    data = request.json
    print(f"DEBUG: analyze_saju data structure: {type(data.get('birth_date'))} - {data.get('birth_date')}") # Debug Log
    
    # [Compatibility] Support both nested 'user_profile' (Frontend v2) and flat structure (Legacy)
    profile_source = data.get('user_profile', data)

    # [Hardening] birth_date extraction & validation
    birth_date = profile_source.get('birth_date', '')
    if isinstance(birth_date, dict):
         # 만약 딕셔너리로 들어왔다면 포맷 변환
         birth_date = f"{birth_date.get('year', '1990')}-{str(birth_date.get('month', '01')).zfill(2)}-{str(birth_date.get('day', '01')).zfill(2)}"

    # 이름 포맷팅
    name_parts = []
    # name_hanja extracted from profile_source
    if profile_source.get('name_hanja'):
        name_parts.append(f"({profile_source['name_hanja']})")

    # 카테고리별 필수 데이터 검증 (Root data used for category)
    category = data.get('category', '')
    if category == "혈액형분석" and not profile_source.get("blood_type"):
        return jsonify({"status": "error", "message": "혈액형 정보를 입력해야 분석이 가능합니다."}), 400
    if category == "MBTI분석" and not profile_source.get("mbti"):
        return jsonify({"status": "error", "message": "MBTI 정보를 입력해야 분석이 가능합니다."}), 400
    
    # name_korean might be in profile_source under 'name_korean' or just 'name' in some contexts, 
    # but index.html sends name_korean.
    korean_name = profile_source.get('name_korean', profile_source.get('name', '고객'))
    
    user_profile = {
        "name": f"{korean_name} {' '.join(name_parts)}".strip(),
        "gender": profile_source.get('gender', 'U'),
        "job": profile_source.get('job', ''),
        "education": profile_source.get('education', ''),
        "mbti": profile_source.get('mbti', ''),
        "blood_type": profile_source.get('blood_type', ''),
        "marital_status": profile_source.get('marital_status', ''),
        "children_count": profile_source.get('children_count', 0),
        "relation_type": profile_source.get('relation_type', 'lover'), # This might be unused if covered by relation_data
        "relation_data": data.get('relation_data', None) # relation_data is at ROOT in index.html call
    }
    
    # birth_time also from profile_source
    birth_time = profile_source.get('birth_time', '12:00')
    
    result = generate_fortune(
        birth_date,
        birth_time,
        data['category'],
        user_profile
    )
    
    if result["status"] == "success":
        return jsonify({
            "status": "success",
            "category": data['category'],
            "result": result["fortune"],
            "char_count": result["char_count"],
            "saju": result["saju"]["saju_text"],
        })
    else:
        return jsonify(result), 500


if __name__ == '__main__':
    print("🚀 사주 AI 상담 서버 시작 (DB 전용 오프라인 버전)")
    print("📍 http://localhost:8080")
    print("📊 모드: 로컬 SQLite DB 기반 (인터넷 불필요)")
    app.run(host='0.0.0.0', port=8080, debug=True)
