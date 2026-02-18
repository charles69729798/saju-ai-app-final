
import os
import asyncio
from playwright.async_api import async_playwright
import datetime

# CRITICAL: Fix for Windows $HOME environment variable issue
if "HOME" not in os.environ:
    if "USERPROFILE" in os.environ:
        os.environ["HOME"] = os.environ["USERPROFILE"]
        print(f"🔧 Set HOME to USERPROFILE: {os.environ['HOME']}")
    else:
        print("⚠️ Warning: USERPROFILE not found, Playwright might fail.")

async def run():
    async with async_playwright() as p:
        print("🚀 Launching Browser (Visual Mode)...")
        # Headless=False to let the user see the browser
        browser = await p.chromium.launch(headless=False, slow_mo=1000) 
        page = await browser.new_page()
        
        # 1. Navigate
        print("🌍 Navigating to http://localhost:8000 ...")
        await page.goto("http://localhost:8000")
        
        # 2. Select Relationship (Business)
        print("👆 Clicking 'Business' Chip...")
        # Check if chips are present
        await page.wait_for_selector(".chip[data-type='business']")
        await page.click(".chip[data-type='business']")
        
        # 3. Input Data
        print("⌨️ Entering User Data...")
        await page.fill("#nameKorean", "테스트유저")
        await page.fill("#birthDate", "1990-01-01")
        await page.fill("#birthTime", "12:00")
        await page.select_option("#mbti", "ISTJ")
        
        print("⌨️ Entering Target Data...")
        await page.fill("#targetName", "직장상사")
        await page.fill("#targetBirthDate", "1985-05-05")
        await page.fill("#targetBirthTime", "09:00")
        
        # 4. Click Analyze
        print("👆 Clicking 'Analyze'...")
        await page.click(".btn-primary")
        
        # 5. Wait for Result
        print("⏳ Waiting for Result...")
        try:
            # Wait for the result card to be visible
            await page.wait_for_selector("#result", state="visible", timeout=10000)
            # Wait a bit for animations
            await page.wait_for_timeout(2000) 
            
            # Scroll to bottom to see Unlock button
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            
            # 6. Capture Screenshot
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"saju_test_result_{timestamp}.png"
            filepath = os.path.abspath(filename)
            
            await page.screenshot(path=filepath, full_page=True)
            print(f"📸 Screenshot saved to: {filepath}")
            
            # Check for Unlock Button text
            content = await page.content()
            if "500원으로 확인" in content:
                print("✅ VERIFIED: 'Unlock' button is present.")
            else:
                print("❌ FAILED: 'Unlock' button NOT found.")
                
        except Exception as e:
            print(f"❌ Error during test: {e}")
            await page.screenshot(path="error_state.png")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
