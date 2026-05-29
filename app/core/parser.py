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
