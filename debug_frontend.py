
import asyncio
import os
from playwright.async_api import async_playwright

# Fix Environment for Playwright
if "HOME" not in os.environ and "USERPROFILE" in os.environ:
    os.environ["HOME"] = os.environ["USERPROFILE"]

async def run():
    async with async_playwright() as p:
        print("🚀 Launching Debug Browser (Headless)...")
        try:
            # devtools=True conflicts with headless=True in some versions, removing it.
            browser = await p.chromium.launch(headless=True)
        except Exception as e:
            print(f"❌ Browser Launch Failed: {e}")
            return
        context = await browser.new_context()
        page = await context.new_page()

        # 1. Capture Console Logs
        print("🎧 Attaching Console Listener...")
        page.on("console", lambda msg: print(f"[CONSOLE] {msg.type}: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"[JS ERROR] {exc}"))

        # 2. Capture Network Failures
        page.on("requestfailed", lambda req: print(f"[NETWORK FAIL] {req.url} - {req.failure}"))

        # 3. Navigate
        print("🌍 Navigating to http://localhost:8000")
        try:
            await page.goto("http://localhost:8000", timeout=10000)
        except Exception as e:
            print(f"❌ Navigation Failed: {e}")
            await browser.close()
            return

        # 4. Check Event Bindings (via interaction)
        print("\n🔍 Inspecting Interactive Elements...")
        
        # Check Chip
        chip = page.locator(".chip[data-type='business']")
        if await chip.count() > 0:
            print("✅ Found 'Business' Chip.")
            await chip.click()
            # Check if active class was added
            is_active = await chip.evaluate("el => el.classList.contains('active')")
            if is_active:
                print("✅ Click Event Worked: Chip has 'active' class.")
            else:
                print("❌ Click Event FAILED: Chip did NOT get 'active' class.")
        else:
            print("❌ 'Business' Chip NOT found.")

        # Check Install Banner
        banner = page.locator("#installBanner")
        is_visible = await banner.is_visible()
        print(f"ℹ️ Install Banner Visible? {is_visible}")
        
        # Check Analyze Button
        btn = page.locator(".btn-primary")
        if await btn.count() > 0:
            print("✅ Found 'Analyze' button.")
            # We won't click it to avoid full analysis wait, just checking presence/binding implied by earlier success
        else:
            print("❌ 'Analyze' button NOT found.")

        # 5. Extract Computed Styles (Layout Check)
        print("\n🎨 Checking Layout/Styles...")
        body_bg = await page.eval_on_selector("body", "el => getComputedStyle(el).backgroundImage")
        print(f"   Body Background: {body_bg[:50]}...")

        # 6. Screenshot
        print("\n📸 Saving Debug Screenshot...")
        await page.screenshot(path="debug_state.png")
        
        await browser.close()
        print("✅ Debug Session Complete.")

if __name__ == "__main__":
    asyncio.run(run())
