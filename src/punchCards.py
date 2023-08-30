import contextlib
import logging
import random
import time
import urllib.parse

from selenium.webdriver.common.by import By

from src.browser import Browser

from .constants import BASE_URL


class PunchCards:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.webdriver = browser.webdriver

    def completePunchCard(self, url: str, childPromotions: dict):
        self.webdriver.get(url)
        for child in childPromotions:
            if child["complete"] is False:
                if child["promotionType"] == "urlreward":
                    self.webdriver.find_element(By.CLASS_NAME, "offer-cta").click()
                    self.browser.utils.visitNewTab(random.randint(13, 17))
                if child["promotionType"] == "quiz":
                    self.webdriver.find_element(By.CLASS_NAME, "offer-cta").click()
                    self.browser.utils.switchToNewTab(8)
                    counter = str(
                        self.webdriver.find_element(
                            By.XPATH, '//*[@id="QuestionPane0"]/div[2]'
                        ).get_attribute("innerHTML")
                    )[:-1][1:]
                    numberOfQuestions = max(
                        int(s) for s in counter.split() if s.isdigit()
                    )
                    for question in range(numberOfQuestions):
                        self.webdriver.find_element(
                            By.XPATH,
                            f'//*[@id="QuestionPane{question}"]/div[1]/div[2]/a[{random.randint(1, 3)}]/div',
                        ).click()
                        time.sleep(random.randint(100, 700) / 100))
                        self.webdriver.find_element(
                            By.XPATH,
                            f'//*[@id="AnswerPane{question}"]/div[1]/div[2]/div[4]/a/div/span/input',
                        ).click()
                        time.sleep(random.randint(100, 700) / 100))
                    time.sleep(random.randint(100, 700) / 100))
                    self.browser.utils.closeCurrentTab()

    def completePunchCards(self):
        logging.info("[PUNCH CARDS] " + "Trying to complete the Punch Cards...")
        self.completePromotionalItems()
        punchCards = self.browser.utils.getDashboardData()["punchCards"]
        for punchCard in punchCards:
            try:
                if (
                    punchCard["parentPromotion"]
                    and punchCard["childPromotions"]
                    and not punchCard["parentPromotion"]["complete"]
                    and punchCard["parentPromotion"]["pointProgressMax"] != 0
                ):
                    self.completePunchCard(
                        punchCard["parentPromotion"]["attributes"]["destination"],
                        punchCard["childPromotions"],
                    )
            except Exception:  # pylint: disable=broad-except
                self.browser.utils.resetTabs()
        logging.info("[PUNCH CARDS] Completed the Punch Cards successfully !")
        time.sleep(random.randint(100, 700) / 100))
        self.webdriver.get(BASE_URL)
        time.sleep(random.randint(100, 700) / 100))

    def completePromotionalItems(self):
        with contextlib.suppress(Exception):
            item = self.browser.utils.getDashboardData()["promotionalItem"]
            destUrl = urllib.parse.urlparse(item["destinationUrl"])
            baseUrl = urllib.parse.urlparse(BASE_URL)
            if (
                (item["pointProgressMax"] in [100, 200, 500])
                and not item["complete"]
                and (
                    (
                        destUrl.hostname == baseUrl.hostname
                        and destUrl.path == baseUrl.path
                    )
                    or destUrl.hostname == "www.bing.com"
                )
            ):
                self.webdriver.find_element(
                    By.XPATH, '//*[@id="promo-item"]/section/div/div/div/span'
                ).click()
                self.browser.utils.visitNewTab(8)
