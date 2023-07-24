import time
import random
import urllib.parse

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from .constants import BASE_URL
from .utils import Utils
from .activities import Activities

class PunchCards:
    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.utils = Utils(browser)
        self.activities = Activities(browser)

    def completePunchCard(self, url: str, childPromotions: dict):
        self.browser.get(url)
        for child in childPromotions:
            if child['complete'] == False:
                self.browser.find_element(By.CLASS_NAME, 'offer-cta').click()
                if child['promotionType'] == "urlreward":
                    self.utils.visitNewTab(random.randint(13, 17))
                elif child['promotionType'] == "quiz":
                    self.utils.switchToNewTab(8)
                    self.activities.completeABC()
                else:
                    self.utils.visitNewTab(random.randint(13, 17))

    def completePunchCards(self):
        self.completePromotionalItems()
        punchCards = self.utils.getDashboardData()['punchCards']
        for punchCard in punchCards:
            try:
                if punchCard['parentPromotion'] and punchCard['childPromotions'] and not punchCard['parentPromotion']['complete'] and punchCard['parentPromotion']['pointProgressMax'] != 0:
                    self.completePunchCard(
                        punchCard['parentPromotion']['attributes']['destination'], punchCard['childPromotions'])
            except:
                self.utils.resetTabs()
        time.sleep(2)
        self.utils.goHome()
        time.sleep(2)

    def completePromotionalItems(self):
        try:
            item = self.utils.getDashboardData()["promotionalItem"]
            destUrl = urllib.parse.urlparse(item["destinationUrl"])
            baseUrl = urllib.parse.urlparse(BASE_URL)
            if (item["pointProgressMax"] in [100, 200, 500]) and not item["complete"] and ((destUrl.hostname == baseUrl.hostname and destUrl.path == baseUrl.path) or destUrl.hostname == "www.bing.com"):
                self.browser.find_element(
                    By.XPATH, '//*[@id="promo-item"]/section/div/div/div/span').click()
                self.utils.visitNewTab(8)
        except:
            pass
