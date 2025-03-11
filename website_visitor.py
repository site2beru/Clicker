# собственно, непосредственно поиск.
# заходим на яндекс, ищем в выдаче ссылки с нужным нам сайтом
# если не находим, ищем кнопку "Показать еще" и жмем ее
# повторяем, если не получилось найти, пока не найдем
# если находим сайт, заходим на него и сразу сваливаем

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
        # селектор для кнопки "Показать ещё"
        self.next_page_selectors = [
            '.Pager' # кнопка с эвентом на подгрузку результатов это div class="чтотодинамическое Pager"
        ]

    def simulate_visit(self, target_website, keywords, use_proxy=True, max_pages=5):
        user_agent = get_random_mobile_user_agent()
        fingerprint = get_random_fingerprint()
        proxy = get_random_proxy() if use_proxy else None

        driver = setup_browser(user_agent, fingerprint, proxy)

        try:
            selected_keyword = random.choice(keywords)
            driver.get(f"{self.search_url}{selected_keyword}")

            if self._check_captcha(driver):
                print("Попали на капчу, перезапуск...")
                driver.quit()
                return self.simulate_visit(target_website, keywords, use_proxy, max_pages)

            for page in range(max_pages):
                print(f"Ищем на странице {page + 1}/{max_pages}")

                if self._find_and_click_target(driver, target_website):
                    visit_time = random.uniform(0.1, 0.3)
                    #print(f"Заходим на сайт и ждем {visit_time:.1f} секунд")
                    time.sleep(visit_time)
                    driver.quit()
                    return True

                if page < max_pages - 1:
                    #print("Сайт не найден, ищем дальше")
                    if not self._go_to_next_page(driver):
                        #print("Не удалось перейти на следующую страницу или больше страниц нет")
                        break
                    time.sleep(random.uniform(1.0, 3.0))

            print(f"Не удалось найти {target_website} в пределах {max_pages} страниц")
            return False

        except Exception as e:
            print(f"Ошибка: {e}")
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
        # Переход на следующую страницу поиска через кнопку 'Показать ещё'
        try:
            # Прокручиваем вниз, чтобы подгрузить кнопку
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1.0, 2.0))

            for selector in self.next_page_selectors:
                try:
                    method = By.XPATH if selector.startswith('//') else By.CSS_SELECTOR
                    # Ждем появления кликабельной кнопки
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((method, selector))
                    )

                    if next_button.is_displayed() and next_button.is_enabled():
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                        time.sleep(random.uniform(0.5, 1.0))
                        try:
                            next_button.click()
                        except:
                            driver.execute_script("arguments[0].click();", next_button)

                        # Ждем обновления контента
                        WebDriverWait(driver, 10).until(
                            lambda driver: len(driver.find_elements(By.XPATH, "//div[contains(@class, 'serp-item')]")) > 0
                        )
                        print("Новые результаты загружены")
                        return True
                    else:
                except Exception as e:
                    continue

            return False
        except Exception as e:
            #driver.save_screenshot(f"next_page_error_{int(time.time())}.png")
            return False


if __name__ == "__main__":
    visitor = WebsiteVisitor()
    target_website = "mastweb.ru"
    search_keywords = ["разработка сайтов тверь"]
    visitor.simulate_visit(target_website, search_keywords, use_proxy=False, max_pages=5)
