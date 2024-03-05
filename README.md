![Made with Python](https://forthebadge.com/images/badges/made-with-python.svg)
![Built by Developers](http://ForTheBadge.com/images/badges/built-by-developers.svg)
![Uses Git](http://ForTheBadge.com/images/badges/uses-git.svg)
![Build with Love](http://ForTheBadge.com/images/badges/built-with-love.svg)

```ascii
███╗   ███╗███████╗    ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗██████╗
████╗ ████║██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗
██╔████╔██║███████╗    █████╗  ███████║██████╔╝██╔████╔██║█████╗  ██████╔╝
██║╚██╔╝██║╚════██║    ██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║██╔══╝  ██╔══██╗
██║ ╚═╝ ██║███████║    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
       by Charles Bel (@charlesbel)          version 3.0
```

![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)
![MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)

## :wave: Welcome to the future of automation

### A simple bot that uses selenium to farm Microsoft Rewards written in Python

```diff
- Use it at your own risk, Microsoft may ban your account (and I would not be responsible for it)
```

## Installation

1. Install requirements with the following command :

   `pip install -r requirements.txt`

2. Make sure you have Chrome installed

3. (Windows Only) Make sure Visual C++ redistributable DLLs are installed

   If they're not, install the current "vc_redist.exe" from this link and reboot your
   computer : https://learn.microsoft.com/en-GB/cpp/windows/latest-supported-vc-redist?view=msvc-170

4. Edit the `accounts.json.sample` with your accounts credentials and rename it by removing `.sample` at the end. The "
   proxy" field is not mandatory, you can omit it if you don't want to use proxy (don't keep it as an empty string,
   remove it completely).

    - If you want to add more than one account, the syntax is the following:

   ```json
   [
     {
       "username": "Your Email 1",
       "password": "Your Password 1",
       "proxy": "http://user:pass@host1:port"
     },
     {
       "username": "Your Email 2",
       "password": "Your Password 2",
       "proxy": "http://user:pass@host2:port"
     }
   ]
   ```

5. Run the script:

   `python main.py`

   Or if you want to keep it updated (it will check on each run if a new version is available, if so, will download and
   run it), use :

   `python autoupdate_main.py`

## Launch arguments

- -v/--visible to disable headless
- -l/--lang to force a language (ex: en)
- -g/--geo to force a geolocation (ex: US)
- -p/--proxy to add a proxy to the whole program, supports http/https/socks4/socks5 (overrides per-account proxy in
  accounts.json) (ex: http://user:pass@host:port)
- -t/--telegram to add a telegram notification, requires Telegram Bot Token and Chat ID (ex: 123456789:
  ABCdefGhIjKlmNoPQRsTUVwxyZ 123456789)
- -d/--discord to add a discord notification, requires Discord Webhook URL (
  ex: https://discord.com/api/webhooks/123456789/ABCdefGhIjKlmNoPQRsTUVwxyZ)

## Features

- Bing searches (Desktop, Mobile and Edge) with User-Agents
- Complete automatically the daily set
- Complete automatically punch cards
- Complete automatically the others promotions
- Headless Mode
- Multi-Account Management
- Session storing (3.0)
- 2FA Support (3.0)
- Notifications (discord, telegram) (3.0)
- Proxy Support (3.0)

## Future Features

- GUI
