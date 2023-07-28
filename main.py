import argparse
import json
import random
from pathlib import Path

from src import Browser, DailySet, Login, MorePromotions, PunchCards, Searches
from src.constants import VERSION
from src.utils import format_number, prGreen, prPurple, prRed, prYellow

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
    random.shuffle(loadedAccounts)
    return loadedAccounts


def executeBot(loadedAccounts):
    for currentAccount in loadedAccounts:
        prYellow(
            "********************{ "
            + currentAccount.get("username", "")
            + " }********************"
        )
        with Browser(
            mobile=False, account=currentAccount, args=argumentParser()
        ) as browser:
            accountPointsCounter = Login(browser).login()
            startingPoints = accountPointsCounter
            prGreen(
                f"[POINTS] You have {format_number(accountPointsCounter)} points on your account !"
            )
            DailySet(browser).completeDailySet()
            PunchCards(browser).completePunchCards()
            MorePromotions(browser).completeMorePromotions()
            remainingSearches, remainingSearchesM = browser.utils.getRemainingSearches()
            if remainingSearches != 0:
                accountPointsCounter = Searches(browser).bingSearches(remainingSearches)

        if remainingSearchesM != 0:
            with Browser(
                mobile=True, account=currentAccount, args=argumentParser()
            ) as browser:
                accountPointsCounter = Login(browser).login()
                accountPointsCounter = Searches(browser).bingSearches(
                    remainingSearchesM
                )

        prGreen(
            f"[POINTS] You have earned {format_number(accountPointsCounter - startingPoints)} points today !"
        )
        prGreen(
            f"[POINTS] You are now at {format_number(accountPointsCounter)} points !\n"
        )


if __name__ == "__main__":
    main()
