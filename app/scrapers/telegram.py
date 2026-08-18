import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def scrape_channel(url, limit=200):
    messages = []
    before = None
    seen_ids = set()

    try:
        while len(messages) < limit:

            page_url = url

            if before:
                page_url += f"?before={before}"

            response = requests.get(
                page_url,
                headers=HEADERS,
                timeout=15
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            posts = soup.select(
                ".tgme_widget_message"
            )

            if not posts:
                break

            oldest_id = None

            for post in posts:

                data_post = post.get("data-post")

                if not data_post:
                    continue

                try:
                    post_id = int(
                        data_post.rsplit("/", 1)[1]
                    )
                except (ValueError, IndexError):
                    continue

                oldest_id = post_id

                if post_id in seen_ids:
                    continue

                seen_ids.add(post_id)

                text = post.select_one(
                    ".tgme_widget_message_text"
                )

                if text:
                    message = text.get_text(
                        separator=" ",
                        strip=True
                    )

                    if message:
                        messages.append(message)

                if len(messages) >= limit:
                    break

            if oldest_id is None:
                break

            if before == oldest_id:
                break

            before = oldest_id

        return messages[:limit]

    except Exception as e:
        print(f"[ERROR] {url} -> {e}")
        return []