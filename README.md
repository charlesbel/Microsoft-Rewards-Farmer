# Microsoft Rewards Bot
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.1-blue.svg?style=flat)](#)

An automated solution for earning daily Microsoft Rewards points using Python and Selenium.

## Installation

### Using config file
* Clone the repo
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
### Using command-line
* Run the the script with the following arguments :
 ```
python MicrosoftRewardsBot -h -a user:pass user2:pass2
 ```
 Where `-h` is for headless-mode and `user:pass` is for `Your Email:Your Password`.
### Using Github Actions
* Fork the repo
* Add `ACCOUNTS` secret, [More info](https://github.com/Azure/actions-workflow-samples/blob/master/assets/create-secrets-for-GitHub-workflows.md)
* Run `Deploy` workflow
 
## Features
* Bing searches (Desktop, Mobile and Edge) with User-Agents
* Complete automatically the daily set
* Complete automatically punch cards
* Complete automatically the others promotions
* Headless Mode
* Multi-Account Management
* Command-line options
* Github Actions

## Credits
Credits to the original author of the repo : [charlesbel](https://github.com/charlesbel)
