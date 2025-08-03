import requests
from config_parser import extract_links
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
def fetch_sub_links_from_raw_url(raw_url):
    try:
        res = requests.get(raw_url, headers=HEADERS)
        if res.status_code == 200:
            return res.text.split("\n")
        else:
            print(f"[!] Failed to fetch {raw_url}")
            return []
    except Exception as e:
        print(f"[!] Error fetching {raw_url}: {e}")
        return []
