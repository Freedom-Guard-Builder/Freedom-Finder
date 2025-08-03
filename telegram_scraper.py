import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_telegram_channel(channel_url: str, max_pages=10):
    posts = []
    for i in range(1, max_pages + 1):
        url = f"{channel_url}?before={i * 20}"
        try:
            res = requests.get(url, headers=HEADERS, timeout=6000)
            if res.status_code != 200:
                print(f"[!] Failed to load page {i}")
                break
            soup = BeautifulSoup(res.text, 'html.parser')
            msgs = soup.find_all("div", class_="tgme_widget_message_text")
            for msg in msgs:
                posts.append(msg.get_text("\n"))
        except Exception as e:
            print(f"[!] Error: {e}")
        time.sleep(0.2)
    return posts
