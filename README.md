[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://github.com/charlesbel/Microsoft-Rewards-Farmer/)
[![ForTheBadge built-by-developers](http://ForTheBadge.com/images/badges/built-by-developers.svg)](https://github.com/charlesbel/Microsoft-Rewards-Farmer/)
[![ForTheBadge uses-git](http://ForTheBadge.com/images/badges/uses-git.svg)](https://GitHub.com/)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://github.com/charlesbel/Microsoft-Rewards-Farmer/)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/charlesbel/Microsoft-Rewards-Farmer/graphs/commit-activity)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://lbesson.mit-license.org/)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/charlesbel/Microsoft-Rewards-Farmer.svg)](http://isitmaintained.com/project/charlesbel/Shopify-Checkout-Bypasser "Average time to resolve an issue")
[![Percentage of issues still open](http://isitmaintained.com/badge/open/charlesbel/Microsoft-Rewards-Farmer.svg)](http://isitmaintained.com/project/charlesbel/Shopify-Checkout-Bypasser "Percentage of issues still open")

# Microsoft Rewards Farmer
A simple bot that uses selenium to farm Microsoft Rewards written in Python.

# Features
- Bing searches (Desktop, Mobile and Edge) with User-Agents
- Complete automatically the daily set
- Complete automatically punch cards
- Complete automatically the others promotions
- Headless Mode
- Multi-Account Management

# Installation
* Install requirements with the following command : `pip install -r requirements.txt`
* Make sure you have Chrome installed
* Windows :
  - Download Chrome WebDriver : https://chromedriver.chromium.org/downloads
  - Place the file in X:\Windows (X as your Windows disk letter)
* MacOS or Linux :
  - `brew cask install chromedriver`
* Rename the `ms_accounts.json.sample` to `ms_accounts.json` and update with your account information.
* Run the script

# Docker Installation
> Note: At this time there is no public repository where this project is. However you can build it yourself!

* Put the files on the docker server
* Run the following commands from within your files folder to build the image:
  * `docker build -t yournamehere/msrewardfarmer`
* Run one of the following commands below to start the container
  * `docker run --name msrewardfarmer -d yournamehere/msrewardfarmer`

You can add some environment variables as well for further control over things like scheduling (early stages).

Example: `docker run --name msrewardfarmer --env MRF_AUTO_RUN_DAILY=True -d yournamehere/msrewardfarmer`

| Environment Var Name | Expected Type | Default Value | Description                                                                                                                                                        |
|----------------------|---------------|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| MRF_DOCKER           | Boolean       | True          | Leave this to true. Its a simple variable to let the script know its in a Docker container                                                                         |
| MRF_AUTO_RUN_DAILY   | Boolean       | False         | Tells the script to setup a schedule for running once a day or not (True = Schedule; False = Run Once). Otherwise the docker container will exit with Exit Code 0. |
| MRF_AUTO_RUN_HOUR    | Boolean       | 12            | Tells the script on which hour to run. For example: 14 would run at 14:00 every day. This number should be between 00-23 depending on when you want it to run.     |


