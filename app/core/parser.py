import re

PATTERN = re.compile(
    r'(vmess://[^\s]+|vless://[^\s]+|trojan://[^\s]+|ss://[^\s]+|ssr://[^\s]+)',
    re.IGNORECASE
)

def extract_configs(texts):
    configs = []

    for text in texts:
        configs.extend(PATTERN.findall(text))

    return configs

def extract_proxies_tg(texts):
    proxies = []

    for text in texts:
        # if text contains proxy link
        if "https://t.me/proxy?" in text:
            proxies.append(text)
        
    return proxies