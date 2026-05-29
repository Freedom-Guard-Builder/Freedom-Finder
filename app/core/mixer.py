import random

def mix_configs(configs, count=100):
    if not configs:
        return []

    if len(configs) <= count:
        return configs

    return random.sample(configs, count)