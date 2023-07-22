"""Module main.py
This module is the main module of the project.
"""
import argparse
import json
import os
import random
from pathlib import Path

import ipapi

from source.browser import browser_setup
from source.daily_set import DailySet
from source.login import Login
from source.more_promos import MorePromotions
from source.punch_cards import PunchCards
from source.searches import Searches
from source.utils import Utils

POINTS_COUNTER = 0


def get_c_code_lang() -> tuple[str, str]:
    """
    Returns the user's language and geolocation based on their IP address.

    Returns:
        tuple: A tuple containing the user's language (str) and geolocation (str).
    """
    try:
        nfo = ipapi.location()

        lang = nfo["languages"].split(",")[0].split("-")[0]  # type: ignore
        geo = nfo["country"]  # type: ignore
        return (lang, geo)
    except Exception:
        return ("en", "US")


def print_red(prt):
    """
    Prints the given string in red color in the console.

    Args:
        prt (str): The string to be printed in red color.
    """
    print(f"\033[91m{prt}\033[00m")


def print_green(prt):
    """
    Prints the given string in green color in the console.

    Args:
        prt (str): The string to be printed in green color.
    """
    print(f"\033[92m{prt}\033[00m")


def print_purple(prt):
    """
    Prints the given string in purple color in the console.

    Args:
        prt (str): The string to be printed in purple color.
    """
    print(f"\033[95m{prt}\033[00m")


def print_yellow(prt):
    """
    Prints the given string in yellow color in the console.

    Args:
        prt (str): The string to be printed in yellow color.
    """
    print(f"\033[93m{prt}\033[00m")


if __name__ == "__main__":
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
    args = parser.parse_args()

    print_red(
        """
    ███╗   ███╗███████╗    ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗██████╗
    ████╗ ████║██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗
    ██╔████╔██║███████╗    █████╗  ███████║██████╔╝██╔████╔██║█████╗  ██████╔╝
    ██║╚██╔╝██║╚════██║    ██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║██╔══╝  ██╔══██╗
    ██║ ╚═╝ ██║███████║    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
    ╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝"""
    )
    print_purple("        by Charles Bel (@charlesbel)               version 3.0\n")

    headless = not args.visible

    LANG = args.lang
    GEO = args.geo
    l, g = get_c_code_lang()
    if not LANG:
        LANG = l
    if not GEO:
        GEO = g

    account_path = Path(f"{os.path.dirname(os.path.abspath(__file__))}")
    accounts_file = account_path / "accounts.json"
    if not accounts_file.exists():
        accounts_file.write_text(
            json.dumps(
                [{"username": "Your Email", "password": "Your Password"}], indent=4
            )
        )
        print_purple(
            """
    [ACCOUNT] Accounts credential file "accounts.json" created.
    [ACCOUNT] Edit with your credentials and save, then press any key to continue...
        """
        )
        input()
    ACCOUNTS = json.loads(accounts_file.read_text(encoding="utf-8"))

    random.shuffle(ACCOUNTS)

    for account in ACCOUNTS:
        print_yellow(
            "********************" + account["username"] + "********************"
        )
        browser = browser_setup(account["username"], headless, False, LANG)
        utils = Utils(browser)

        print("[LOGIN]", "Logging-in...")
        POINTS_COUNTER = Login(browser).login(account["username"], account["password"])
        print_green("[LOGIN] Logged-in successfully !")
        startingPoints = POINTS_COUNTER
        print_green(f"[POINTS] You have {str(POINTS_COUNTER)} points on your account !")

        utils.go_home()

        print("[DAILY SET]", "Trying to complete the Daily Set...")
        DailySet(browser).complete_daily_set()
        print_green("[DAILY SET] Completed the Daily Set successfully !")
        print("[PUNCH CARDS]", "Trying to complete the Punch Cards...")
        PunchCards(browser).complete_punch_cards()
        print_green("[PUNCH CARDS] Completed the Punch Cards successfully !")
        print("[MORE PROMO]", "Trying to complete More Promotions...")
        MorePromotions(browser).complete_more_promotions()
        print_green("[MORE PROMO] Completed More Promotions successfully !")
        remainingSearches, remainingSearchesM = utils.get_remaining_searches()
        if remainingSearches != 0:
            print("[BING]", "Starting Desktop and Edge Bing searches...")
            POINTS_COUNTER = Searches(browser, LANG, GEO).bing_searches(
                remainingSearches
            )
            print_green("[BING] Finished Desktop and Edge Bing searches !")
        browser.quit()

        if remainingSearchesM != 0:
            browser = browser_setup(account["username"], headless, True, LANG)
            utils = Utils(browser)

            print("[LOGIN]", "Logging-in...")
            POINTS_COUNTER = Login(browser).login(
                account["username"], account["password"], True
            )
            print("[LOGIN]", "Logged-in successfully !")
            print("[BING]", "Starting Mobile Bing searches...")
            POINTS_COUNTER = Searches(browser, LANG, GEO).bing_searches(
                remainingSearchesM, True
            )
            print_green("[BING] Finished Mobile Bing searches !")
            browser.quit()

        print_green(
            f"[POINTS] You have earned {POINTS_COUNTER - startingPoints} points today !"
        )
        print_green(f"[POINTS] You are now at {POINTS_COUNTER} points !\n")
