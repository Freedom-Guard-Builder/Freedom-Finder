import requests

def fetch_raw_configs(url):
    try:
        response = requests.get(
            url,
            timeout=15
        )

        response.raise_for_status()

        return response.text.splitlines()

    except:
        return []