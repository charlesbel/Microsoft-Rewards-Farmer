import time
import random

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from .constants import BASE_URL
from .utils import Utils


class PunchCards:
    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.utils = Utils(browser)

    def completePunchCard(self, url: str, childPromotions: dict):
        self.browser.get(url)
        for child in childPromotions:
            if child['complete'] == False:
                if child['promotionType'] == "urlreward":
                    self.browser.execute_script(
                        "document.getElementsByClassName('offer-cta')[0].click()")
                    self.utils.visitNewTab(random.randint(13, 17))
                if child['promotionType'] == "quiz":
                    self.browser.execute_script(
                        "document.getElementsByClassName('offer-cta')[0].click()")
                    self.utils.switchToNewTab(8)
                    counter = str(self.browser.find_element(
                        By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
                    numberOfQuestions = max(
                        [int(s) for s in counter.split() if s.isdigit()])
                    for question in range(numberOfQuestions):
                        self.browser.execute_script(
                            f'document.evaluate("//*[@id=\'QuestionPane{question}]/div[1]/div[2]/a[{random.randint(1, 3)}]/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                        time.sleep(5)
                        self.browser.find_element(
                            By.XPATH, f'//*[@id="AnswerPane{question}"]/div[1]/div[2]/div[4]/a/div/span/input').click()
                        time.sleep(3)
                    time.sleep(5)
                    self.utils.closeCurrentTab()

    def completePunchCards(self):
        self.completePromotionalItems()
        punchCards = self.utils.getDashboardData()['punchCards']
        for punchCard in punchCards:
            try:
                if punchCard['parentPromotion'] != None and punchCard['childPromotions'] != None and punchCard['parentPromotion']['complete'] == False and punchCard['parentPromotion']['pointProgressMax'] != 0:
                    self.completePunchCard(
                        punchCard['parentPromotion']['attributes']['destination'], punchCard['childPromotions'])
            except:
                self.utils.resetTabs()
        time.sleep(2)
        self.browser.get(BASE_URL)
        time.sleep(2)

    def completePromotionalItems(self):
        try:
            item = self.utils.getDashboardData()["promotionalItem"]
            if (item["pointProgressMax"] in [100, 200, 500]) and item["complete"] == False and (item["destinationUrl"] == BASE_URL or item["destinationUrl"].startswith("https://www.bing.com/")):
                self.browser.find_element(
                    By.XPATH, '//*[@id="promo-item"]/section/div/div/div/span').click()
                self.utils.visitNewTab(8)
        except:
            pass
