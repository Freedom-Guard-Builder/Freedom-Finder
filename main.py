import os
import json
import random
from telegram_scraper import scrape_telegram_channel
from config_parser import extract_links
from config_filter import clean_config_list, is_valid_config
import re

CHANNELS = [
    "https://t.me/s/amirw_shop_q",
    "https://t.me/FG_Link"
]

# Subscription link patterns
SUB_PATTERNS = [
    r'https?://[^\s\'"<>]+',
]

# Mobile config protocols
MOBILE_PROTOCOLS = [
    "vmess://", "vless://", "trojan://", "ss://", "ssr://"
]

def is_subscription_link(link: str) -> bool:
    for pat in SUB_PATTERNS:
        if re.match(pat, link, re.IGNORECASE):
            return True
    return False

def is_mobile_config(cfg: str) -> bool:
    return any(cfg.startswith(proto) for proto in MOBILE_PROTOCOLS) or is_subscription_link(cfg)

def is_desktop_config(cfg: str) -> bool:
    return is_subscription_link(cfg)

def mix_configs(configs: list[str], count: int = 50) -> list[str]:
    return random.sample(configs, min(count, len(configs)))

def categorize_configs(configs: list[str]):
    categories = {
        "PUBLIC": [],
        "MCI": [],
        "IRANCELL": [],
        "RIGHTEL": [],
        "PISHGAMAN": [],
        "TCI": [],
        "SHATEL": [],
        "PARSONLINE": [],
        "other": [],
        "MOBILE": []
    }
    for cfg in configs:
        if "mci" in cfg.lower():
            categories["MCI"].append(cfg)
        elif "irancell" in cfg.lower():
            categories["IRANCELL"].append(cfg)
        elif "rightel" in cfg.lower():
            categories["RIGHTEL"].append(cfg)
        elif "pishgaman" in cfg.lower():
            categories["PISHGAMAN"].append(cfg)
        elif "tci" in cfg.lower():
            categories["TCI"].append(cfg)
        elif "shatel" in cfg.lower():
            categories["SHATEL"].append(cfg)
        elif "parsonline" in cfg.lower():
            categories["PARSONLINE"].append(cfg)
        elif is_mobile_config(cfg):
            categories["MOBILE"].append(cfg)
        elif is_desktop_config(cfg):
            categories["PUBLIC"].append(cfg)
        else:
            categories["other"].append(cfg)
    return categories

def main():
    os.makedirs("out", exist_ok=True)
    all_posts = []
    for url in CHANNELS:
        print(f"[+] Scraping {url}")
        all_posts += scrape_telegram_channel(url)

    all_configs = extract_links(all_posts)
    filtered = [c for c in all_configs if is_valid_config(c) or is_subscription_link(c)]
    cleaned = clean_config_list(filtered)

    print(f"[✓] Total: {len(all_configs)}, Valid: {len(filtered)}, Unique: {len(cleaned)}")

    categories = categorize_configs(cleaned)

    desktop_subs = [c for c in cleaned if is_subscription_link(c)]
    with open("out/desktop_subs.txt", "w", encoding="utf-8") as f:
        for sub in desktop_subs:
            f.write(sub + "\n")

    mobile_configs = [c for c in cleaned if is_mobile_config(c)]
    with open("out/mobile_configs.txt", "w", encoding="utf-8") as f:
        for cfg in mobile_configs:
            f.write(cfg + "\n")
    
    mixed_configs = mix_configs(cleaned, count=100)
    with open("out/mixed_configs.txt", "w", encoding="utf-8") as f:
        for cfg in mixed_configs:
            f.write(cfg + "\n")
    non_sub_configs = [c for c in cleaned if not is_subscription_link(c)]
    with open("out/configs.txt", "w", encoding="utf-8") as f:
        for cfg in non_sub_configs:
            f.write(cfg + "\n")

    with open("out/configs.json", "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=4)

    print("[✓] Exported configs to out/configs.json, out/configs.txt, out/mobile_configs.txt, out/desktop_subs.txt")

if __name__ == "__main__":
    main()