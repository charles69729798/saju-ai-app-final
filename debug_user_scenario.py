
import asyncio
import os
from playwright.async_api import async_playwright

# Data from User Screenshot
USER_DATA = {
    "birth_date": "2004-07-17",
    "birth_time": "09:18",
    "name": "홍길동",
    "mbti": "INTJ",
    "target_name": "이사이",
    "target_birth": "2010-05-03",
    "target_time": "12:00",
    "target_mbti": "ESTJ",
    "relation_type": "lover"
}

async def run():
    print("🚀 Starting User Scenario Debug (Visible Mode)...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()

        # --- DIAGNOSTIC LISTENERS ---
        page.on("console", lambda msg: print(f"📝 Browser Console: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"❌ Browser JS Error: {exc}"))
        page.on("requestfailed", lambda req: print(f"❌ Network Fail: {req.url} - {req.failure}"))
        
        try:
            print("🌍 Navigating...")
            await page.goto("http://localhost:8000")
            
            print(f"⌨️ Inputting User Data: {USER_DATA['birth_date']}")
            # 1. Relation
            await page.click(f".chip[data-type='{USER_DATA['relation_type']}']")
            
            # 2. User Info
            await page.fill("#nameKorean", USER_DATA['name'])
            await page.fill("#birthDate", USER_DATA['birth_date'])
            await page.fill("#birthTime", USER_DATA['birth_time'])
            await page.select_option("#mbti", USER_DATA['mbti'])
            
            # 3. Target Info
            print(f"⌨️ Inputting Target Data: {USER_DATA['target_birth']}")
            await page.fill("#targetName", USER_DATA['target_name'])
            await page.fill("#targetBirthDate", USER_DATA['target_birth'])
            await page.fill("#targetBirthTime", USER_DATA['target_time'])
            await page.select_option("#targetMbti", USER_DATA['target_mbti'])
            
            # 4. Analyze
            print("👆 Clicking Analyze...")
            await page.click(".btn-primary")
            
            # 5. Wait/Check
            try:
                # Wait for either result or error message
                await page.wait_for_selector("#result h2, #error.show", timeout=5000)
                
                # Check for error
                error_el = await page.query_selector("#error.show")
                if error_el:
                    err_text = await error_el.inner_text()
                    print(f"\n❌ CAPTURED UI ERROR: {err_text}")
                else:
                    success_el = await page.query_selector("#result h2")
                    if success_el:
                        text = await success_el.inner_text()
                        print(f"\n✅ SUCCESS: Result loaded - {text}")
                    else:
                        print("\n❓ Unknown State: No result or error found.")
                        
            except Exception as e:
                print(f"⚠️ Wait Exception: {e}")

            # Keep open briefly to see
            await page.wait_for_timeout(3000)
            
        except Exception as e:
            print(f"❌ Script Error: {e}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
