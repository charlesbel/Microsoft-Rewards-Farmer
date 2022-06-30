# Microsoft Rewards Farmer
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1-blue.svg?style=flat)](#)


<pre align="center">
  __  __ _                           __ _     ____                            _     
 |  \/  (_) ___ _ __ ___  ___  ___  / _| |_  |  _ \ _____      ____ _ _ __ __| |___ 
 | |\/| | |/ __| '__/ _ \/ __|/ _ \| |_| __| | |_) / _ \ \ /\ / / _` | '__/ _` / __|
 | |  | | | (__| | | (_) \__ \ (_) |  _| |_  |  _ <  __/\ V  V / (_| | | | (_| \__ \
 |_|  |_|_|\___|_|  \___/|___/\___/|_|  \__| |_| \_\___| \_/\_/ \__,_|_|  \__,_|___/
                       |  ___|_ _ _ __ _ __ ___   ___ _ __                          
                       | |_ / _` | '__| '_ ` _ \ / _ \ '__|                         
                       |  _| (_| | |  | | | | | |  __/ |                            
                       |_|  \__,_|_|  |_| |_| |_|\___|_|                                
</pre>

A simple bot that uses selenium to farm Microsoft Rewards written in Python.

## Installation
* Install requirements with the following command :
 ```
 pip install -r requirements.txt
 ```
* Make sure you have Chrome installed.
* Edit the accounts.json.sample with your accounts credentials and rename it by removing .sample at the end
If you want to add more than one account, the syntax is the following :
```json
{
  "username": "Your Email",
  "password": "Your Password"
},
{
  "username": "Your Email",
  "password": "Your Password"
}
```
* Run the script
 
## Features
* Bing searches (Desktop, Mobile and Edge) with User-Agents
* Complete automatically the daily set
* Complete automatically punch cards
* Complete automatically the others promotions
* Headless Mode
* Multi-Account Management

## Credits
Credits to the original author of the repo : @charlesbel
