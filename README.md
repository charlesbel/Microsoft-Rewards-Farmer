# Microsoft Rewards Farmer
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1-blue.svg?style=flat)](#)


<pre>
    _____  .__                                 _____  __   
  /     \ |__| ___________  ____  ___________/ ____\/  |_ 
 /  \ /  \|  |/ ___\_  __ \/  _ \/  ___/  _ \   __\\   __\
/    Y    \  \  \___|  | \(  <_> )___ (  <_> )  |   |  |  
\____|__  /__|\___  >__|   \____/____  >____/|__|   |__|  
        \/        \/                 \/                   
__________                                .___            
\______   \ ______  _  _______ _______  __| _/______      
 |       _// __ \ \/ \/ /\__  \\_  __ \/ __ |/  ___/      
 |    |   \  ___/\     /  / __ \|  | \/ /_/ |\___ \       
 |____|_  /\___  >\/\_/  (____  /__|  \____ /____  >      
        \/     \/             \/           \/    \/       
___________                                               
\_   _____/____ _______  _____   ___________              
 |    __) \__  \\_  __ \/     \_/ __ \_  __ \             
 |     \   / __ \|  | \/  Y Y  \  ___/|  | \/             
 \___  /  (____  /__|  |__|_|  /\___  >__|                
     \/        \/            \/     \/                    
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
