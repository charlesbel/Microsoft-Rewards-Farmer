import urllib.parse
from datetime import datetime

from selenium.webdriver.chrome.webdriver import WebDriver

from .activities import Activities
from .utils import Utils


class DailySet:
    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.utils = Utils(browser)
        self.activities = Activities(browser)

    def completeDailySet(self):
        data = self.utils.getDashboardData()["dailySetPromotions"]
        todayDate = datetime.today().strftime("%m/%d/%Y")
        for activity in data.get(todayDate, []):
            try:
                if activity["complete"] is False:
                    cardId = int(activity["offerId"][-1:])
                    self.activities.openDailySetActivity(cardId)
                    if activity["promotionType"] == "urlreward":
                        print("[DAILY SET]", "Completing search of card " + str(cardId))
                        self.activities.completeSearch()
                    if activity["promotionType"] == "quiz":
                        if (
                            activity["pointProgressMax"] == 50
                            and activity["pointProgress"] == 0
                        ):
                            print(
                                "[DAILY SET]",
                                "Completing This or That of card " + str(cardId),
                            )
                            self.activities.completeThisOrThat()
                        elif (
                            activity["pointProgressMax"] == 40
                            or activity["pointProgressMax"] == 30
                        ) and activity["pointProgress"] == 0:
                            print(
                                "[DAILY SET]", "Completing quiz of card " + str(cardId)
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
                                print(
                                    "[DAILY SET]",
                                    "Completing poll of card " + str(cardId),
                                )
                                self.activities.completeSurvey()
                            else:
                                print(
                                    "[DAILY SET]",
                                    "Completing quiz of card " + str(cardId),
                                )
                                try:
                                    self.activities.completeABC()
                                except Exception:  # pylint: disable=broad-except
                                    self.activities.completeQuiz()
            except Exception:  # pylint: disable=broad-except
                self.utils.resetTabs()
