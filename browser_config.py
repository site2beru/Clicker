# настройки браузера и куки
# робот запускается в Хроме, открывая его. можно попробовать добавить в options "headless"

import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_browser(user_agent, fingerprint, proxy=None):
    options = Options()
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument(f'--window-size={fingerprint["screen_resolution"]}')
    options.add_argument(f'--lang={fingerprint["language"]}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-webrtc')

    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

    driver = webdriver.Chrome(options=options)

    # первый визит для установки печенег
    driver.get("https://ya.ru")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    driver.add_cookie({"name": "session_id", "value": f"session_{random.randint(1000, 9999)}", "domain": "ya.ru"})

    return driver
