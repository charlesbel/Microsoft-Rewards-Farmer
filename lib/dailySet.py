import time
from datetime import datetime
import random
import urllib.parse

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from .utils import Utils
from .activities import Activities


class DailySet:
    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.utils = Utils(browser)
        self.activities = Activities(browser)

    def completeDailySet(self):
        data = self.utils.getDashboardData()['dailySetPromotions']
        todayDate = datetime.today().strftime('%m/%d/%Y')

        if todayDate in data:  # Check if today's date is a key in the data dictionary
            for activity in data[todayDate]:
                try:
                    if activity['complete'] == False:
                        cardId = int(activity['offerId'][-1:])
                        self.activities.openDailySetActivity(cardId)
                        if activity['promotionType'] == "urlreward":
                            print('[DAILY SET]',
                                'Completing search of card ' + str(cardId))
                            self.activities.completeSearch()
                        if activity['promotionType'] == "quiz":
                            if activity['pointProgressMax'] == 50 and activity['pointProgress'] == 0:
                                print(
                                    '[DAILY SET]', 'Completing This or That of card ' + str(cardId))
                                self.activities.completeThisOrThat()
                            elif (activity['pointProgressMax'] == 40 or activity['pointProgressMax'] == 30) and activity['pointProgress'] == 0:
                                print('[DAILY SET]',
                                        'Completing quiz of card ' + str(cardId))
                                self.activities.completeQuiz()
                            elif activity['pointProgressMax'] == 10 and activity['pointProgress'] == 0:
                                searchUrl = urllib.parse.unquote(urllib.parse.parse_qs(
                                    urllib.parse.urlparse(activity['destinationUrl']).query)['ru'][0])
                                searchUrlQueries = urllib.parse.parse_qs(
                                    urllib.parse.urlparse(searchUrl).query)
                                filters = {}
                                for filter in searchUrlQueries['filters'][0].split(" "):
                                    filter = filter.split(':', 1)
                                    filters[filter[0]] = filter[1]
                                if "PollScenarioId" in filters:
                                    print(
                                        '[DAILY SET]', 'Completing poll of card ' + str(cardId))
                                    self.activities.completeSurvey()
                                else:
                                    print(
                                        '[DAILY SET]', 'Completing quiz of card ' + str(cardId))
                                    try:
                                        self.activities.completeABC()
                                    except:
                                        self.activities.completeQuiz()
                except:
                    self.utils.resetTabs()
        else:  # If today's date is not a key in the data dictionary, print a message
            print(f"No activities found for today's date: {todayDate}")
