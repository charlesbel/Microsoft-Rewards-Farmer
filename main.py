import argparse
import json
import random
from pathlib import Path

from src import (Browser, DailySet, Discord, Login, MorePromotions, PunchCards,
                 Searches)
from src.constants import VERSION
from src.utils import prGreen, prPurple, prRed, prYellow

POINTS_COUNTER = 0


def main():
    loadedAccounts = setupAccounts()
    executeBot(loadedAccounts)


def argumentParser():
    parser = argparse.ArgumentParser(description="Microsoft Rewards Farmer")
    parser.add_argument(
        "-v", "--visible", action="store_true", help="Optional: Visible browser"
    )
    parser.add_argument(
        "-l", "--lang", type=str, default=None, help="Optional: Language (ex: en)"
    )
    parser.add_argument(
        "-g", "--geo", type=str, default=None, help="Optional: Geolocation (ex: US)"
    )
    parser.add_argument(
        "-wh", "--webhook", action="store_true", help="Optional: send a discord webhook message with the summary"
    )
    parser.add_argument(
        "-s", "--shuffle", action="store_true", help="Optional: shuffle the order in which accounts will be farmed on"
    )
    return parser.parse_args()


def bannerDisplay():
    farmerBanner = """
    ███╗   ███╗███████╗    ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗██████╗
    ████╗ ████║██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗
    ██╔████╔██║███████╗    █████╗  ███████║██████╔╝██╔████╔██║█████╗  ██████╔╝
    ██║╚██╔╝██║╚════██║    ██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║██╔══╝  ██╔══██╗
    ██║ ╚═╝ ██║███████║    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
    ╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝"""
    prRed(farmerBanner)
    prPurple(f"        by Charles Bel (@charlesbel)               version {VERSION}\n")


def setupAccounts() -> dict:
    accountPath = Path(__file__).resolve().parent / "accounts.json"
    if not accountPath.exists():
        accountPath.write_text(
            json.dumps(
                [{"username": "Your Email", "password": "Your Password"}], indent=4
            ),
            encoding="utf-8",
        )
        noAccountsNotice = """
    [ACCOUNT] Accounts credential file "accounts.json" not found.
    [ACCOUNT] A new file has been created, please edit with your credentials and save.
    """
        prPurple(noAccountsNotice)
        exit()
    loadedAccounts = json.loads(accountPath.read_text(encoding="utf-8"))

    args = argumentParser()

    if args.shuffle:  
        random.shuffle(loadedAccounts)

    return loadedAccounts


def executeBot(loadedAccounts):
    Discord.check_json()
    
    for currentAccount in loadedAccounts:
        prYellow(
            "********************{ "
            + currentAccount.get("username", "")
            + " }********************"
        )
        with Browser(
            mobile=False, account=currentAccount, args=argumentParser()
        ) as desktopBrowser:
            accountPointsCounter = Login(desktopBrowser).login()
            startingPoints = accountPointsCounter
            prGreen(
                f"[POINTS] You have {desktopBrowser.utils.formatNumber(accountPointsCounter)} points on your account !"
            )
            DailySet(desktopBrowser).completeDailySet()
            PunchCards(desktopBrowser).completePunchCards()
            MorePromotions(desktopBrowser).completeMorePromotions()
            (
                remainingSearches,
                remainingSearchesM,
            ) = desktopBrowser.utils.getRemainingSearches()
            if remainingSearches != 0:
                accountPointsCounter = Searches(desktopBrowser).bingSearches(
                    remainingSearches
                )

            if remainingSearchesM != 0:
                desktopBrowser.closeBrowser()
                with Browser(
                    mobile=True, account=currentAccount, args=argumentParser()
                ) as mobileBrowser:
                    accountPointsCounter = Login(mobileBrowser).login()
                    accountPointsCounter = Searches(mobileBrowser).bingSearches(
                        remainingSearchesM
                    )

            prGreen(
                f"[POINTS] You have earned {desktopBrowser.utils.formatNumber(accountPointsCounter - startingPoints)} points today !"
            )
            prGreen(
                f"[POINTS] You are now at {desktopBrowser.utils.formatNumber(accountPointsCounter)} points !\n"
            )
            
            args = argumentParser()
            
            if args.webhook:
                Discord.send_to_webhook(f'`{currentAccount.get("username", "")}` has farmed {accountPointsCounter - startingPoints} points today. Total points: {accountPointsCounter}')


if __name__ == "__main__":
    main()
