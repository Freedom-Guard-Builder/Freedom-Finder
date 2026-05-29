from pathlib import Path
import importlib

def load_channels():
    channels = []

    source_dir = Path("app/sources")

    for file in source_dir.rglob("*.py"):

        if file.stem.startswith("__"):
            continue

        relative = file.relative_to(source_dir)

        module_path = (
            "app.sources."
            + str(relative.with_suffix(""))
            .replace("\\", ".")
            .replace("/", ".")
        )

        try:
            module = importlib.import_module(
                module_path
            )

            channels.append({
                "name": module.CHANNEL_NAME,
                "url": module.CHANNEL_URL
            })

        except Exception as e:
            print(
                f"[ERROR] {module_path} -> {e}"
            )

    return channels