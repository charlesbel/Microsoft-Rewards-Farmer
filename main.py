import json
import random
import ipapi
import os

from lib.browser import browserSetup

from lib.utils import Utils
from lib.login import Login
from lib.searches import Searches
from lib.dailySet import DailySet
from lib.morePromotions import MorePromotions
from lib.punchCards import PunchCards


POINTS_COUNTER = 0


def getCCodeLang() -> tuple:
    try:
        nfo = ipapi.location()
        lang = nfo['languages'].split(',')[0]
        geo = nfo['country']
        return (lang, geo)
    except:
        return ('fr-FR', 'FR')


def prRed(prt):
    print("\033[91m{}\033[00m".format(prt))


def prGreen(prt):
    print("\033[92m{}\033[00m".format(prt))


def prPurple(prt):
    print("\033[95m{}\033[00m".format(prt))


def prYellow(prt):
    print("\033[93m{}\033[00m".format(prt))


prRed("""
███╗   ███╗███████╗    ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗██████╗
████╗ ████║██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗
██╔████╔██║███████╗    █████╗  ███████║██████╔╝██╔████╔██║█████╗  ██████╔╝
██║╚██╔╝██║╚════██║    ██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║██╔══╝  ██╔══██╗
██║ ╚═╝ ██║███████║    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝""")
prPurple("        by Charles Bel (@charlesbel)               version 2.0\n")

LANG, GEO = getCCodeLang()

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
    browser = browserSetup(account['username'], False, False, LANG)

    utils = Utils(browser)
    login = Login(browser)
    searches = Searches(browser)
    dailySet = DailySet(browser)
    morePromotions = MorePromotions(browser)
    punchCards = PunchCards(browser)

    print('[LOGIN]', 'Logging-in...')
    POINTS_COUNTER = login.login(account['username'], account['password'])
    prGreen('[LOGIN] Logged-in successfully !')
    startingPoints = POINTS_COUNTER
    prGreen('[POINTS] You have ' + str(POINTS_COUNTER) +
            ' points on your account !')

    utils.goHome()

    print('[DAILY SET]', 'Trying to complete the Daily Set...')
    dailySet.completeDailySet()
    prGreen('[DAILY SET] Completed the Daily Set successfully !')
    print('[PUNCH CARDS]', 'Trying to complete the Punch Cards...')
    punchCards.completePunchCards()
    prGreen('[PUNCH CARDS] Completed the Punch Cards successfully !')
    print('[MORE PROMO]', 'Trying to complete More Promotions...')
    morePromotions.completeMorePromotions()
    prGreen('[MORE PROMO] Completed More Promotions successfully !')
    remainingSearches, remainingSearchesM = utils.getRemainingSearches()
    if remainingSearches != 0:
        print('[BING]', 'Starting Desktop and Edge Bing searches...')
        POINTS_COUNTER = searches.bingSearches(remainingSearches)
        prGreen('[BING] Finished Desktop and Edge Bing searches !')
    browser.quit()

    if remainingSearchesM != 0:
        browser = browserSetup(account['username'], False, True, LANG)

        utils = Utils(browser)
        login = Login(browser)
        searches = Searches(browser)
        dailySet = DailySet(browser)
        morePromotions = MorePromotions(browser)
        punchCards = PunchCards(browser)

        print('[LOGIN]', 'Logging-in...')
        POINTS_COUNTER = login.login(account['username'], account['password'], True)
        print('[LOGIN]', 'Logged-in successfully !')
        print('[BING]', 'Starting Mobile Bing searches...')
        POINTS_COUNTER = searches.bingSearches(remainingSearchesM, True)
        prGreen('[BING] Finished Mobile Bing searches !')
        browser.quit()

    prGreen('[POINTS] You have earned ' +
            str(POINTS_COUNTER - startingPoints) + ' points today !')
    prGreen('[POINTS] You are now at ' + str(POINTS_COUNTER) + ' points !\n')
