from app.settings import MOBILE_PROTOCOLS

def get_mobile_configs(configs):
    return [
        cfg for cfg in configs
        if any(
            cfg.startswith(proto)
            for proto in MOBILE_PROTOCOLS
        )
    ]