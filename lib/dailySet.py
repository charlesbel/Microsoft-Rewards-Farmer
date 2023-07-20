import time
from datetime import datetime
import random
import urllib.parse

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from .utils import Utils


class DailySet:
    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.utils = Utils(browser)

    def completeDailySetSearch(self, cardNumber: int):
        self.browser.find_element(
            By.XPATH, f'//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[{cardNumber}]/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
        self.utils.visitNewTab(random.randint(13, 17))

    def completeDailySetSurvey(self, cardNumber: int):
        self.browser.find_element(
            By.XPATH, f'//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[{cardNumber}]/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
        self.utils.switchToNewTab(8)
        self.browser.find_element(
            By.ID, f'btoption{random.randint(0, 1)}').click()
        time.sleep(random.randint(10, 15))
        self.utils.closeCurrentTab()

    def completeDailySetQuiz(self, cardNumber: int):
        self.browser.find_element(
            By.XPATH, f'//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[{cardNumber}]/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
        self.utils.switchToNewTab(8)
        if not self.utils.waitUntilQuizLoads():
            self.utils.resetTabs()
            return
        self.browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        self.utils.waitUntilVisible(By.XPATH,
                                    '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
        time.sleep(3)
        numberOfQuestions = self.browser.execute_script(
            "return _w.rewardsQuizRenderInfo.maxQuestions")
        numberOfOptions = self.browser.execute_script(
            "return _w.rewardsQuizRenderInfo.numberOfOptions")
        for _ in range(numberOfQuestions):
            if numberOfOptions == 8:
                answers = []
                for i in range(8):
                    if self.browser.find_element(By.ID, f'rqAnswerOption{i}').get_attribute("iscorrectoption").lower() == "true":
                        answers.append(f'rqAnswerOption{i}')
                for answer in answers:
                    self.browser.find_element(By.ID, answer).click()
                    time.sleep(5)
                    if not self.utils.waitUntilQuestionRefresh():
                        return
                time.sleep(5)
            elif numberOfOptions == 4:
                correctOption = self.browser.execute_script(
                    "return _w.rewardsQuizRenderInfo.correctAnswer")
                for i in range(4):
                    if self.browser.find_element(By.ID, f'rqAnswerOption{i}').get_attribute("data-option") == correctOption:
                        self.browser.find_element(
                            By.ID, f'rqAnswerOption{i}').click()
                        time.sleep(5)
                        if not self.utils.waitUntilQuestionRefresh():
                            return
                        break
                time.sleep(5)
        time.sleep(5)
        self.utils.closeCurrentTab()

    def completeDailySetVariableActivity(self, cardNumber: int):
        self.browser.find_element(
            By.XPATH, f'//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[{cardNumber}]/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
        self.utils.switchToNewTab(8)
        try:
            self.browser.find_element(
                By.XPATH, '//*[@id="rqStartQuiz"]').click()
            self.utils.waitUntilVisible(By.XPATH,
                                        '//*[@id="currentQuestionContainer"]/div/div[1]', 3)
        except (NoSuchElementException, TimeoutException):
            try:
                counter = str(self.browser.find_element(
                    By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
                numberOfQuestions = max([int(s)
                                        for s in counter.split() if s.isdigit()])
                for question in range(numberOfQuestions):
                    self.browser.execute_script(
                        f'document.evaluate("//*[@id=\'QuestionPane{question}\']/div[1]/div[2]/a[{random.randint(1, 3)}]/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                    time.sleep(5)
                    self.browser.find_element(
                        By.XPATH, f'//*[@id="AnswerPane{question}]/div[1]/div[2]/div[4]/a/div/span/input').click()
                    time.sleep(3)
                time.sleep(5)
                self.utils.closeCurrentTab()
                return
            except NoSuchElementException:
                time.sleep(random.randint(5, 9))
                self.utils.closeCurrentTab()
                return
        time.sleep(3)
        correctAnswer = self.browser.execute_script(
            "return _w.rewardsQuizRenderInfo.correctAnswer")
        if self.browser.find_element(By.ID, "rqAnswerOption0").get_attribute("data-option") == correctAnswer:
            self.browser.find_element(By.ID, "rqAnswerOption0").click()
        else:
            self.browser.find_element(By.ID, "rqAnswerOption1").click()
        time.sleep(10)
        self.utils.closeCurrentTab()

    def completeDailySetThisOrThat(self, cardNumber: int):
        self.browser.find_element(
            By.XPATH, f'//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[{cardNumber}]/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
        self.utils.switchToNewTab(8)
        if not self.utils.waitUntilQuizLoads():
            self.utils.resetTabs()
            return
        self.browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        self.utils.waitUntilVisible(By.XPATH,
                                    '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
        time.sleep(3)
        for _ in range(10):
            answerEncodeKey = self.browser.execute_script("return _G.IG")

            answer1 = self.browser.find_element(By.ID, "rqAnswerOption0")
            answer1Title = answer1.get_attribute('data-option')
            answer1Code = self.utils.getAnswerCode(
                answerEncodeKey, answer1Title)

            answer2 = self.browser.find_element(By.ID, "rqAnswerOption1")
            answer2Title = answer2.get_attribute('data-option')
            answer2Code = self.utils.getAnswerCode(
                answerEncodeKey, answer2Title)

            correctAnswerCode = self.browser.execute_script(
                "return _w.rewardsQuizRenderInfo.correctAnswer")

            if (answer1Code == correctAnswerCode):
                answer1.click()
                time.sleep(8)
            elif (answer2Code == correctAnswerCode):
                answer2.click()
                time.sleep(8)

        time.sleep(5)
        self.utils.closeCurrentTab()

    def completeDailySet(self):
        d = self.utils.getDashboardData()['dailySetPromotions']
        todayDate = datetime.today().strftime('%m/%d/%Y')
        todayPack = []
        for date, data in d.items():
            if date == todayDate:
                todayPack = data
        for activity in todayPack:
            try:
                if activity['complete'] == False:
                    cardNumber = int(activity['offerId'][-1:])
                    if activity['promotionType'] == "urlreward":
                        print('[DAILY SET]',
                              'Completing search of card ' + str(cardNumber))
                        self.completeDailySetSearch(cardNumber)
                    if activity['promotionType'] == "quiz":
                        if activity['pointProgressMax'] == 50 and activity['pointProgress'] == 0:
                            print(
                                '[DAILY SET]', 'Completing This or That of card ' + str(cardNumber))
                            self.completeDailySetThisOrThat(cardNumber)
                        elif (activity['pointProgressMax'] == 40 or activity['pointProgressMax'] == 30) and activity['pointProgress'] == 0:
                            print('[DAILY SET]',
                                  'Completing quiz of card ' + str(cardNumber))
                            self.completeDailySetQuiz(cardNumber)
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
                                    '[DAILY SET]', 'Completing poll of card ' + str(cardNumber))
                                self.completeDailySetSurvey(cardNumber)
                            else:
                                print(
                                    '[DAILY SET]', 'Completing quiz of card ' + str(cardNumber))
                                self.completeDailySetVariableActivity(
                                    self.browser, cardNumber)
            except:
                self.utils.resetTabs()
