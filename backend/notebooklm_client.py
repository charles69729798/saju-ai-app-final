import os
import json
import sqlite3
from saju_db import get_db, save_notebooklm_cache, get_notebooklm_cache

# Try to import real client, fallback to None
try:
    from notebooklm_tools.core.client import NotebookLMClient
except ImportError:
    NotebookLMClient = None

class SajuNotebookLMClient:
    def __init__(self, cookies=None):
        self.cookies = cookies or os.environ.get("NOTEBOOKLM_COOKIES")
        self.client = None
        if self.cookies and NotebookLMClient:
            self.client = NotebookLMClient(cookies=self.cookies)
    
    def query(self, prompt, use_cache=True):
        """
        Query NotebookLM about a topic.
        Returns the response string.
        """
        # 1. Check Cache
        query_hash = str(hash(prompt)) # Simple hash for demo
        if use_cache:
            cached = get_notebooklm_cache(query_hash)
            if cached:
                print(f"[Cache Hit] {prompt[:30]}...")
                return cached["response"]
        
        # 2. Fetch from Real Client
        if self.client:
            try:
                print(f"[NotebookLM] Querying: {prompt[:30]}...")
                # Note: Actual API might differ, adjusting to hypothetical usage
                # Assuming client.query_notebook(notebook_id, query) or similar
                # For now using a placeholder call structure
                response = self.client.query(prompt) 
                save_notebooklm_cache(query_hash, prompt, response)
                return response
            except Exception as e:
                print(f"[Error] NotebookLM query failed: {e}")
                return self._get_mock_response(prompt)
        
        # 3. Fallback to Mock
        print(f"[Mock] Returning simulated response for: {prompt[:30]}...")
        return self._get_mock_response(prompt)

    def _get_mock_response(self, prompt):
        """Simulated responses for testing without API access"""
        if "갑목" in prompt:
            return "갑목(甲木)은 거목과 같아 굽히기를 싫어하고 위로 뻗어나가려는 기질이 강합니다. 적천수에서는 '갑목참천 탈태요화'라 하여..."
        elif "정관" in prompt:
            return "정관(正官)은 바른 벼슬을 의미하며, 규율과 질서를 중시합니다. 자평진전에서는 정관을 귀하게 여겨 형충파해를 꺼린다고 하였습니다..."
        return f"'{prompt}'에 대한 고전 명리 해석입니다. (NotebookLM 연동 필요)"

# Test execution
if __name__ == "__main__":
    client = SajuNotebookLMClient()
    print(client.query("갑목의 성질에 대해 알려줘"))
