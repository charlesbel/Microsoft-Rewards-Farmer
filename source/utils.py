"""
This module contains utility functions used in the Microsoft Rewards Farmer project.
"""


import contextlib
import time
import urllib.parse

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from .constants import BASE_URL


class Utils:
    """
    A collection of utility functions used in the Microsoft Rewards Farmer project.
    """

    def __init__(self, browser: WebDriver):
        self.browser = browser

    def wait_until_visible(self, by_: str, selector: str, time_to_wait: float = 10):
        """
        Waits until an element is visible on the page.

        Args:
            by_ (By): The method used to locate the element.
            selector (str): The selector used to locate the element.
            time_to_wait (int, optional): The amount of time to wait for
            the element to become visible. Defaults to 10.
        """
        WebDriverWait(self.browser, time_to_wait).until(
            ec.visibility_of_element_located((by_, selector))
        )

    def wait_until_clickable(self, by_: str, selector: str, time_to_wait: float = 10):
        """
        Waits until an element is clickable on the page.

        Args:
            by_ (str): The method used to locate the element.
            selector (str): The selector used to locate the element.
            time_to_wait (int, optional): The amount of time to wait for
            the element to become clickable. Defaults to 10.
        """
        WebDriverWait(self.browser, time_to_wait).until(
            ec.element_to_be_clickable((by_, selector))
        )

    def wait_for_ms_reward_element(self, by_: str, selector: str):
        """
        Waits for an element with the specified selector to appear on the page.

        Args:
            by_ (str): The method used to locate the element.
            selector (str): The selector used to locate the element.

        Returns:
            bool: True if the element is found, False otherwise.
        """
        loading_time_allowed = 5
        refreshs_allowed = 5

        checking_interval = 0.5
        checks = loading_time_allowed / checking_interval

        tries = 0
        refresh_count = 0
        while True:
            try:
                self.browser.find_element(by_, selector)
                return True
            except Exception:
                if tries < checks:
                    tries += 1
                    time.sleep(checking_interval)
                elif refresh_count < refreshs_allowed:
                    self.browser.refresh()
                    refresh_count += 1
                    tries = 0
                    time.sleep(5)
                else:
                    return False

    def wait_until_question_refresh(self):
        """
        Waits for the question to refresh on the page.

        Returns:
            bool: True if the question is refreshed, False otherwise.
        """
        return self.wait_for_ms_reward_element(By.CLASS_NAME, "rqECredits")

    def wait_until_quiz_loads(self):
        """
        Waits for the quiz to load on the page.

        Returns:
            bool: True if the quiz is loaded, False otherwise.
        """
        return self.wait_for_ms_reward_element(By.XPATH, '//*[@id="rqStartQuiz"]')

    def reset_tabs(self):
        """
        Closes all tabs except the current one and navigates to the home page.

        Returns:
            None
        """
        try:
            curr = self.browser.current_window_handle

            for handle in self.browser.window_handles:
                if handle != curr:
                    self.browser.switch_to.window(handle)
                    time.sleep(0.5)
                    self.browser.close()
                    time.sleep(0.5)

            self.browser.switch_to.window(curr)
            time.sleep(0.5)
            self.go_home()
        except Exception:
            self.go_home()

    def go_home(self):
        """
        Navigates to the Microsoft Rewards home page and waits for the daily sets to load.
        If the current URL is not the same as the base URL, it will navigate to the base URL.
        """
        current_url = urllib.parse.urlparse(self.browser.current_url)
        target_url = urllib.parse.urlparse(BASE_URL)
        if (
            current_url.hostname != target_url.hostname
            or current_url.path != target_url.path
        ):
            self.browser.get(BASE_URL)
            while True:
                self.try_dismiss_cookie_banner()
                with contextlib.suppress(Exception):
                    self.browser.find_element(By.ID, "more-activities")
                    break
                if (
                    urllib.parse.urlparse(self.browser.current_url).hostname
                    != target_url.hostname
                ) and self.try_dismiss_all_messages():
                    time.sleep(2)
                    self.browser.get(BASE_URL)
                time.sleep(0.5)

    def get_answer_code(self, key: str, string: str) -> str:
        """
        Calculates the answer code for a given key and string.

        Args:
            key (str): The key used to calculate the answer code.
            string (str): The string used to calculate the answer code.

        Returns:
            str: The answer code calculated from the key and string.
        """
        answer_code = sum(ord(string[i]) for i in range(len(string)))
        answer_code += int(key[-2:], 16)
        return str(answer_code)

    def get_dashboard_data(self) -> dict:
        """
        Returns the dashboard data as a dictionary.

        Returns:
            dict: The dashboard data as a dictionary.
        """
        return self.browser.execute_script("return dashboard")

    def get_account_points(self) -> int:
        """
        Returns the number of available points in the user's Microsoft Rewards account.

        Returns:
            int: The number of available points in the user's account.
        """
        return self.get_dashboard_data()["userStatus"]["availablePoints"]

    def try_dismiss_all_messages(self):
        """
        Dismisses all messages on the current page.
        """
        buttons = [
            (By.ID, "iLandingViewAction"),
            (By.ID, "iShowSkip"),
            (By.ID, "iNext"),
            (By.ID, "iLooksGood"),
            (By.ID, "idSIButton9"),
            (By.CSS_SELECTOR, ".ms-Button.ms-Button--primary"),
        ]
        result = False
        for button in buttons:
            try:
                self.browser.find_element(button[0], button[1]).click()
                result = True
            except Exception:
                continue
        return result

    def try_dismiss_cookie_banner(self):
        with contextlib.suppress(Exception):
            self.browser.find_element(By.ID, "cookie-banner").find_element(
                By.TAG_NAME, "button"
            ).click()
            time.sleep(2)

    def try_dismiss_bing_cookie_banner(self):
        with contextlib.suppress(Exception):
            self.browser.find_element(By.ID, "bnp_btn_accept").click()
            time.sleep(2)

    def switch_to_new_tab(self, time_to_wait: int = 0):
        time.sleep(0.5)
        self.browser.switch_to.window(window_name=self.browser.window_handles[1])
        if time_to_wait > 0:
            time.sleep(time_to_wait)

    def close_current_tab(self):
        self.browser.close()
        time.sleep(0.5)
        self.browser.switch_to.window(window_name=self.browser.window_handles[0])
        time.sleep(0.5)

    def visit_new_tab(self, time_to_wait: int = 0):
        self.switch_to_new_tab(time_to_wait)
        self.close_current_tab()

    def get_remaining_searches(self):
        dashboard = self.get_dashboard_data()
        search_points = 1
        counters = dashboard["userStatus"]["counters"]
        if "pcSearch" not in counters:
            return 0, 0
        progress_desktop = (
            counters["pcSearch"][0]["pointProgress"]
            + counters["pcSearch"][1]["pointProgress"]
        )
        target_desktop = (
            counters["pcSearch"][0]["pointProgressMax"]
            + counters["pcSearch"][1]["pointProgressMax"]
        )
        if target_desktop == 33 or target_desktop != 55 and target_desktop == 102:
            # Level 1 EU
            search_points = 3
        elif target_desktop == 55 or target_desktop >= 170:
            # Level 1 US
            search_points = 5
        remaining_desktop = int((target_desktop - progress_desktop) / search_points)
        remaining_mobile = 0
        if dashboard["userStatus"]["levelInfo"]["activeLevel"] != "Level1":
            progress_mobile = counters["mobileSearch"][0]["pointProgress"]
            target_mobile = counters["mobileSearch"][0]["pointProgressMax"]
            remaining_mobile = int((target_mobile - progress_mobile) / search_points)
        return remaining_desktop, remaining_mobile
