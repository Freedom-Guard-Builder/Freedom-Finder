# Freedom Finder Pro

Advanced modular proxy collector built with Python.

## Features

* Telegram channel scraper
* GitHub raw subscription parser
* Modular architecture
* Per-channel exports
* Protocol categorization
* Mobile config extraction
* Random mixed config generator
* GitHub Actions automation
* JSON + TXT exports
* Duplicate removal
* Async-ready structure
* Logging system

---

# Project Structure

```txt
project/
│
├── app/
│   ├── channels/
│   ├── core/
│   ├── scrapers/
│   ├── services/
│   └── settings.py
│
├── out/
├── protocols/
├── requirements.txt
├── main.py
└── README.md
```

---

# Installation

## Clone repository

```bash
git clone https://github.com/Freedom-Guard-Builder/freedom-finder.git
cd freedom-finder
```

---

## Create virtual environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\\Scripts\\activate
```

---

# Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run project

```bash
python main.py
```

---

# Outputs

After running:

```txt
out/
│
├── channels/
│   ├── Cook_Vpn.txt
│   ├── BegzarProxy.txt
│   └── ...
│
├── configs/
│   ├── all.txt
│   ├── mixed.txt
│   ├── mobile.txt
│   └── mobile.json
│
├── reports/
│   ├── categories.json
│   └── stats.json
│
└── app.log
```

---

# Add New Telegram Channel

Create file:

```txt
app/channels/new_channel.py
```

Example:

```python
CHANNEL_NAME = "Example"
CHANNEL_URL = "https://t.me/s/example"
```

Done.

The system auto-loads channels.

---

# Supported Protocols

* VMESS
* VLESS
* Trojan
* Shadowsocks
* SSR
* TUIC
* Hysteria
* Hysteria2
* Snell
* MTProto
* SOCKS5

---

# GitHub Actions

The project supports automatic daily updates.

Workflow path:

```txt
.github/workflows/daily.yml
```

Runs every day automatically.

---

# Requirements

* Python 3.11+
* Internet connection

---

# Recommended Improvements

* SQLite database
* FastAPI dashboard
* Async scraping
* Health checker
* Config scoring system
* Docker support
* Web panel

---

# Disclaimer

This project is for educational and research purposes only.
