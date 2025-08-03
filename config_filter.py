def clean_config_list(configs: list[str]) -> list[str]:
    seen = set()
    result = []
    for c in configs:
        if c.strip() == "":
            continue
        sig = hash(c.strip().lower())
        if sig not in seen:
            seen.add(sig)
            result.append(c)
    return result

def is_valid_config(cfg: str) -> bool:
    return any(cfg.startswith(proto) for proto in [
        "vmess://", "vless://", "trojan://", "ss://", "ssr://",
        "tuic://", "hysteria://", "hysteria2://", "snell://",
        "mtproto://", "warp://", "juicity://", "ssh://", "socks5://"
    ]) and len(cfg) > 10
