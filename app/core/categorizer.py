def categorize(configs):
    result = {
        "mci": [],
        "irancell": [],
        "rightel": [],
        "public": [],
        "other": []
    }

    for cfg in configs:
        lower = cfg.lower()

        if "mci" in lower:
            result["mci"].append(cfg)

        elif "irancell" in lower:
            result["irancell"].append(cfg)

        elif "rightel" in lower:
            result["rightel"].append(cfg)

        else:
            result["other"].append(cfg)

    return result
