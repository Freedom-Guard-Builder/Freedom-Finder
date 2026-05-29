from app.settings import PROTOCOLS

def is_valid_config(config):
    return any(
        config.startswith(proto)
        for proto in PROTOCOLS
    )

def unique_configs(configs):
    seen = set()
    result = []

    for config in configs:
        normalized = config.strip().lower()

        if normalized in seen:
            continue

        seen.add(normalized)
        result.append(config)

    return result
