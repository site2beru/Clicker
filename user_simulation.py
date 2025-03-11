# Эмуляция юзера

from fake_useragent import UserAgent
import random


def get_random_mobile_user_agent():
    ua = UserAgent()
    return ua.chrome if 'Mobile' in ua.chrome else ua.safari


def get_random_fingerprint():
    screen_resolutions = [
        "320x480", "375x667", "390x844", "393x786", "360x640",
        "360x740", "360x780", "412x915", "414x736", "414x896"
    ]

    return {
        "screen_resolution": random.choice(screen_resolutions),
        "language": random.choice(["ru-RU", "ru"]),
        "platform": random.choice(["Linux armv8l", "Linux armv7l", "iPhone", "iPad"])
    }