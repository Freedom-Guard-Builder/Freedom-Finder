import subprocess
import re
import time
import requests

def test_ping_or_download(proxy_url: str, timeout=5) -> dict:
    result = {
        "proxy": proxy_url,
        "success": False,
        "ping": 9999,
        "country": "Unknown",
        "channel": "Unknown"
    }

    try:
        domain_match = re.search(r'(?:(?:@|//))([a-zA-Z0-9\.\-]+)', proxy_url)
        if not domain_match:
            return result
        host = domain_match.group(1)

        ping_res = subprocess.run(["ping", "-c", "1", "-W", str(timeout), host], capture_output=True, text=True)
        if ping_res.returncode == 0:
            result["ping"] = int(re.search(r'time=(\d+\.?\d*)', ping_res.stdout).group(1))
            result["success"] = True

        try:
            ip_info = requests.get(f"http://ip-api.com/json/{host}", timeout=3).json()
            if ip_info['status'] == 'success':
                result["country"] = ip_info["countryCode"]
        except:
            pass

    except Exception as e:
        print(f"[×] Error testing {proxy_url[:20]}... {e}")

    return result
