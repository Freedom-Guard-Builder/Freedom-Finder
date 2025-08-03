import re

def extract_links(texts: list[str]) -> list[str]:
    proxies = []
    pattern = r'(vmess://[^\s]+|vless://[^\s]+|trojan://[^\s]+|ss://[^\s]+|ssr://[^\s]+|tuic://[^\s]+|hysteria2?://[^\s]+|snell://[^\s]+|mtproto://[^\s]+|ssh://[^\s]+|warp://[^\s]+|juicity://[^\s]+|socks5://[^\s]+)'
    for text in texts:
        found = re.findall(pattern, text, re.IGNORECASE)
        proxies.extend(found)
    return proxies
