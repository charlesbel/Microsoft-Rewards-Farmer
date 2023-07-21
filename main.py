import json
import random
import ipapi
import os
import argparse

from lib import *


POINTS_COUNTER = 0


def getCCodeLang() -> tuple:
    try:
        nfo = ipapi.location()
        lang = nfo['languages'].split(',')[0].split('-')[0]
        geo = nfo['country']
        return (lang, geo)
    except:
        return ('en', 'US')


def prRed(prt):
    print("\033[91m{}\033[00m".format(prt))


def prGreen(prt):
    print("\033[92m{}\033[00m".format(prt))


def prPurple(prt):
    print("\033[95m{}\033[00m".format(prt))


def prYellow(prt):
    print("\033[93m{}\033[00m".format(prt))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Microsoft Rewards Farmer')
    parser.add_argument('-v', '--visible', action='store_true',
                        help='Optional: Visible browser')
    parser.add_argument('-l', '--lang', type=str, default=None,
                        help='Optional: Language (ex: en)')
    parser.add_argument('-g', '--geo', type=str, default=None,
                        help='Optional: Geolocation (ex: US)')
    args = parser.parse_args()

    prRed("""
    ███╗   ███╗███████╗    ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗██████╗
    ████╗ ████║██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗
    ██╔████╔██║███████╗    █████╗  ███████║██████╔╝██╔████╔██║█████╗  ██████╔╝
    ██║╚██╔╝██║╚════██║    ██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║██╔══╝  ██╔══██╗
    ██║ ╚═╝ ██║███████║    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
    ╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝""")
    prPurple("        by Charles Bel (@charlesbel)               version 3.0\n")

    headless = not args.visible

    LANG = args.lang
    GEO = args.geo
    if not LANG or not GEO :
        l, g = getCCodeLang()
        if not LANG:
            LANG = l
        if not GEO:
            GEO = g

    try:
        account_path = os.path.dirname(
            os.path.abspath(__file__)) + '/accounts.json'
        ACCOUNTS = json.load(open(account_path, "r"))
    except FileNotFoundError:
        with open(account_path, 'w') as f:
            f.write(json.dumps([{
                "username": "Your Email",
                "password": "Your Password"
            }], indent=4))
        prPurple("""
    [ACCOUNT] Accounts credential file "accounts.json" created.
    [ACCOUNT] Edit with your credentials and save, then press any key to continue...
        """)
        input()
        ACCOUNTS = json.load(open(account_path, "r"))

    random.shuffle(ACCOUNTS)

    for account in ACCOUNTS:

        prYellow('********************' +
                 account['username'] + '********************')
        browser = browserSetup(account['username'], headless, False, LANG)
        utils = Utils(browser)

        print('[LOGIN]', 'Logging-in...')
        POINTS_COUNTER = Login(browser).login(
            account['username'], account['password'])
        prGreen('[LOGIN] Logged-in successfully !')
        startingPoints = POINTS_COUNTER
        prGreen('[POINTS] You have ' + str(POINTS_COUNTER) +
                ' points on your account !')

        utils.goHome()

        print('[DAILY SET]', 'Trying to complete the Daily Set...')
        DailySet(browser).completeDailySet()
        prGreen('[DAILY SET] Completed the Daily Set successfully !')
        print('[PUNCH CARDS]', 'Trying to complete the Punch Cards...')
        PunchCards(browser).completePunchCards()
        prGreen('[PUNCH CARDS] Completed the Punch Cards successfully !')
        print('[MORE PROMO]', 'Trying to complete More Promotions...')
        MorePromotions(browser).completeMorePromotions()
        prGreen('[MORE PROMO] Completed More Promotions successfully !')
        remainingSearches, remainingSearchesM = utils.getRemainingSearches()
        if remainingSearches != 0:
            print('[BING]', 'Starting Desktop and Edge Bing searches...')
            POINTS_COUNTER = Searches(
                browser, LANG, GEO).bingSearches(remainingSearches)
            prGreen('[BING] Finished Desktop and Edge Bing searches !')
        browser.quit()

        if remainingSearchesM != 0:
            browser = browserSetup(account['username'], headless, True, LANG)
            utils = Utils(browser)

            print('[LOGIN]', 'Logging-in...')
            POINTS_COUNTER = Login(browser).login(
                account['username'], account['password'], True)
            print('[LOGIN]', 'Logged-in successfully !')
            print('[BING]', 'Starting Mobile Bing searches...')
            POINTS_COUNTER = Searches(browser, LANG, GEO).bingSearches(
                remainingSearchesM, True)
            prGreen('[BING] Finished Mobile Bing searches !')
            browser.quit()

        prGreen(f'[POINTS] You have earned {POINTS_COUNTER - startingPoints} points today !')
        prGreen(f'[POINTS] You are now at {POINTS_COUNTER} points !\n')
