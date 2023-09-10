import logging
import urllib.parse
from datetime import datetime

from src.browser import Browser

from .activities import Activities


class DailySet:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.webdriver = browser.webdriver
        self.activities = Activities(browser)

    def completeDailySet(self):
        logging.info("[DAILY SET] " + "Trying to complete the Daily Set...")
        self.browser.utils.goHome()
        data = self.browser.utils.getDashboardData()["dailySetPromotions"]
        todayDate = datetime.now().strftime("%m/%d/%Y")
        for activity in data.get(todayDate, []):
            try:
                if activity["complete"] is False:
                    cardId = int(activity["offerId"][-1:])
                    self.activities.openDailySetActivity(cardId)
                    if activity["promotionType"] == "urlreward":
                        logging.info(
                            "[DAILY SET] " + f"Completing search of card {cardId}"
                        )
                        self.activities.completeSearch()
                    if activity["promotionType"] == "quiz":
                        if (
                            activity["pointProgressMax"] == 50
                            and activity["pointProgress"] == 0
                        ):
                            logging.info(
                                "[DAILY SET] "
                                + f"Completing This or That of card {cardId}"
                            )
                            self.activities.completeThisOrThat()
                        elif (
                            activity["pointProgressMax"] in [40, 30]
                            and activity["pointProgress"] == 0
                        ):
                            logging.info(
                                "[DAILY SET] " + f"Completing quiz of card {cardId}"
                            )
                            self.activities.completeQuiz()
                        elif (
                            activity["pointProgressMax"] == 10
                            and activity["pointProgress"] == 0
                        ):
                            searchUrl = urllib.parse.unquote(
                                urllib.parse.parse_qs(
                                    urllib.parse.urlparse(
                                        activity["destinationUrl"]
                                    ).query
                                )["ru"][0]
                            )
                            searchUrlQueries = urllib.parse.parse_qs(
                                urllib.parse.urlparse(searchUrl).query
                            )
                            filters = {}
                            for filterEl in searchUrlQueries["filters"][0].split(" "):
                                filterEl = filterEl.split(":", 1)
                                filters[filterEl[0]] = filterEl[1]
                            if "PollScenarioId" in filters:
                                logging.info(
                                    "[DAILY SET] " + f"Completing poll of card {cardId}"
                                )
                                self.activities.completeSurvey()
                            else:
                                logging.info(
                                    "[DAILY SET] " + f"Completing quiz of card {cardId}"
                                )
                                try:
                                    self.activities.completeABC()
                                except Exception:  # pylint: disable=broad-except
                                    self.activities.completeQuiz()
            except Exception:  # pylint: disable=broad-except
                self.browser.utils.resetTabs()
        logging.info("[DAILY SET] Completed the Daily Set successfully !")
