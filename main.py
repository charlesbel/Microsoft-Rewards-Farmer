import argparse
import csv
import json
import logging
import logging.handlers as handlers
import random
import sys
import time
from pathlib import Path
import pandas as pd
from datetime import datetime

from src import Browser, DailySet, Login, MorePromotions, PunchCards, Searches
from src.loggingColoredFormatter import ColoredFormatter
from src.notifier import Notifier
from src.utils import Utils

POINTS_COUNTER = 0

def main():
    print("test", Utils.randomSeconds(5, 10))
    args = argumentParser()
    notifier = Notifier(args)
    setupLogging(args.verbosenotifs, notifier)
    loadedAccounts = setupAccounts()

    # Load previous day's points data
    previous_points_data = load_previous_points_data()

    for currentAccount in loadedAccounts:
        try:
            earned_points = executeBot(currentAccount, notifier, args)
            account_name = currentAccount.get("username", "")
            previous_points = previous_points_data.get(account_name, 0)

            # Calculate the difference in points from the prior day
            points_difference = earned_points - previous_points

            # Append the daily points and points difference to CSV and Excel
            log_daily_points_to_csv(account_name, earned_points, points_difference)

            # Update the previous day's points data
            previous_points_data[account_name] = earned_points

            print(f"[POINTS] data for '{account_name}' appended to the file.")
        except Exception as e:
            logging.exception(f"{e.__class__.__name__}: {e}")

    # Save the current day's points data for the next day in the "logs" folder
    save_previous_points_data(previous_points_data)
    print("Points data saved for the next day.")

def log_daily_points_to_csv(date, earned_points, points_difference):
    logs_directory = Path(__file__).resolve().parent / "logs"
    csv_filename = logs_directory / "points_data.csv"

    # Create a new row with the date, daily points, and points difference
    date = datetime.now().strftime("%Y-%m-%d")
    new_row = {
        "Date": date,
        "Earned Points": earned_points,
        "Points Difference": points_difference,
    }

    fieldnames = ["Date", "Earned Points", "Points Difference"]
    is_new_file = not csv_filename.exists()

    with open(csv_filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if is_new_file:
            writer.writeheader()
        
        writer.writerow(new_row)

def setupLogging(verbose_notifs, notifier):
    ColoredFormatter.verbose_notifs = verbose_notifs
    ColoredFormatter.notifier = notifier

    format = "%(asctime)s [%(levelname)s] %(message)s"
    terminalHandler = logging.StreamHandler(sys.stdout)
    terminalHandler.setFormatter(ColoredFormatter(format))

    logs_directory = Path(__file__).resolve().parent / "logs"
    logs_directory.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format=format,
        handlers=[
            handlers.TimedRotatingFileHandler(
                logs_directory / "activity.log",
                when="midnight",
                interval=1,
                backupCount=2,
                encoding="utf-8",
            ),
            terminalHandler,
        ],
    )


def argumentParser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MS Rewards Farmer")
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
        "-p",
        "--proxy",
        type=str,
        default=None,
        help="Optional: Global Proxy (ex: http://user:pass@host:port)",
    )
    parser.add_argument(
        "-t",
        "--telegram",
        metavar=("TOKEN", "CHAT_ID"),
        nargs=2,
        type=str,
        default=None,
        help="Optional: Telegram Bot Token and Chat ID (ex: 123456789:ABCdefGhIjKlmNoPQRsTUVwxyZ 123456789)",
    )
    parser.add_argument(
        "-d",
        "--discord",
        type=str,
        default=None,
        help="Optional: Discord Webhook URL (ex: https://discord.com/api/webhooks/123456789/ABCdefGhIjKlmNoPQRsTUVwxyZ)",
    )
    parser.add_argument(
        "-vn",
        "--verbosenotifs",
        action="store_true",
        help="Optional: Send all the logs to discord/telegram",
    )
    return parser.parse_args()


def setupAccounts() -> list:
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
        logging.warning(noAccountsNotice)
        exit()
    loadedAccounts = json.loads(accountPath.read_text(encoding="utf-8"))
    random.shuffle(loadedAccounts)
    return loadedAccounts


