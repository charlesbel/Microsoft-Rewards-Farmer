import time
import random

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from .utils import Utils

class MorePromotions:
    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.utils = Utils(browser)

    def completeMorePromotionSearch(self, cardNumber: int):
        self.browser.find_element(
            By.XPATH, f'//*[@id="more-activities"]/div/mee-card[{cardNumber}]/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
        self.utils.visitNewTab(random.randint(13, 17))


    def completeMorePromotionQuiz(self, cardNumber: int):
        self.browser.find_element(
            By.XPATH, f'//*[@id="more-activities"]/div/mee-card[{cardNumber}]/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
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


    def completeMorePromotionABC(self, cardNumber: int):
        self.browser.find_element(
            By.XPATH, f'//*[@id="more-activities"]/div/mee-card[{cardNumber}]/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
        self.utils.switchToNewTab(8)
        counter = str(self.browser.find_element(
            By.XPATH, '//*[@id="QuestionPane0"]/div[1]').get_attribute('innerHTML'))[:-1][1:]
        numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
        for question in range(numberOfQuestions):
            self.browser.execute_script(
                f'document.evaluate("//*[@id=\'QuestionPane{question}\']/div[1]/div[2]/a[{random.randint(1, 3)}]/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
            time.sleep(5)
            self.browser.find_element(
                By.XPATH, f'//*[@id="AnswerPane{question}"]/div[1]/div[2]/div[4]/a/div/span/input').click()
            time.sleep(3)
        time.sleep(5)
        self.utils.closeCurrentTab()


    def completeMorePromotionThisOrThat(self, cardNumber: int):
        self.browser.find_element(
            By.XPATH, f'//*[@id="more-activities"]/div/mee-card[{cardNumber}]/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
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
            answer1Code = self.utils.getAnswerCode(answerEncodeKey, answer1Title)

            answer2 = self.browser.find_element(By.ID, "rqAnswerOption1")
            answer2Title = answer2.get_attribute('data-option')
            answer2Code = self.utils.getAnswerCode(answerEncodeKey, answer2Title)

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


    def completeMorePromotions(self):
        morePromotions = self.utils.getDashboardData()['morePromotions']
        i = 0
        for promotion in morePromotions:
            try:
                i += 1
                if promotion['complete'] == False and promotion['pointProgressMax'] != 0:
                    if promotion['promotionType'] == "urlreward":
                        self.completeMorePromotionSearch(i)
                    elif promotion['promotionType'] == "quiz" and promotion['pointProgress'] == 0:
                        if promotion['pointProgressMax'] == 10:
                            self.completeMorePromotionABC(i)
                        elif promotion['pointProgressMax'] == 30 or promotion['pointProgressMax'] == 40:
                            self.completeMorePromotionQuiz(i)
                        elif promotion['pointProgressMax'] == 50:
                            self.completeMorePromotionThisOrThat(i)
                    else:
                        if promotion['pointProgressMax'] == 100 or promotion['pointProgressMax'] == 200:
                            self.completeMorePromotionSearch(i)
            except:
                self.utils.resetTabs()
