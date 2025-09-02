
from crewai.tools import tool
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import base64

def _driver(headless=True):
    opts = webdriver.ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1400,900")
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opts)

@tool("visit_site")
def visit_site(url: str) -> str:
    """Open URL and return 'TITLE: ... | H1: ...'."""
    d = _driver(headless=True)
    try:
        d.get(url)
        WebDriverWait(d, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        title = d.title or ""
        h1 = ""
        try:
            h1 = d.find_element(By.TAG_NAME, "h1").text.strip()
        except Exception:
            pass
        return f"TITLE: {title} | H1: {h1}"
    finally:
        d.quit()

@tool("simple_search")
def simple_search(query: str) -> str:
    """Search DuckDuckGo for 'query' and return top 5 'title — link' lines."""
    d = _driver(headless=True)
    try:
        d.get("https://duckduckgo.com/")
        WebDriverWait(d, 15).until(EC.presence_of_element_located((By.ID, "searchbox_input")))
        box = d.find_element(By.ID, "searchbox_input")
        box.clear(); box.send_keys(query); box.submit()
        WebDriverWait(d, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-testid='result-title-a']")))
        items = d.find_elements(By.CSS_SELECTOR, "a[data-testid='result-title-a']")[:5]
        out = []
        for a in items:
            title = a.text.strip()
            href = a.get_attribute("href")
            if title and href:
                out.append(f"- {title} — {href}")
        return "\n".join(out) if out else "No results."
    finally:
        d.quit()

@tool("page_screenshot_b64")
def page_screenshot_b64(url: str) -> str:
    """Open URL and return a base64 PNG screenshot (short strings only)."""
    d = _driver(headless=True)
    try:
        d.get(url)
        WebDriverWait(d, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        png = d.get_screenshot_as_png()
        return base64.b64encode(png).decode("utf-8")
    finally:
        d.quit()
