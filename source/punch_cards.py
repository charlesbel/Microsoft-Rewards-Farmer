""" This module contains the PunchCards class. """

import contextlib
import random
import time
import urllib.parse

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from .constants import BASE_URL
from .utils import Utils


class PunchCards:
    """
    This class represents the punch cards feature of the Microsoft Rewards program.
    It provides methods to complete punch cards and promotional items.
    """

    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.utils = Utils(browser)

    def complete_punch_card(self, url: str, child_promotions: dict):
        """
        Completes a punch card by visiting the specified URL and completing its child promotions.

        Args:
            url (str): The URL of the punch card to complete.
            child_promotions (dict): A dictionary containing information about
            the child promotions of the punch card.

        Returns:
            None
        """
        self.browser.get(url)
        for child in child_promotions:
            if not child["complete"]:
                if child["promotionType"] == "urlreward":
                    self.browser.execute_script(
                        "document.getElementsByClassName('offer-cta')[0].click()"
                    )
                    self.utils.visit_new_tab(random.randint(13, 17))
                if child["promotionType"] == "quiz":
                    self.browser.execute_script(
                        "document.getElementsByClassName('offer-cta')[0].click()"
                    )
                    self.utils.switch_to_new_tab(8)
                    counter = str(
                        self.browser.find_element(
                            By.XPATH, '//*[@id="QuestionPane0"]/div[2]'
                        ).get_attribute("innerHTML")
                    )[:-1][1:]
                    number_of_questions = max(
                        int(s) for s in counter.split() if s.isdigit()
                    )
                    for question in range(number_of_questions):
                        self.browser.execute_script(
                            f"document.evaluate(\"//*[@id='QuestionPane{question}]/div[1]/div[2]/a"
                            f'[{random.randint(1, 3)}]/div", document, null, '
                            "XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()"
                        )
                        time.sleep(5)
                        self.browser.find_element(
                            By.XPATH,
                            f'//*[@id="AnswerPane{question}"]'
                            "/div[1]/div[2]/div[4]/a/div/span/input",
                        ).click()
                        time.sleep(3)
                    time.sleep(5)
                    self.utils.close_current_tab()

    def complete_punch_cards(self):
        """
        This method completes all punch cards items available on the dashboard.
        """
        self.complete_promotional_items()
        punch_cards = self.utils.get_dashboard_data()["punchCards"]
        for punch_card in punch_cards:
            try:
                if (
                    punch_card["parentPromotion"]
                    and punch_card["childPromotions"]
                    and not punch_card["parentPromotion"]["complete"]
                    and punch_card["parentPromotion"]["pointProgressMax"] != 0
                ):
                    self.complete_punch_card(
                        punch_card["parentPromotion"]["attributes"]["destination"],
                        punch_card["childPromotions"],
                    )
            except Exception:
                self.utils.reset_tabs()
        time.sleep(2)
        self.utils.go_home()
        time.sleep(2)

    def complete_promotional_items(self):
        """
        This method completes all promotional items available on the dashboard.
        """
        with contextlib.suppress(Exception):
            item = self.utils.get_dashboard_data()["promotionalItem"]
            dest_url = urllib.parse.urlparse(item["destinationUrl"])
            base_url = urllib.parse.urlparse(BASE_URL)
            if (
                (item["pointProgressMax"] in [100, 200, 500])
                and not item["complete"]
                and (
                    (
                        dest_url.hostname == base_url.hostname
                        and dest_url.path == base_url.path
                    )
                    or dest_url.hostname == "www.bing.com"
                )
            ):
                self.browser.find_element(
                    By.XPATH, '//*[@id="promo-item"]/section/div/div/div/span'
                ).click()
                self.utils.visit_new_tab(8)
