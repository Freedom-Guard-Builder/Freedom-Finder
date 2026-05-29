from pathlib import Path
import importlib

def load_channels():
    channels = []

    channel_dir = Path("app/channels")

    for file in channel_dir.glob("*.py"):
        if file.stem.startswith("__"):
            continue

        module = importlib.import_module(
            f"app.channels.{file.stem}"
        )

        channels.append({
            "name": module.CHANNEL_NAME,
            "url": module.CHANNEL_URL
        })

    return channels
