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

1) Install requirements with the following command :

    `pip install -r requirements.txt`

2) Make sure you have Chrome installed

3) ~~Install ChromeDriver:~~

   You no longer need to do this step since selenium >=4.10.0 include a webdriver manager
   
   To update your selenium version, run this command : ```pip install selenium --upgrade```

5) Edit the `accounts.json.sample` with your accounts credentials and rename it by removing `.sample` at the end (ex. `accounts.json`)

   * If you want to add more than one account, the syntax is the following:

    ```json
        [
            {
                "username": "Your Email",
                "password": "Your Password"
            },
            {
                "username": "Your Email",
                "password": "Your Password"
            }
        ]
    ```

6) Run the script:

    `python main.py`

## Features

* Bing searches (Desktop, Mobile and Edge) with User-Agents
* Complete automatically the daily set
* Complete automatically punch cards
* Complete automatically the others promotions
* Headless Mode
* Multi-Account Management
* Session storing (3.0)
* 2FA Support (3.0)
* Send a Discord Webhook when done (-wh, -webhook)

## Future Features

* GUI
