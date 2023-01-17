<pre align="center">
███╗   ███╗███████╗    ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗██████╗ 
████╗ ████║██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗
██╔████╔██║███████╗    █████╗  ███████║██████╔╝██╔████╔██║█████╗  ██████╔╝
██║╚██╔╝██║╚════██║    ██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║██╔══╝  ██╔══██╗
██║ ╚═╝ ██║███████║    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
       by Charles Bel (@charlesbel)          version 2.0
</pre>
**How to Install:**
-Install zip from GitHub: https://github.com/charlesbel/Microsoft-Rewards-Farmer

-Install Python https://www.python.org/downloads/
	Select custom installation, change nothing hit yes until installed. 

-Open Microsoft-Rewards-Farmer-master, move requirements.txt to C:\Users\Alex

-Open command prompt. win + R>CMD, then type (without quotes): 'pip install -r requirements.txt' 	Press enter

-Install Google Chrome.

-Install ChromeDriver from https://chromedriver.chromium.org/downloads
	Place the file in X:\Windows (X as your Windows disk letter)

-Edit the accounts.json.sample with your accounts credentials and rename it by removing .sample at the end of the file name
-If you want to add more than one account, the syntax is the following:
```
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

-How to Disable Headless mode to watch the script work. Comment out around line 32 and 33
#if headless_mode : #comment out to disable headless mode (makes window visable)
#options.add_argument("--headless")


-How to run Script:
Run the script by double clicking on ms_rewards_farmer.py

