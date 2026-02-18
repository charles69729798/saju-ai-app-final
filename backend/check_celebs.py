import requests

def test_celeb_search():
    url = "http://localhost:8000/api/celebs"
    params = {"search": "손흥민"}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            celebs = data.get("celebs", [])
            print(f"✅ 검색 성공: {len(celebs)}건 발견")
            for c in celebs:
                print(f"- {c['name']} ({c['category']})")
        else:
            print(f"❌ 검색 실패: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 연결 오류: {e}")

if __name__ == "__main__":
    test_celeb_search()
