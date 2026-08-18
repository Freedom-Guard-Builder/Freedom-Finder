import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0"
    )
}

def scrape_channel(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        messages = soup.select(
            ".tgme_widget_message_text"
        )

        return [
            m.get_text(
                separator=" ",
                strip=True
            )
            for m in messages
        ]

    except Exception as e:
        print(f"[ERROR] {url} -> {e}")
        return []