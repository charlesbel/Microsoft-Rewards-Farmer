""" This module contains the DailySet class. """
import urllib.parse
from datetime import datetime

from selenium.webdriver.chrome.webdriver import WebDriver

from .activities import Activities
from .utils import Utils


class DailySet:
    """Class for completing the daily set."""

    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.utils = Utils(browser)
        self.activities = Activities(browser)

    def complete_daily_set(self):
        """
        Completes the daily set by iterating through the daily set activities
        and completing them if they have not already been completed.
        """
        dashboard_data = self.utils.get_dashboard_data()["dailySetPromotions"]
        todays_date = datetime.now().strftime("%m/%d/%Y")
        todays_pack = dashboard_data.get(todays_date, [])
        for activity in todays_pack:
            try:
                if activity.get("complete"):
                    continue
                card_id = int(activity["offerId"][-1:])
                self.activities.open_daily_set_activity(card_id)
                promotion_type = activity["promotionType"]
                if promotion_type == "urlreward":
                    print("[DAILY SET]", f"Completing search of card {card_id}")
                    self.activities.complete_search()
                if promotion_type == "quiz":
                    point_progress_max = activity["pointProgressMax"]
                    point_progress = activity["pointProgress"]
                    if point_progress_max == 50 and point_progress == 0:
                        print(
                            "[DAILY SET]",
                            f"Completing This or That of card {card_id}",
                        )
                        self.activities.complete_this_or_that()
                    elif point_progress_max in [40, 30] and point_progress == 0:
                        print("[DAILY SET]", f"Completing quiz of card {card_id}")
                        self.activities.complete_quiz()
                    elif point_progress_max == 10 and point_progress == 0:
                        destination_url = activity["destinationUrl"]
                        search_url = urllib.parse.unquote(
                            urllib.parse.parse_qs(
                                urllib.parse.urlparse(destination_url).query
                            )["ru"][0]
                        )
                        search_url_queries = urllib.parse.parse_qs(
                            urllib.parse.urlparse(search_url).query
                        )
                        filters = dict(
                            filter_query.split(":", 1)
                            for filter_query in search_url_queries["filters"][0].split(
                                " "
                            )
                        )
                        if "PollScenarioId" in filters:
                            print("[DAILY SET]", f"Completing poll of card {card_id}")
                            self.activities.complete_survey()
                        else:
                            print("[DAILY SET]", f"Completing quiz of card {card_id}")
                            try:
                                self.activities.complete_abc()
                            except Exception:
                                self.activities.complete_quiz()
            except Exception:
                self.utils.reset_tabs()
