import re

PATTERN = re.compile(
    r'(vmess://[^\s]+|vless://[^\s]+|trojan://[^\s]+|ss://[^\s]+|ssr://[^\s]+)',
    re.IGNORECASE
)

TG_PATTERN = re.compile(r'(?:https?://)?t\.me/[^\s)]+', re.IGNORECASE)

def extract_configs(texts):
    configs = []

    for text in texts:
        configs.extend(PATTERN.findall(text))

    return configs

def extract_proxies_tg(texts):
    proxies = []

    for text in texts:
        # get proxies tg from text
        proxies.extend(TG_PATTERN.findall(text))
        
    return proxies