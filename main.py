import os
from telegram_scraper import scrape_telegram_channel
from config_parser import extract_links
from config_filter import clean_config_list, is_valid_config
from config_exporter import export_txt, export_base64, export_html_index
from config_tester import test_ping_or_download
import time

CHANNELS = [
    "https://t.me/s/V2rayCollectors",
    "https://t.me/s/V2rayFreeDaily",
    "https://t.me/s/OutlineVpnServer",
    "https://t.me/s/MTProoProxy",
    "https://t.me/s/Proxy_For_You"
]

def main():
    os.makedirs("out", exist_ok=True)
    all_posts = []
    for url in CHANNELS:
        print(f"[+] Scraping {url}")
        all_posts += scrape_telegram_channel(url)

    all_configs = extract_links(all_posts)
    filtered = [c for c in all_configs if is_valid_config(c)]
    cleaned = clean_config_list(filtered)

    print(f"[✓] Total: {len(all_configs)}, Valid: {len(filtered)}, Unique: {len(cleaned)}")

    # Speed test
    print(f"[!] Starting speed test on {len(cleaned)} configs...")
    tested = []
    for config in cleaned:
        res = test_ping_or_download(config)
        if res["success"]:
            tested.append(res)
        if len(tested) >= 300:
            break
        time.sleep(0.1)

    tested = sorted(tested, key=lambda x: x['ping'])
    top_configs = [r["proxy"] for r in tested]

    export_txt(top_configs, "out/top300.txt")
    export_base64(top_configs, "out/top300_base64.txt")
    export_html_index(top_configs, "out/index.html")

if __name__ == "__main__":
    main()