def executeBot(currentAccount, notifier: Notifier, args: argparse.Namespace):
    logging.info(
        f'********************{ currentAccount.get("username", "") }********************'
    )
    with Browser(mobile=False, account=currentAccount, args=args) as desktopBrowser:
        accountPointsCounter = Login(desktopBrowser).login()
        startingPoints = accountPointsCounter
        logging.info(
            f"[POINTS] You have {desktopBrowser.utils.formatNumber(accountPointsCounter)} points on your account"
        )
        DailySet(desktopBrowser).completeDailySet()
        PunchCards(desktopBrowser).completePunchCards()
        MorePromotions(desktopBrowser).completeMorePromotions()
        (
            remainingSearches,
            remainingSearchesM,
        ) = desktopBrowser.utils.getRemainingSearches()

        # Introduce random pauses before and after searches
        pause_before_search = random.uniform(1.0, 5.0)  # Random pause between 1 to 5 seconds
        time.sleep(pause_before_search)

        if remainingSearches != 0:
            accountPointsCounter = Searches(desktopBrowser).bingSearches(
                remainingSearches
            )

        pause_after_search = random.uniform(1.0, 5.0)  # Random pause between 1 to 5 seconds
        time.sleep(pause_after_search)

        if remainingSearchesM != 0:
            desktopBrowser.closeBrowser()
            with Browser(
                mobile=True, account=currentAccount, args=args
            ) as mobileBrowser:
                accountPointsCounter = Login(mobileBrowser).login()
                accountPointsCounter = Searches(mobileBrowser).bingSearches(
                    remainingSearchesM
                )

        desktopBrowser.utils.goHome()
        goalPoints = desktopBrowser.utils.getGoalPoints()
        goalTitle = desktopBrowser.utils.getGoalTitle()
        desktopBrowser.closeBrowser()

        logging.info(
            f"[POINTS] You have earned {desktopBrowser.utils.formatNumber(accountPointsCounter - startingPoints)} points today !"
        )
        logging.info(
            f"[POINTS] You are now at {desktopBrowser.utils.formatNumber(accountPointsCounter)} points !"
        )
        goalNotifier = ""
        if goalPoints > 0:
            logging.info(
                f"[POINTS] You are now at {(desktopBrowser.utils.formatNumber((accountPointsCounter / goalPoints) * 100))}% of your goal ({goalTitle}) !\n"
            )
            goalNotifier = f"🎯 Goal reached: {(desktopBrowser.utils.formatNumber((accountPointsCounter / goalPoints) * 100))}% ({goalTitle})"

        notifier.send(
            "\n".join(
                [
                    "🏅 MS Rewards Farmer",
                    f"👤 Account: {currentAccount.get('username', '')}",
                    f"⭐️ Points earned today: {desktopBrowser.utils.formatNumber(accountPointsCounter - startingPoints)}",
                    f"💰 Total points: {desktopBrowser.utils.formatNumber(accountPointsCounter)}",
                    goalNotifier,
                ]
            )
        )

        return accountPointsCounter


def export_points_to_csv(points_data):
    logs_directory = Path(__file__).resolve().parent / "logs"
    csv_filename = logs_directory / "points_data.csv"
    with open(csv_filename, mode="a", newline="") as file:  # Use "a" mode for append
        fieldnames = ["Account", "Earned Points", "Points Difference"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Check if the file is empty, and if so, write the header row
        if file.tell() == 0:
            writer.writeheader()

        for data in points_data:
            writer.writerow(data)


# Define a function to load the previous day's points data from a file in the "logs" folder
def load_previous_points_data():
    logs_directory = Path(__file__).resolve().parent / "logs"
    try:
        with open(logs_directory / "previous_points_data.json", "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {}


# Define a function to save the current day's points data for the next day in the "logs" folder
def save_previous_points_data(data):
    logs_directory = Path(__file__).resolve().parent / "logs"
    with open(logs_directory / "previous_points_data.json", "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    main()