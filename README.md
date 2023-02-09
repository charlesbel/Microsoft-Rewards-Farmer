<pre align="center">
███╗   ███╗███████╗    ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗██████╗ 
████╗ ████║██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗
██╔████╔██║███████╗    █████╗  ███████║██████╔╝██╔████╔██║█████╗  ██████╔╝
██║╚██╔╝██║╚════██║    ██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║██╔══╝  ██╔══██╗
██║ ╚═╝ ██║███████║    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
         Created by  Charles Bel (@charlesbel)    Updated by Alex V (@Alexy_Galaxy)   version 3.0
</pre>
- **Use at your own risk, Microsoft may ban your account (and I would not be responsible for it)** -
-How to avoid getting banned
```
**Do not use more than one phone number per 5 accounts. **
**Do not Redeem more than one reward per day**
```
**How to Install:**

-Install zip from GitHub: https://github.com/AlexyGalaxy/Microsoft-Rewards-Farmer

-Install Python https://www.python.org/downloads/
	Select custom installation, change nothing hit yes until installed. 

```
-Open Microsoft-Rewards-Farmer-master, move requirements.txt to C:\Users\YOURNAMEHERE

-Open command prompt. win + R>CMD
type (without quotes and with a space after): 'cd ' 
drag the folder that contains requirements.txt into cmd
hit enter
type (without quotes): 'pip install -r requirements.txt'
Press enter

-Install Google Chrome.
```
-Windows
```
-Install ChromeDriver from https://chromedriver.chromium.org/downloads
	Place the file in X:\Windows (X as your Windows disk letter)
```
-MacOS or Linux :
```
apt install chromium-chromedriver
```
-or if you have brew :
```
brew cask install chromedriver
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

-How to run Script:

	Double click on ms_rewards_farmer.py

-How to make Script automatically close:

Comment out the second to last line of code
(If you do this you will not know if there was any errors)
```
#input()
```
