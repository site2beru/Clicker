# Поиск. Ходим по страницам и ищем

import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser_config import setup_browser
from proxy_handler import get_random_proxy
from user_simulation import get_random_mobile_user_agent, get_random_fingerprint


class WebsiteVisitor:
    def __init__(self):
        self.search_url = 'https://ya.ru/search/?text='
        self.result_selectors = [
            '.serp-item a.link',
            '.serp-item a.Link_theme_normal',
            '.organic__url',
            '//a[contains(@href, "clck.yandex.ru")]'
        ]
        # ищем на странице кнопку "Показать еще"
        self.next_page_selectors = [
            'button[data-counter="["b"]"]',  # обычно это оно
            '.pager__item_type_next',  # другие версии
            '//a[contains(@class, "pager__item") and contains(@href, "page=")]'  # еще другие версии — пагинация
        ]

    def simulate_visit(self, target_website, keywords, use_proxy=True, max_pages=5):
        user_agent = get_random_mobile_user_agent()
        fingerprint = get_random_fingerprint()
        proxy = get_random_proxy() if use_proxy else None

        driver = setup_browser(user_agent, fingerprint, proxy)

        try:
            # ищем
            selected_keyword = random.choice(keywords)
            driver.get(f"{self.search_url}{selected_keyword}")

            # если нарвались на капчу — пробуем еще раз
            if self._check_captcha(driver):
                print("попали на капчу, перезапуск...")
                driver.quit()
                return self.simulate_visit(target_website, keywords, use_proxy, max_pages)

            # ходим по страницам]
            for page in range(max_pages):
                print(f"ищем на странице {page + 1}/{max_pages}")

                if self._find_and_click_target(driver, target_website):
                    visit_time = random.uniform(3.0, 8.0)
                    print(f"заходим на сайт и ждем {visit_time:.1f} секунд")
                    time.sleep(visit_time)
                    driver.quit()
                    return True

                # не нашли — ищем на следующей
                if page < max_pages - 1:
                    if not self._go_to_next_page(driver):
                        print("больше нечего ловить")
                        break
                    time.sleep(random.uniform(1.0, 3.0))

            print(f"Could not find {target_website} within {max_pages} pages")
            return False

        except Exception as e:
            driver.save_screenshot(f"error_{int(time.time())}.png")
            return False
        finally:
            driver.quit()

    def _check_captcha(self, driver):
        captcha_indicators = [
            '//input[@name="rep"]',
            '//img[contains(@src, "captcha")]',
            '//*[contains(text(), "Подтвердите, что") or contains(text(), "робот")]'
        ]
        return any(driver.find_elements(By.XPATH, indicator) for indicator in captcha_indicators)

    def _find_and_click_target(self, driver, target_website):
        for selector in self.result_selectors:
            try:
                method = By.XPATH if selector.startswith('//') else By.CSS_SELECTOR
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((method, selector)))
                results = driver.find_elements(method, selector)

                for result in results:
                    href = result.get_attribute('href')
                    if href and target_website in href:
                        driver.execute_script("arguments[0].scrollIntoView(true);", result)
                        time.sleep(random.uniform(0.5, 1.5))
                        try:
                            result.click()
                        except:
                            driver.execute_script("arguments[0].click();", result)
                        if len(driver.window_handles) > 1:
                            driver.switch_to.window(driver.window_handles[-1])
                        return True
            except:
                continue
        return False

    def _go_to_next_page(self, driver):

        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(0.5, 1.0))

            for selector in self.next_page_selectors:
                try:
                    method = By.XPATH if selector.startswith('//') else By.CSS_SELECTOR
                    next_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((method, selector))
                    )

                    if next_button.is_displayed():
                        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                        time.sleep(random.uniform(0.5, 1.0))
                        try:
                            next_button.click()
                        except:
                            driver.execute_script("arguments[0].click();", next_button)
                        # загрузка результатов
                        WebDriverWait(driver, 10).until(
                            EC.staleness_of(next_button)
                        )
                        return True
                except:
                    continue

            return False  # если не нашли кнопку слдеующей страницы
        except Exception as e:
            print(f"Error navigating to next page: {e}")
            return False