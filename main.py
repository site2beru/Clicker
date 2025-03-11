# 05.03.2025 usp
# чудо-бот для захода на сайты через Яшу по заданным поисковым запросам
# используем прокси, куки и фингерпринты
#
# алгоритм действий следующий:
# 1. открываем браузер, заходим на яндекс с ключевиком (задается в конце файла)
# 2. ищем нужный нам сайт (задается в конце файла)
# 3. тыкаем на него и сразу сваливаем
# 4. ждем N-ное время и идем еще раз
#
# main — этот файл — исполняет запуск
# proxy_handler — настройки прокси
# browser_config — конфигурация
# website_visitor — процесс поиска по страницам
# user_simulation – настройки девайса пользователя
#
# с проверкой на робота случаются проблемы

import random
import time
from browser_config import setup_browser
from proxy_handler import get_random_proxy, check_proxy
from user_simulation import get_random_mobile_user_agent, get_random_fingerprint
from website_visitor import WebsiteVisitor


def main():
    visitor = WebsiteVisitor()
    target_website = "afanasy.biz" # что ищем
    search_keywords = ["новости тверь"] # запросы

    # глубина страниц и использование прокси
    for i in range(3):
        visitor.simulate_visit(target_website, search_keywords, use_proxy=False, max_pages=5) # True, если нам нужно прокси
        if i < 2:
            time.sleep(random.randint(30, 120))


if __name__ == "__main__":
    main()
