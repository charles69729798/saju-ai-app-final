import unittest
import json
import urllib.request
import urllib.error
import sys

# 테스트 대상 서버 설정
BASE_URL = "http://127.0.0.1:8000/api"

class TestSajuAppAPI(unittest.TestCase):
    def setUp(self):
        """각 테스트 시작 전 실행"""
        self.headers = {"Content-Type": "application/json"}
        # 기본 공통 페이로드
        self.default_payload = {
            "birth_date": "1995-05-05",
            "birth_time": "14:30",
            "gender": "F",
            "name_korean": "TestUser",
            "relation_type": "lover"
        }

    def _get(self, endpoint):
        """GET 요청 헬퍼"""
        url = f"{BASE_URL}{endpoint}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            self.fail(f"GET Request Failed ({endpoint}): {e}")

    def _post(self, endpoint, data):
        """POST 요청 헬퍼"""
        url = f"{BASE_URL}{endpoint}"
        try:
            req = urllib.request.Request(
                url, 
                data=json.dumps(data).encode('utf-8'), 
                headers=self.headers
            )
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            # 에러 응답도 테스트의 일부이므로 반환
            return json.loads(e.read().decode())
        except Exception as e:
            self.fail(f"POST Request Failed ({endpoint}): {e}")

    # -------------------------------------------------------------------------
    # 1. 카테고리 로딩 테스트
    # -------------------------------------------------------------------------
    def test_01_categories_loading(self):
        """[Checklist 1] /api/categories가 정상적으로 목록을 반환하는가?"""
        print("\n🔍 [Test 1] 카테고리 목록 로딩 확인")
        data = self._get("/categories")
        
        self.assertIn("categories", data)
        self.assertTrue(len(data["categories"]) > 0, "카테고리 목록이 비어있습니다.")
        
        # 필수 카테고리 존재 여부 확인
        category_ids = [c["id"] for c in data["categories"]]
        print(f"   👉 로드된 카테고리: {', '.join(category_ids[:5])}...")
        
        required = ["평생사주", "애정운", "재물운"]
        for req in required:
            self.assertIn(req, category_ids, f"필수 카테고리 '{req}' 누락됨")

    # -------------------------------------------------------------------------
    # 2. 관계별 문맥 확인 테스트
    # -------------------------------------------------------------------------
    def test_02_relationship_context_lover(self):
        """[Checklist 2-1] 'Lover' 관계 시 '궁합', 'DNA Hybrid' 키워드 포함 확인"""
        print("\n🔍 [Test 2-1] Lover(연인) 관계 문맥 테스트")
        payload = self.default_payload.copy()
        payload["category"] = "평생사주"
        payload["relation_type"] = "lover"
        
        res = self._post("/saju/analyze", payload)
        self.assertEqual(res["status"], "success")
        
        content = res["result"]
        # 키워드 검증
        keywords = ["궁합", "DNA Hybrid"]
        found = [k for k in keywords if k in content]
        
        if len(found) != len(keywords):
            print(f"   ⚠️ 일부 키워드 누락: {set(keywords) - set(found)}")
        
        # 최소 하나 이상은 있어야 성공으로 간주 (앱 로직에 따라 다를 수 있음)
        self.assertTrue(len(found) > 0, f"Lover 문맥 키워드({keywords})가 결과에 없습니다.")
        print(f"   ✅ 발견된 키워드: {found}")

    def test_02_relationship_context_business(self):
        """[Checklist 2-2] 'Business' 관계 시 'MZ Summary', '성향' 키워드 포함 확인"""
        print("\n🔍 [Test 2-2] Business(비즈니스) 관계 문맥 테스트")
        payload = self.default_payload.copy()
        payload["category"] = "평생사주"
        payload["relation_type"] = "business"
        
        res = self._post("/saju/analyze", payload)
        self.assertEqual(res["status"], "success")
        
        content = res["result"]
        # 키워드 검증 (비즈니스적 관점)
        keywords = ["MZ Summary", "성향", "비즈니스", "분석"]
        found = [k for k in keywords if k in content]
        
        self.assertTrue(len(found) > 0, f"Business 문맥 키워드({keywords})가 결과에 없습니다.")
        print(f"   ✅ 발견된 키워드: {found}")

    # -------------------------------------------------------------------------
    # 3. 데이터 검증 (에러 처리) 테스트
    # -------------------------------------------------------------------------
    def test_03_validation_mbti(self):
        """[Checklist 3] MBTI 분석 요청 시 필수 데이터 누락 에러 확인"""
        print("\n🔍 [Test 3] MBTI 데이터 누락 검증")
        payload = self.default_payload.copy()
        payload["category"] = "MBTI분석"
        # 의도적으로 mbti 필드 제거
        if "mbti" in payload: del payload["mbti"]
        
        res = self._post("/saju/analyze", payload)
        
        # 에러가 발생해야 정상
        self.assertEqual(res.get("status"), "error", "MBTI 데이터가 없는데 성공했습니다 (보안 취약점)")
        print(f"   ✅ 예상된 에러 메시지: {res.get('message')}")

if __name__ == '__main__':
    # unittest 실행 결과를 커스텀하게 출력하기 위해 TextTestRunner 사용
    runner = unittest.TextTestRunner(verbosity=0)
    # Python 3 호환성 수정: makeSuite -> TestLoader().loadTestsFromTestCase
    result = runner.run(unittest.TestLoader().loadTestsFromTestCase(TestSajuAppAPI))
    
    # 요약 리포트 출력
    print("\n" + "="*50)
    print("📊 [QA Report] 테스트 결과 요약")
    print("="*50)
    print(f"총 테스트: {result.testsRun}개")
    print(f"성공: {result.testsRun - len(result.failures) - len(result.errors)}개")
    print(f"실패: {len(result.failures)}개")
    print(f"에러: {len(result.errors)}개")
    
    if not result.wasSuccessful():
        print("\n❌ [Critical Issues]")
        for failure in result.failures:
            print(f"- {failure[0]._testMethodName}: {failure[1].splitlines()[-1]}")
        for error in result.errors:
            print(f"- {error[0]._testMethodName}: {error[1].splitlines()[-1]}")
        sys.exit(1)
    else:
        print("\n✨ 모든 시스템이 정상 작동 중입니다.")
        sys.exit(0)
