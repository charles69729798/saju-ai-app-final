import sqlite3
from saju_db import get_db, init_db
from notebooklm_client import SajuNotebookLMClient

def populate_wisdom():
    """
    NotebookLM을 통해 고전 명리 데이터를 확장/보강합니다.
    (실제 연동이 안 될 경우, notebooklm_client의 Mock 데이터가 사용됩니다)
    """
    client = SajuNotebookLMClient()
    conn = get_db()
    cursor = conn.cursor()

    # 1. 대상 목록 정의
    targets = [
        ("ten_gods", "비견", "적천수", "비견에 대한 심층적 해석과 적천수 원문 인용"),
        ("ten_gods", "겁재", "궁통보감", "겁재의 양면성과 궁통보감의 시각"),
        ("elements", "목", "자평진전", "목(木) 오행의 성질과 자평진전의 논리"),
        ("elements", "금", "적천수", "금(金) 오행의 숙살지기와 적천수 해석"),
    ]

    print("📜 NotebookLM을 통한 고전 지식 수집 시작...")

    for category, name, source, query in targets:
        print(f"   Querying: {name} ({source})...")
        
        # NotebookLM(또는 Mock)에 질의
        prompt = f"{source}에서 말하는 {name}의 핵심 내용을 원문과 함께 설명해줘."
        response = client.query(prompt)
        
        # 간단한 파싱 (Mock 데이터는 형식이 일정하지 않을 수 있으므로 통째로 저장)
        # 실제 구현 시에는 정규식 등으로 원문/해석 분리 필요
        original_text = f"[{source} 원문 발췌]"
        modern_interp = response

        # DB 업데이트 (중복 시 덮어쓰기)
        # target_name과 source가 일치하는 항목이 있으면 현대적 해석 업데이트
        # 없으면 새로 추가
        
        # Check existing
        cursor.execute("SELECT id FROM classical_wisdom WHERE category=? AND target_name=? AND source=?", 
                       (category, name, source))
        row = cursor.fetchone()
        
        if row:
            print(f"      -> Updating existing entry ID {row[0]}")
            cursor.execute("""
                UPDATE classical_wisdom 
                SET modern_interpretation = ? 
                WHERE id = ?
            """, (modern_interp, row[0]))
        else:
            print(f"      -> Inserting new entry")
            cursor.execute("""
                INSERT INTO classical_wisdom (category, target_name, source, original_text, modern_interpretation)
                VALUES (?, ?, ?, ?, ?)
            """, (category, name, source, original_text, modern_interp))
            
    conn.commit()
    conn.close()
    print("✅ 고전 지식 데이터베이스 업데이트 완료.")

if __name__ == "__main__":
    populate_wisdom()
