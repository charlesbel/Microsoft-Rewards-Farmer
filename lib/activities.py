"""Activities module.

This module contains the Activities class which is used to complete
"""
import random
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from .utils import Utils


class Activities:
    """
    The Activities class is used to complete various activities on the Microsoft Rewards website.
    These activities include completing daily sets, surveys, quizzes, and more promotions.
    """

    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.utils = Utils(browser)

    def open_daily_set_activity(self, card_id: int):
        """
        Opens the daily set activity with the given card ID.

        Args:
            cardId (int): The ID of the card to click on to open the daily set activity.

        Returns:
            None
        """
        self.browser.find_element(
            By.XPATH,
            '//*[@id="daily-sets"]/mee-card-group[1]/div/'
            f"mee-card[{card_id}]/div/card-content/mee-rewards-daily-set-item-content/div/a",
        ).click()
        self.utils.switch_to_new_tab(8)

    def open_more_promotions_activity(self, card_id: int):
        """
        Opens the more promotions activity with the given card ID.

        Args:
            cardId (int): The ID of the card to click on to open the more promotions activity.

        Returns:
            None
        """
        self.browser.find_element(
            By.XPATH,
            f'//*[@id="more-activities"]/div/mee-card[{card_id}]/'
            "div/card-content/mee-rewards-more-activities-card-item/div/a",
        ).click()
        self.utils.switch_to_new_tab(8)

    def complete_search(self):
        """
        Completes a search activity on the Microsoft Rewards website.

        Returns:
            None
        """
        time.sleep(random.randint(5, 10))
        self.utils.close_current_tab()

    def complete_survey(self):
        """
        Completes a survey activity on the Microsoft Rewards website by
        selecting a random option and waiting for a random amount of time.

        Returns:
            None
        """
        self.browser.find_element(By.ID, f"btoption{random.randint(0, 1)}").click()
        time.sleep(random.randint(10, 15))
        self.utils.close_current_tab()

    def complete_quiz(self):
        """
        Completes a quiz activity on the Microsoft Rewards website by
        answering each question and waiting for a random amount of time between questions.

        Returns:
            None
        """
        if not self.utils.wait_until_quiz_loads():
            self.utils.reset_tabs()
            return
        self.browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        self.utils.wait_until_visible(
            By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10
        )
        time.sleep(3)
        number_of_questions = self.browser.execute_script(
            "return _w.rewardsQuizRenderInfo.maxQuestions"
        )
        number_of_options = self.browser.execute_script(
            "return _w.rewardsQuizRenderInfo.numberOfOptions"
        )
        for question in range(number_of_questions):
            if number_of_options == 8:
                answers = [
                    f"rqAnswerOption{i}"
                    for i in range(number_of_options)
                    if (
                        self.browser.find_element(By.ID, f"rqAnswerOption{i}")
                        .get_attribute("iscorrectoption")
                        .lower()  # type: ignore
                        == "true"
                    )
                ]
                for answer in answers:
                    self.browser.find_element(By.ID, answer).click()
                    time.sleep(5)
                    if not self.utils.wait_until_question_refresh():
                        self.utils.reset_tabs()
                        return
            elif number_of_options in [2, 4]:
                correct_option = self.browser.execute_script(
                    "return _w.rewardsQuizRenderInfo.correctAnswer"
                )
                for i in range(number_of_options):
                    if (
                        self.browser.find_element(
                            By.ID, f"rqAnswerOption{i}"
                        ).get_attribute("data-option")
                        == correct_option
                    ):
                        self.browser.find_element(By.ID, f"rqAnswerOption{i}").click()
                        time.sleep(5)
                        if not self.utils.wait_until_question_refresh():
                            self.utils.reset_tabs()
                            return
                        break
            if question + 1 != number_of_questions:
                time.sleep(5)
        time.sleep(5)
        self.utils.close_current_tab()

    def complete_abc(self):
        """
        This method is used to complete the ABC quiz on the Microsoft Rewards website.
        It iterates through each question and randomly selects an answer option
        before moving on to the next question.
        """
        counter = self.browser.find_element(
            By.XPATH, '//*[@id="QuestionPane0"]/div[2]'
        ).text[:-1][1:]
        number_of_questions = max(int(s) for s in counter.split() if s.isdigit())
        for question in range(number_of_questions):
            self.browser.find_element(
                By.ID, f"questionOptionChoice{question}{random.randint(0, 2)}"
            ).click()
            time.sleep(5)
            self.browser.find_element(By.ID, f"nextQuestionbtn{question}").click()
            time.sleep(3)
        time.sleep(5)
        self.utils.close_current_tab()

    def complete_this_or_that(self):
        """
        This method is used to complete the "This or That" quiz on the Microsoft Rewards website.
        It iterates through each question and randomly selects one of the two answer options
        before moving on to the next question.
        """
        number_of_questions = 10
        if not self.utils.wait_until_quiz_loads():
            self.utils.reset_tabs()
            return
        self.browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        self.utils.wait_until_visible(
            By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10
        )
        time.sleep(3)
        for question in range(number_of_questions):
            answer_encode_key = self.browser.execute_script("return _G.IG")

            answer1 = self.browser.find_element(By.ID, "rqAnswerOption0")
            answer1_title = answer1.get_attribute("data-option")
            if answer1_title is not None:
                answer1_code = self.utils.get_answer_code(
                    answer_encode_key, answer1_title
                )
            else:
                answer1_code = ""

            answer2 = self.browser.find_element(By.ID, "rqAnswerOption1")
            answer2_title = answer2.get_attribute("data-option")
            answer2_code = self.utils.get_answer_code(
                answer_encode_key, answer2_title or ""
            )

            correct_answer_code = self.browser.execute_script(
                "return _w.rewardsQuizRenderInfo.correctAnswer"
            )

            if answer1_code == correct_answer_code:
                answer1.click()
            elif answer2_code == correct_answer_code:
                answer2.click()
            if question + 1 != number_of_questions:
                time.sleep(8)

        time.sleep(5)
        self.utils.close_current_tab()
