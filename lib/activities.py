import time
from datetime import datetime
import random
import urllib.parse

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from .utils import Utils


class Activities:

    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.utils = Utils(browser)

    def openDailySetActivity(self, cardId: int):
        self.browser.find_element(
            By.XPATH, f'//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[{cardId}]/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
        self.utils.switchToNewTab(8)

    def openMorePromotionsActivity(self, cardId: int):
        self.browser.find_element(
            By.XPATH, f'//*[@id="more-activities"]/div/mee-card[{cardId}]/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
        self.utils.switchToNewTab(8)

    def completeSearch(self):
        time.sleep(random.randint(5, 10))
        self.utils.closeCurrentTab()

    def completeSurvey(self):
        self.browser.find_element(
            By.ID, f'btoption{random.randint(0, 1)}').click()
        time.sleep(random.randint(10, 15))
        self.utils.closeCurrentTab()

    def completeABC(self):
        counter = self.browser.find_element(
            By.XPATH, '//*[@id="QuestionPane0"]/div[2]').text[:-1][1:]
        numberOfQuestions = max([int(s)
                                for s in counter.split() if s.isdigit()])
        for question in range(numberOfQuestions):
            self.browser.find_element(
                By.ID, f'questionOptionChoice{question}{random.randint(0, 2)}').click()
            time.sleep(5)
            self.browser.find_element(
                By.ID, f'nextQuestionbtn{question}').click()
            time.sleep(3)
        time.sleep(5)
        self.utils.closeCurrentTab()

    def completeQuiz(self):
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
        for question in range(numberOfQuestions):
            if numberOfOptions == 8:
                answers = []
                for i in range(numberOfOptions):
                    if self.browser.find_element(By.ID, f'rqAnswerOption{i}').get_attribute("iscorrectoption").lower() == "true":
                        answers.append(f'rqAnswerOption{i}')
                for answer in answers:
                    self.browser.find_element(By.ID, answer).click()
                    time.sleep(5)
                    if not self.utils.waitUntilQuestionRefresh():
                        self.utils.resetTabs()
                        return
            elif numberOfOptions in [2, 4]:
                correctOption = self.browser.execute_script(
                    "return _w.rewardsQuizRenderInfo.correctAnswer")
                for i in range(numberOfOptions):
                    if self.browser.find_element(By.ID, f'rqAnswerOption{i}').get_attribute("data-option") == correctOption:
                        self.browser.find_element(
                            By.ID, f'rqAnswerOption{i}').click()
                        time.sleep(5)
                        if not self.utils.waitUntilQuestionRefresh():
                            self.utils.resetTabs()
                            return
                        break
            if question + 1 != numberOfQuestions:
                time.sleep(5)
        time.sleep(5)
        self.utils.closeCurrentTab()

    def completeThisOrThat(self):
        numberOfQuestions = 10
        if not self.utils.waitUntilQuizLoads():
            self.utils.resetTabs()
            return
        self.browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        self.utils.waitUntilVisible(By.XPATH,
                                    '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
        time.sleep(3)
        for question in range(numberOfQuestions):
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
            elif (answer2Code == correctAnswerCode):
                answer2.click()

            if question + 1 != numberOfQuestions:
                time.sleep(8)

        time.sleep(5)
        self.utils.closeCurrentTab()
