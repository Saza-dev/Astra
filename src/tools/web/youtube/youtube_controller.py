import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class YouTubeController:
    def __init__(self, headless: bool = False):
        opts = webdriver.ChromeOptions()
        if headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opts)
        self.wait = WebDriverWait(self.driver, 20)

    # ---------- helpers ----------
    def _accept_cookies_if_present(self):
        try:
            # Varies by region; try common button texts
            for text in ["Accept all", "I agree", "Accept", "AGREE", "Yes, I’m in"]:
                btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, f"//button[.//text()[contains(., '{text}')]]"))
                )
                btn.click()
                return
        except Exception:
            pass

    def _player(self):
        return self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "html5-video-player")))

    def _video(self):
        # <video> tag is easiest for JS control
        return self.driver.find_element(By.CSS_SELECTOR, "video.html5-main-video")

    def _focus_player(self):
        p = self._player()
        ActionChains(self.driver).move_to_element(p).click().perform()

    def _skip_ad_if_possible(self):
        try:
            skip = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".ytp-ad-skip-button, .ytp-ad-skip-button-modern"))
            )
            skip.click()
        except Exception:
            pass

    # ---------- core flows ----------
    def open_home(self):
        self.driver.get("https://www.youtube.com")
        self._accept_cookies_if_present()

    def play_query(self, query: str):
        self.open_home()
        box = self.wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
        box.clear()
        box.send_keys(query)
        box.submit()
        first = self.wait.until(EC.element_to_be_clickable((By.ID, "video-title")))
        first.click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "html5-video-player")))
        self._skip_ad_if_possible()
        self._focus_player()

    def play_url(self, url: str):
        self.driver.get(url)
        self._accept_cookies_if_present()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "html5-video-player")))
        self._skip_ad_if_possible()
        self._focus_player()

    # ---------- playback controls (keyboard + JS) ----------
    def toggle_play_pause(self):
        self._focus_player()
        ActionChains(self.driver).send_keys(Keys.SPACE).perform()

    def pause(self):
        self._focus_player()
        # if already playing, SPACE pauses; if paused, do nothing by checking video.paused
        paused = self.driver.execute_script("return document.querySelector('video')?.paused")
        if paused is False:
            ActionChains(self.driver).send_keys(Keys.SPACE).perform()

    def play(self):
        self._focus_player()
        paused = self.driver.execute_script("return document.querySelector('video')?.paused")
        if paused:
            ActionChains(self.driver).send_keys(Keys.SPACE).perform()

    def seek(self, seconds: int):
        # positive = forward, negative = backward
        self._focus_player()
        if seconds >= 0:
            # ArrowRight seeks ~5s; do multiple taps
            taps = max(1, seconds // 5)
            for _ in range(taps):
                ActionChains(self.driver).send_keys(Keys.ARROW_RIGHT).perform()
                time.sleep(0.05)
        else:
            taps = max(1, abs(seconds) // 5)
            for _ in range(taps):
                ActionChains(self.driver).send_keys(Keys.ARROW_LEFT).perform()
                time.sleep(0.05)

    def set_time_exact(self, seconds: float):
        # precise seek with JS
        self.driver.execute_script("let v=document.querySelector('video'); if(v){v.currentTime=arguments[0];}", seconds)

    def next_video(self):
        self._focus_player()
        # YouTube next: Shift + n
        ActionChains(self.driver).key_down(Keys.SHIFT).send_keys('N').key_up(Keys.SHIFT).perform()

    def previous_video(self):
        self._focus_player()
        # YouTube previous: Shift + p
        ActionChains(self.driver).key_down(Keys.SHIFT).send_keys('P').key_up(Keys.SHIFT).perform()

    def mute_toggle(self):
        self._focus_player()
        # 'm' toggles mute
        ActionChains(self.driver).send_keys('m').perform()

    def set_volume_percent(self, percent: int):
        # 0..100 via JS volume 0..1
        pct = max(0, min(100, percent))
        self.driver.execute_script("let v=document.querySelector('video'); if(v){v.volume=arguments[0];}", pct/100)

    def captions_toggle(self):
        self._focus_player()
        # 'c' toggles subtitles
        ActionChains(self.driver).send_keys('c').perform()

    def theater_toggle(self):
        self._focus_player()
        # 't' toggles theater mode
        ActionChains(self.driver).send_keys('t').perform()

    def fullscreen_toggle(self):
        self._focus_player()
        # 'f' toggles fullscreen
        ActionChains(self.driver).send_keys('f').perform()

    def like(self):
        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, "ytd-toggle-button-renderer:nth-of-type(1) button")
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            btn.click()
        except Exception:
            pass

    def subscribe(self):
        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, "ytd-subscribe-button-renderer button")
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            btn.click()
        except Exception:
            pass

    def info(self) -> dict:
        # returns a small status snapshot
        title = ""
        try:
            title = self.driver.find_element(By.CSS_SELECTOR, "h1.ytd-watch-metadata").text.strip()
        except Exception:
            pass
        current = self.driver.execute_script("let v=document.querySelector('video'); return v? v.currentTime : null;")
        duration = self.driver.execute_script("let v=document.querySelector('video'); return v? v.duration : null;")
        muted = self.driver.execute_script("let v=document.querySelector('video'); return v? v.muted : null;")
        volume = self.driver.execute_script("let v=document.querySelector('video'); return v? v.volume : null;")
        paused = self.driver.execute_script("let v=document.querySelector('video'); return v? v.paused : null;")
        return {
            "title": title,
            "current_time": current,
            "duration": duration,
            "muted": muted,
            "volume_pct": int((volume or 0)*100) if volume is not None else None,
            "paused": paused
        }

    def close(self):
        self.driver.quit()


# quick manual test
if __name__ == "__main__":
    yt = YouTubeController(headless=False)
    yt.play_query("lofi girl live")
    time.sleep(3)
    yt.pause()
    time.sleep(1)
    yt.play()
    yt.seek(20)
    yt.captions_toggle()
    print(yt.info())
    yt.close()
