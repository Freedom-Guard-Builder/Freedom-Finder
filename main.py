import os
import re
import json
import random
import logging
from datetime import datetime
from sub_scraper import fetch_sub_links_from_raw_url
from telegram_scraper import scrape_telegram_channel
from config_parser import extract_links
from config_filter import clean_config_list, is_valid_config

# Setup
CHANNELS = [
    "https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt",
    "https://t.me/FG_Link",
    "https://t.me/sinavm",
    "https://t.me/ir2ray_free",
    "https://t.me/s/amirw_shop_q",
    "https://t.me/v2ray_configs_pools",
    "https://t.me/Rayan_Config"
]

SUB_PATTERNS = [r'https?://[^\s\'"<>]+']
MOBILE_PROTOCOLS = ["vmess://", "vless://", "trojan://", "ss://", "ssr://"]
BLOCKED_DOMAINS = ["porn", "facebook.com"]

# Setup logger
os.makedirs("out", exist_ok=True)
logging.basicConfig(filename="out/log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Core helpers
def is_subscription_link(link: str) -> bool:
    return any(re.match(pat, link, re.IGNORECASE) for pat in SUB_PATTERNS)

def is_mobile_config(cfg: str) -> bool:
    return any(cfg.startswith(proto) for proto in MOBILE_PROTOCOLS)

def is_blocked(link: str) -> bool:
    return any(domain in link for domain in BLOCKED_DOMAINS)

def unique(seq: list[str]) -> list[str]:
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]

def mix_configs(configs: list[str], count: int = 50) -> list[str]:
    return random.sample(configs, min(count, len(configs)))

def categorize_configs(configs: list[str]) -> dict:
    cats = {
        "PUBLIC": [], "MCI": [], "IRANCELL": [], "RIGHTEL": [], "PISHGAMAN": [],
        "TCI": [], "SHATEL": [], "PARSONLINE": [], "MOBILE": [], "other": []
    }
    for cfg in configs:
        low = cfg.lower()
        if "mci" in low: cats["MCI"].append(cfg)
        elif "irancell" in low: cats["IRANCELL"].append(cfg)
        elif "rightel" in low: cats["RIGHTEL"].append(cfg)
        elif "pishgaman" in low: cats["PISHGAMAN"].append(cfg)
        elif "tci" in low: cats["TCI"].append(cfg)
        elif "shatel" in low: cats["SHATEL"].append(cfg)
        elif "parsonline" in low: cats["PARSONLINE"].append(cfg)
        elif is_mobile_config(cfg): cats["MOBILE"].append(cfg)
        elif is_subscription_link(cfg): cats["PUBLIC"].append(cfg)
        else: cats["other"].append(cfg)
    return cats

def main():
    start = datetime.now()
    all_posts, all_configs = [], []

    for url in CHANNELS:
        print(f"[+] {url}")
        try:
            if "t.me" in url:
                all_posts += scrape_telegram_channel(url)
            else:
                all_configs += fetch_sub_links_from_raw_url(url)
        except Exception as e:
            logging.error(f"ERROR scraping {url}: {e}")

    all_configs += extract_links(all_posts)

    # Filter & clean
    filtered = [c for c in all_configs if (is_valid_config(c) or is_subscription_link(c)) and not is_blocked(c)]
    cleaned = unique(clean_config_list(filtered))

    print(f"[✓] Total: {len(all_configs)}, Valid: {len(filtered)}, Unique: {len(cleaned)}")

    # Categorize
    categories = categorize_configs(cleaned)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    # Save by category
    def save_list(name, data, folder = "out"):
        with open(f"{folder}/{name}_{timestamp}.txt", "w", encoding="utf-8") as f:
            for line in data:
                f.write(line + "\n")

    desktop_subs = [c for c in cleaned if is_subscription_link(c)]
    save_list("desktop_subs", desktop_subs)

    mobile_configs = [c for c in cleaned if is_mobile_config(c)]
    save_list("mobile_configs", mobile_configs)

    non_subs = [c for c in cleaned if not is_subscription_link(c)]
    save_list("configs", non_subs)

    mixed = mix_configs(cleaned, count=100)
    save_list("mixed_configs", mixed)

    # Save by protocol
    proto_map = {proto: [] for proto in MOBILE_PROTOCOLS}
    for cfg in mobile_configs:
        for proto in MOBILE_PROTOCOLS:
            if cfg.startswith(proto):
                proto_map[proto].append(cfg)
                break

    for proto, cfgs in proto_map.items():
        save_list(proto.replace("://", ""), cfgs, "protocols")

    # JSON exports
    with open(f"out/configs_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)

    with open(f"out/protocols_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump({k.replace("://", ""): v for k, v in proto_map.items()}, f, ensure_ascii=False, indent=2)

    # Summary
    print("\n[📦] Summary:")
    for cat, items in categories.items():
        print(f"{cat}: {len(items)}")

    for proto, items in proto_map.items():
        print(f"{proto.replace('://', '')}: {len(items)}")

    print(f"\n[✓] Finished in {datetime.now() - start}")

if __name__ == "__main__":
    main()
