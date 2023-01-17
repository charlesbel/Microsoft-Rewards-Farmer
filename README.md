<pre align="center">
███╗   ███╗███████╗    ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗██████╗ 
████╗ ████║██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗
██╔████╔██║███████╗    █████╗  ███████║██████╔╝██╔████╔██║█████╗  ██████╔╝
██║╚██╔╝██║╚════██║    ██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║██╔══╝  ██╔══██╗
██║ ╚═╝ ██║███████║    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
         Created by  Charles Bel (@charlesbel)    Updated by Alex V (@Alexy_Galaxy)   version 3.0
</pre>
**How to Install:**
```
-Install zip from GitHub: https://github.com/charlesbel/Microsoft-Rewards-Farmer

-Install Python https://www.python.org/downloads/
	Select custom installation, change nothing hit yes until installed. 

-Open Microsoft-Rewards-Farmer-master, move requirements.txt to C:\Users\Alex

-Open command prompt. win + R>CMD
type (without quotes): 'pip install -r requirements.txt'
Press enter

-Install Google Chrome.

-Install ChromeDriver from https://chromedriver.chromium.org/downloads
	Place the file in X:\Windows (X as your Windows disk letter)
```
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

-How to enable Rewards logger to create a txt file when you have more than 6500 points for a $5 gift card.
```
On line 30 remove the # infront of rewardsFile and change YourNameHere to your pc's Username
To find your pc's user's name go to C:\Users
```

-How to Disable Headless mode to watch the script work:

Comment out line 41 and 42 by placing a # in front of each line.
```
#if headless_mode : #comment out to disable headless mode (makes window visable)
#options.add_argument("--headless")
```

-How to run Script:'

	Double click on ms_rewards_farmer.py

