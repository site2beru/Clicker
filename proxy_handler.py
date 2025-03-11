# настройки прокси

import json
import os
import random
import requests


def get_random_proxy():
    try:
        proxy_file = "proxies.json" # файл с проксями. должен содержать ip и порт
        if not os.path.exists(proxy_file):
            print(f"Proxy file {proxy_file} not found")
            return None

        with open(proxy_file, 'r', encoding='utf-8') as f:
            proxy_data = json.load(f)

        if not isinstance(proxy_data, list):
            print("Expected proxy list in JSON file")
            return None

        selected_proxy = random.choice(proxy_data)
        ip, port = selected_proxy.get('IP_Address'), selected_proxy.get('Port')

        if not ip or not port:
            print("Selected proxy missing IP or port")
            return None

        proxy_str = f"{ip}:{port}"
        return proxy_str if check_proxy(proxy_str) else get_random_proxy()

    except Exception as e:
        print(f"Error getting proxy: {e}")
        return None


def check_proxy(proxy):
    try:
        response = requests.get("https://ya.ru", proxies={"http": proxy, "https": proxy}, timeout=5)
        return response.status_code == 200
    except:
        return False
