import random
import time

from selenium.webdriver.common.by import By

from src.browser import Browser


class Activities:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.webdriver = browser.webdriver

    def openDailySetActivity(self, cardId: int):
        self.webdriver.find_element(
            By.XPATH,
            f'//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[{cardId}]/div/card-content/mee-rewards-daily-set-item-content/div/a',
        ).click()
        self.browser.utils.switchToNewTab(8)

    def openMorePromotionsActivity(self, cardId: int):
        self.webdriver.find_element(
            By.XPATH,
            f'//*[@id="more-activities"]/div/mee-card[{cardId}]/div/card-content/mee-rewards-more-activities-card-item/div/a',
        ).click()
        self.browser.utils.switchToNewTab(8)

    def completeSearch(self):
        time.sleep(random.randint(5, 10))
        self.browser.utils.closeCurrentTab()

    def completeSurvey(self):
        self.webdriver.find_element(By.ID, f"btoption{random.randint(0, 1)}").click()
        time.sleep(random.randint(10, 15))
        self.browser.utils.closeCurrentTab()

    def completeQuiz(self):
        if not self.browser.utils.waitUntilQuizLoads():
            self.browser.utils.resetTabs()
            return
        self.webdriver.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        self.browser.utils.waitUntilVisible(
            By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 5
        )
        time.sleep(3)
        numberOfQuestions = self.webdriver.execute_script(
            "return _w.rewardsQuizRenderInfo.maxQuestions"
        )
        numberOfOptions = self.webdriver.execute_script(
            "return _w.rewardsQuizRenderInfo.numberOfOptions"
        )
        for question in range(numberOfQuestions):
            if numberOfOptions == 8:
                answers = []
                for i in range(numberOfOptions):
                    isCorrectOption = self.webdriver.find_element(
                        By.ID, f"rqAnswerOption{i}"
                    ).get_attribute("iscorrectoption")
                    if isCorrectOption and isCorrectOption.lower() == "true":
                        answers.append(f"rqAnswerOption{i}")
                for answer in answers:
                    self.webdriver.find_element(By.ID, answer).click()
                    time.sleep(5)
                    if not self.browser.utils.waitUntilQuestionRefresh():
                        self.browser.utils.resetTabs()
                        return
            elif numberOfOptions in [2, 3, 4]:
                correctOption = self.webdriver.execute_script(
                    "return _w.rewardsQuizRenderInfo.correctAnswer"
                )
                for i in range(numberOfOptions):
                    if (
                        self.webdriver.find_element(
                            By.ID, f"rqAnswerOption{i}"
                        ).get_attribute("data-option")
                        == correctOption
                    ):
                        self.webdriver.find_element(By.ID, f"rqAnswerOption{i}").click()
                        time.sleep(5)
                        if not self.browser.utils.waitUntilQuestionRefresh():
                            self.browser.utils.resetTabs()
                            return
                        break
            if question + 1 != numberOfQuestions:
                time.sleep(5)
        time.sleep(5)
        self.browser.utils.closeCurrentTab()

    def completeABC(self):
        counter = self.webdriver.find_element(
            By.XPATH, '//*[@id="QuestionPane0"]/div[2]'
        ).text[:-1][1:]
        numberOfQuestions = max(int(s) for s in counter.split() if s.isdigit())
        for question in range(numberOfQuestions):
            self.webdriver.find_element(
                By.ID, f"questionOptionChoice{question}{random.randint(0, 2)}"
            ).click()
            time.sleep(5)
            self.webdriver.find_element(By.ID, f"nextQuestionbtn{question}").click()
            time.sleep(3)
        time.sleep(5)
        self.browser.utils.closeCurrentTab()

    def completeThisOrThat(self):
        if not self.browser.utils.waitUntilQuizLoads():
            self.browser.utils.resetTabs()
            return
        self.webdriver.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        self.browser.utils.waitUntilVisible(
            By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10
        )
        time.sleep(3)
        for _ in range(10):
            correctAnswerCode = self.webdriver.execute_script(
                "return _w.rewardsQuizRenderInfo.correctAnswer"
            )
            answer1, answer1Code = self.getAnswerAndCode("rqAnswerOption0")
            answer2, answer2Code = self.getAnswerAndCode("rqAnswerOption1")
            if answer1Code == correctAnswerCode:
                answer1.click()
                time.sleep(8)
            elif answer2Code == correctAnswerCode:
                answer2.click()
                time.sleep(8)

        time.sleep(5)
        self.browser.utils.closeCurrentTab()

    def getAnswerAndCode(self, answerId: str) -> tuple:
        answerEncodeKey = self.webdriver.execute_script("return _G.IG")
        answer = self.webdriver.find_element(By.ID, answerId)
        answerTitle = answer.get_attribute("data-option")
        if answerTitle is not None:
            return (
                answer,
                self.browser.utils.getAnswerCode(answerEncodeKey, answerTitle),
            )
        else:
            return (answer, None)
