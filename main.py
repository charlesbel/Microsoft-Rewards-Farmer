import argparse
import json
import logging
import logging.handlers as handlers
import random
import sys
from pathlib import Path

from src import Browser, DailySet, Login, MorePromotions, PunchCards, Searches
from src.constants import VERSION
from src.loggingColoredFormatter import ColoredFormatter
from src.notifier import Notifier

POINTS_COUNTER = 0


def main():
    if sys.version_info[0] == 3:
        if sys.version_info[1] >= 12:
            raise Exception(
                "Not supported, see https://peps.python.org/pep-0632/#:~:text=In%20Python%203.12%2C%20distutils"
                "%20will%20no%20longer%20be%20installed%20by%20make%20install%20or%20any%20of%20the%20first%2Dparty"
                "%20distribution.%20Third%2Dparty%20redistributors%20should%20no%20longer%20include%20distutils%20in"
                "%20their%20bundles%20or%20repositories."
            )
    setupLogging()
    args = argumentParser()
    notifier = Notifier(args)
    loadedAccounts = setupAccounts()
    for currentAccount in loadedAccounts:
        try:
            executeBot(currentAccount, notifier, args)
        except Exception as e:
            logging.exception(f"{e.__class__.__name__}: {e}")


def setupLogging():
    format = "%(asctime)s [%(levelname)s] %(message)s"
    terminalHandler = logging.StreamHandler(sys.stdout)
    terminalHandler.setFormatter(ColoredFormatter(format))

    (Path(__file__).resolve().parent / "logs").mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format=format,
        handlers=[
            handlers.TimedRotatingFileHandler(
                "logs/activity.log",
                when="midnight",
                interval=1,
                backupCount=2,
                encoding="utf-8",
            ),
            terminalHandler,
        ],
    )


def argumentParser() -> argparse.Namespace:
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
        "-p",
        "--proxy",
        type=str,
        default=None,
        help="Optional: Global Proxy (ex: http://user:pass@host:port)",
    )
    # noinspection SpellCheckingInspection
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
    return parser.parse_args()


def bannerDisplay():
    farmerBanner = """
    ███╗   ███╗███████╗    ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗██████╗
    ████╗ ████║██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗
    ██╔████╔██║███████╗    █████╗  ███████║██████╔╝██╔████╔██║█████╗  ██████╔╝
    ██║╚██╔╝██║╚════██║    ██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║██╔══╝  ██╔══██╗
    ██║ ╚═╝ ██║███████║    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
    ╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝"""
    logging.error(farmerBanner)
    logging.warning(
        f"        by Charles Bel (@charlesbel)               version {VERSION}\n"
    )


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
        logging.warning(noAccountsNotice)
        exit()
    loadedAccounts = json.loads(accountPath.read_text(encoding="utf-8"))
    random.shuffle(loadedAccounts)
    return loadedAccounts


def executeBot(currentAccount, notifier: Notifier, args: argparse.Namespace):
    logging.info(
        f'********************{currentAccount.get("username", "")}********************'
    )
    accountsPointsCounter: int
    remainingSearchesMobile: int
    startingPoints: int
    accountPointsCounter: int
    remainingSearchesMobile: int
    with Browser(mobile=False, account=currentAccount, args=args) as desktopBrowser:
        accountPointsCounter = Login(desktopBrowser).login()
        startingPoints = accountPointsCounter
        logging.info(
            f"[POINTS] You have {desktopBrowser.utils.formatNumber(accountPointsCounter)} points on your account !"
        )
        DailySet(desktopBrowser).completeDailySet()
        PunchCards(desktopBrowser).completePunchCards()
        MorePromotions(desktopBrowser).completeMorePromotions()
        (
            remainingSearches,
            remainingSearchesMobile,
        ) = desktopBrowser.utils.getRemainingSearches()
        if remainingSearches != 0:
            accountPointsCounter = Searches(desktopBrowser).bingSearches(
                remainingSearches
            )

    if remainingSearchesMobile != 0:
        with Browser(mobile=True, account=currentAccount, args=args) as mobileBrowser:
            Login(mobileBrowser).login()
            accountPointsCounter = Searches(mobileBrowser).bingSearches(
                remainingSearchesMobile
            )

    logging.info(
        f"[POINTS] You have earned {desktopBrowser.utils.formatNumber(accountPointsCounter - startingPoints)} points today !"
    )
    logging.info(
        f"[POINTS] You are now at {desktopBrowser.utils.formatNumber(accountPointsCounter)} points !\n"
    )

    notifier.send(
        "\n".join(
            [
                "Microsoft Rewards Farmer",
                f"Account: {currentAccount.get('username', '')}",
                f"Points earned today: {desktopBrowser.utils.formatNumber(accountPointsCounter - startingPoints)}",
                f"Total points: {desktopBrowser.utils.formatNumber(accountPointsCounter)}",
            ]
        )
    )


if __name__ == "__main__":
    main()
