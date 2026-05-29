from pathlib import Path

from app.services.channel_service import load_channels
from app.scrapers.telegram import scrape_channel
from app.scrapers.raw import fetch_raw_configs

from app.core.parser import extract_configs
from app.core.filters import (
    unique_configs,
    is_valid_config
)

from app.core.exporter import (
    export_txt,
    export_json
)

from app.core.categorizer import categorize
from app.core.mixer import mix_configs
from app.core.mobile import get_mobile_configs


def main():

    Path("out").mkdir(exist_ok=True)

    Path(
        "out/configs"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    Path(
        "out/channels"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    Path(
        "out/reports"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    channels = load_channels()

    all_configs = []

    for channel in channels:

        print(
            f"[+] {channel['name']}"
        )

        try:

            if "t.me" in channel["url"]:

                posts = scrape_channel(
                    channel["url"]
                )

                configs = extract_configs(
                    posts
                )

            else:

                configs = fetch_raw_configs(
                    channel["url"]
                )

            configs = [
                c for c in configs
                if is_valid_config(c)
            ]

            configs = unique_configs(
                configs
            )

            export_txt(
                f"out/channels/{channel['name']}.txt",
                configs
            )

            all_configs.extend(
                configs
            )

            print(
                f"[✓] {channel['name']} -> {len(configs)}"
            )

        except Exception as e:

            print(
                f"[ERROR] {channel['name']} -> {e}"
            )

    all_configs = unique_configs(
        all_configs
    )

    mixed_configs = mix_configs(
        all_configs,
        count=100
    )

    mobile_configs = get_mobile_configs(
        all_configs
    )

    categorized = categorize(
        all_configs
    )

    export_txt(
        "out/configs/all.txt",
        all_configs
    )

    export_txt(
        "out/configs/mixed.txt",
        mixed_configs
    )

    export_txt(
        "out/configs/mobile.txt",
        mobile_configs
    )

    export_json(
        "out/configs/mobile.json",
        {
            "count": len(
                mobile_configs
            ),
            "MOBILE": mobile_configs
        }
    )

    export_json(
        "out/reports/categories.json",
        categorized
    )

    export_json(
        "out/reports/stats.json",
        {
            "total": len(all_configs),
            "mobile": len(mobile_configs),
            "mixed": len(mixed_configs)
        }
    )

    print(
        f"[✓] Total configs: {len(all_configs)}"
    )


if __name__ == "__main__":
    main()