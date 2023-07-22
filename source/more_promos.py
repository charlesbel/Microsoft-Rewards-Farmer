""" This module contains the MorePromotions class, which is used to complete
the More Promotions section of the Microsoft Rewards dashboard."""
from selenium.webdriver.chrome.webdriver import WebDriver

from .activities import Activities
from .utils import Utils


class MorePromotions:
    """A class representing the 'More Promotions' section of the Microsoft Rewards dashboard.
    This class provides methods for completing various types of promotions,
    such as quizzes and searches.
    """

    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.utils = Utils(browser)
        self.activities = Activities(browser)

    def complete_more_promotions(self):
        """Completes more promotions by iterating through the list of available
        promotions and completing them based on their type and progress."""
        more_promotions = self.utils.get_dashboard_data()["morePromotions"]
        i = 0
        for promotion in more_promotions:
            try:
                i += 1
                if not promotion["complete"] and promotion["pointProgressMax"] != 0:
                    self.activities.open_more_promotions_activity(i)
                    if promotion["promotionType"] == "urlreward":
                        self.activities.complete_search()
                    elif (
                        promotion["promotionType"] == "quiz"
                        and promotion["pointProgress"] == 0
                    ):
                        if promotion["pointProgressMax"] == 10:
                            self.activities.complete_abc()
                        elif promotion["pointProgressMax"] in [30, 40]:
                            self.activities.complete_quiz()
                        elif promotion["pointProgressMax"] == 50:
                            self.activities.complete_this_or_that()
                    else:
                        self.activities.complete_search()
            except Exception:
                self.utils.reset_tabs()
