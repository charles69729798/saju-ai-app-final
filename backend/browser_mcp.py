from fastmcp import FastMCP
from playwright.sync_api import sync_playwright
import base64
import time
import os
from notebooklm_client import SajuNotebookLMClient

# Initialize MCP Server
mcp = FastMCP("Saju Browser Control")

# Constants
APP_URL = "http://localhost:8000"

def _get_browser_context(p, headless=False):
    """Launch browser and return context"""
    browser = p.chromium.launch(headless=headless)
    context = browser.new_context(
        viewport={'width': 1280, 'height': 800},
        locale='ko-KR'
    )
    return browser, context

# --- Implementation Logic (Separated for Testing) ---

def open_app_logic() -> str:
    """Implementation of open_app"""
    with sync_playwright() as p:
        browser, context = _get_browser_context(p, headless=False)
        page = context.new_page()
        try:
            page.goto(APP_URL)
            page.wait_for_load_state("networkidle")
            title = page.title()
            time.sleep(2) 
            return f"Successfully opened app. Title: {title}"
        except Exception as e:
            return f"Failed to open app: {str(e)}"
        finally:
            browser.close()

def run_saju_test_logic(
    name: str, 
    birth_date: str, 
    birth_time: str = "12:00", 
    gender: str = "M", 
    category: str = "평생사주",
    mbti: str = None,
    target_name: str = None,
    target_birth_date: str = None,
    target_birth_time: str = "12:00",
    target_gender: str = "F",
    target_mbti: str = None,
    relation_type: str = "lover"
) -> str:
    """Implementation of run_saju_test"""
    with sync_playwright() as p:
        browser, context = _get_browser_context(p, headless=False)
        page = context.new_page()
        
        try:
            # 1. Open App
            page.goto(APP_URL)
            page.wait_for_selector("#nameKorean")
            
            # 2. Fill User Info
            page.fill("#nameKorean", name)
            page.fill("#birthDate", birth_date)
            page.evaluate(f"document.getElementById('birthTime').value = '{birth_time}'")
            
            gender_selector = f"#userGenderToggle .gender-option[data-value='{gender}']"
            page.click(gender_selector)

            # MBTI Selection (Optional)
            if mbti:
                # Assuming chips have inner text matching MBTI
                # First, ensure MBTI grid is populated
                page.wait_for_selector("#userMbtiGrid .mbti-chip")
                mbti_chips = page.query_selector_all("#userMbtiGrid .mbti-chip")
                for chip in mbti_chips:
                    if chip.inner_text() == mbti:
                        chip.click()
                        break

            # 3. Fill Target Info (Optional - for Compatibility/Relation)
            if target_name:
                # Select Relation Type
                # Assuming chips have data-type attribute
                relation_chip_selector = f"#relationChips .chip[data-type='{relation_type}']"
                if page.query_selector(relation_chip_selector):
                    page.click(relation_chip_selector)
                
                # Fill Target Info
                page.fill("#targetName", target_name)
                
                if target_birth_date:
                    page.fill("#targetBirthDate", target_birth_date)
                
                page.evaluate(f"document.getElementById('targetBirthTime').value = '{target_birth_time}'")
                
                # Target Gender
                target_gender_selector = f"#targetGenderToggle .gender-option[data-value='{target_gender}']"
                if page.query_selector(target_gender_selector):
                    page.click(target_gender_selector)
                
                # Target MBTI
                if target_mbti:
                    page.wait_for_selector("#targetMbtiGrid .mbti-chip")
                    target_mbti_chips = page.query_selector_all("#targetMbtiGrid .mbti-chip")
                    for chip in target_mbti_chips:
                        if chip.inner_text() == target_mbti:
                            chip.click()
                            break
            
            # 4. Trigger Analysis
            page.wait_for_selector("#categoriesGrid button", timeout=5000)
            category_btn = page.get_by_role("button", name=category)
            
            if not category_btn.is_visible():
                buttons = page.query_selector_all(".category-btn")
                found = False
                for btn in buttons:
                    if category in btn.inner_text():
                        btn.click()
                        found = True
                        break
                if not found:
                    return f"Error: Category '{category}' not found."
            else:
                category_btn.click()
            
            # 5. Wait for Result
            try:
                page.wait_for_selector("#loading", state="visible", timeout=2000)
                page.wait_for_selector("#loading", state="hidden", timeout=30000)
            except:
                pass
            
            page.wait_for_selector("#result", state="visible", timeout=10000)
            
            # 6. Extract Data
            result_text = page.inner_text("#resultContent")
            
            # Screenshot
            os.makedirs("frontend/screenshots", exist_ok=True)
            screenshot_path = f"frontend/screenshots/test_result_{int(time.time())}_{category}.png"
            page.screenshot(path=screenshot_path, full_page=False)
            
            # Return FULL text for validation (summary created by caller if needed)
            return f"✅ Analysis Successful! [{category}]\n\n[Full Content]\n{result_text}\n\n(Screenshot saved to {screenshot_path})"

        except Exception as e:
            os.makedirs("frontend/screenshots", exist_ok=True)
            error_path = f"frontend/screenshots/error_{int(time.time())}.png"
            page.screenshot(path=error_path)
            return f"❌ Test Failed: {str(e)}\n(Error screenshot saved to {error_path})"
            
        finally:
            browser.close()

# --- MCP Tool Definitions ---

@mcp.tool()
def open_app() -> str:
    """
    Opens the Saju App in a visible browser window to check if it loads correctly.
    Returns the page title.
    """
    return open_app_logic()

@mcp.tool()
def run_saju_test(
    name: str, 
    birth_date: str, 
    birth_time: str = "12:00", 
    gender: str = "M", 
    category: str = "평생사주",
    mbti: str = None,
    target_name: str = None,
    target_birth_date: str = None,
    target_birth_time: str = "12:00",
    target_gender: str = "F",
    target_mbti: str = None,
    relation_type: str = "lover"
) -> str:
    """
    Executes an End-to-End test on the Saju App with full features including MBTI and Compatibility.
    """
    return run_saju_test_logic(
        name, birth_date, birth_time, gender, category,
        mbti, target_name, target_birth_date, target_birth_time, target_gender, target_mbti, relation_type
    )

@mcp.tool()
def query_notebooklm(prompt: str) -> str:
    """
    Query NotebookLM for information or insights related to Saju (or general topics).
    Returns the response from NotebookLM.
    Requires NOTEBOOKLM_COOKIES environment variable for real responses, otherwise returns mock data.
    """
    client = SajuNotebookLMClient()
    return client.query(prompt)

if __name__ == "__main__":
    mcp.run()
