import requests
from bs4 import BeautifulSoup

def scrape_channel(url):
    response = requests.get(url, timeout=10)

    soup = BeautifulSoup(
        response.text,
        "lxml"
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
