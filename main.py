from app.services.channel_service import load_channels
from app.scrapers.telegram import scrape_channel
from app.core.parser import extract_configs
from app.core.filters import unique_configs, is_valid_config
from app.core.exporter import export_txt, export_json
from app.core.categorizer import categorize
from app.core.mixer import mix_configs
from app.core.mobile import get_mobile_configs

def main():
    channels = load_channels()

    all_configs = []

    for channel in channels:
        print(f"[+] {channel['name']}")

        posts = scrape_channel(
            channel["url"]
        )

        configs = extract_configs(posts)

        configs = [
            c for c in configs
            if is_valid_config(c)
        ]

        configs = unique_configs(configs)

        export_txt(
            f"out/channels/{channel['name']}.txt",
            configs
        )

        all_configs.extend(configs)

    all_configs = unique_configs(all_configs)
    mixed_configs = mix_configs(
        all_configs,
        count=100
    )
    mobile_configs = get_mobile_configs(
        all_configs
    )

    categorized = categorize(all_configs)

    export_txt(
        "out/configs/all.txt",
        all_configs
    )

    export_json(
        "out/reports/categories.json",
        categorized
    )

    export_txt(
        "out/configs/mixed.txt",
        mixed_configs
    )
    export_json(
        "out/configs/mobile.json",
        {
            "MOBILE": mobile_configs
        }
    )

    print(f"[✓] Total: {len(all_configs)}")

if __name__ == "__main__":
    main()
