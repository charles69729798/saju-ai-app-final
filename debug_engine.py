
import sys
import os
import json

# backend 디렉토리를 경로에 추가
sys.path.append(os.path.join(os.getcwd(), "backend"))

from fortune_generator import generate_fortune

def debug_test():
    print("--- Debugging generate_fortune ---")
    birth_date = "2004-08-31"
    birth_time = "12:00"
    categories = ["평생사주", "재물운", "직업운", "애정운", "건강운", "신년운세"]
    user_profile = {
        "name": "charles",
        "gender": "M",
        "job": "developer",
        "mbti": "INTJ",
        "blood_type": "O",
        "name_hanja": "",
        "relation_type": "boss"
    }
    
    for cat in categories:
        print(f"Testing Category: {cat}...", end="")
        try:
            result = generate_fortune(birth_date, birth_time, cat, user_profile)
            if result.get("status") == "success":
                print(" ✅ OK")
            else:
                print(f" ❌ Failed: {result.get('message')}")
        except Exception as e:
            print(f" 💥 CRASHED: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_test()
