""" Login module """

import contextlib
import time
import urllib.parse

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from .constants import BASE_URL
from .utils import Utils


class Login:
    """
    A class that handles logging in to the Microsoft Rewards website.
    """

    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.utils = Utils(browser)

    def login(self, email: str, password: str, is_mobile: bool = False):
        """
        Logs in to the Microsoft Rewards website using the provided email and password.

        Args:
            email (str): The email address to use for logging in.
            password (str): The password to use for logging in.
            is_mobile (bool, optional): Is Mobile version of the website. Defaults to False.

        Returns:
            int: The number of points in the user's account after logging in.
        """
        self.browser.get("https://login.live.com/")

        already_logged_in = False
        while True:
            try:
                self.utils.wait_until_visible(
                    By.CSS_SELECTOR, 'html[data-role-name="MeePortal"]', 0.1
                )
                already_logged_in = True
                break
            except Exception:
                try:
                    self.utils.wait_until_visible(By.ID, "loginHeader", 0.1)
                    break
                except Exception:
                    if self.utils.try_dismiss_all_messages():
                        continue

        if not already_logged_in:
            self.execute_login(email, password)
        self.utils.try_dismiss_cookie_banner()

        print("[LOGIN]", "Logged-in !")

        self.browser.get(BASE_URL)
        while True:
            self.utils.try_dismiss_cookie_banner()
            with contextlib.suppress(Exception):
                self.browser.find_element(By.ID, "daily-sets")
                break
            if (
                urllib.parse.urlparse(self.browser.current_url).hostname
                != urllib.parse.urlparse(BASE_URL).hostname
            ) and self.utils.try_dismiss_all_messages():
                time.sleep(1)
                self.browser.get(BASE_URL)
            time.sleep(1)
        points = self.utils.get_account_points()

        print("[LOGIN]", "Ensuring login on Bing...")
        self.check_bing_login(is_mobile)

        return points

    def execute_login(self, email, password):
        """
        Logs in to the Microsoft Rewards website if the user is not already logged in.

        Args:
            email (str): The email address associated with the Microsoft account.
            password (str): The password for the Microsoft account.

        Returns:
            None
        """
        self.utils.wait_until_visible(By.ID, "loginHeader", 10)
        print("[LOGIN]", "Writing email...")
        self.browser.find_element(By.NAME, "loginfmt").send_keys(email)
        self.browser.find_element(By.ID, "idSIButton9").click()

        try:
            self.fill_password(password)
        except Exception:
            print("[LOGIN]", "2FA required !")
            with contextlib.suppress(Exception):
                code = self.browser.find_element(
                    By.ID, "idRemoteNGC_DisplaySign"
                ).get_attribute("innerHTML")
                print("[LOGIN]", "2FA code:", code)
            input("[LOGIN] Press enter when confirmed...")

        while not (
            urllib.parse.urlparse(self.browser.current_url).path == "/"
            and urllib.parse.urlparse(self.browser.current_url).hostname
            == "account.microsoft.com"
        ):
            self.utils.try_dismiss_all_messages()
            time.sleep(1)

        self.utils.wait_until_visible(
            By.CSS_SELECTOR, 'html[data-role-name="MeePortal"]', 10
        )

    def fill_password(self, password):
        """
        Fills in the password field on the Microsoft login page and submits the form.

        Args:
            password (str): The password for the Microsoft account.

        Returns:
            None
        """
        self.utils.wait_until_clickable(By.NAME, "passwd", 10)
        self.utils.wait_until_clickable(By.ID, "idSIButton9", 10)
        # browser.find_element(By.NAME, "passwd").send_keys(password)
        # If password contains special characters like " ' or \, send_keys() will not work
        password = password.replace("\\", "\\\\").replace('"', '\\"')
        self.browser.execute_script(
            f'document.getElementsByName("passwd")[0].value = "{password}";'
        )
        print("[LOGIN]", "Writing password...")
        self.browser.find_element(By.ID, "idSIButton9").click()
        time.sleep(3)

    def check_bing_login(self, is_mobile: bool = False):
        """
        Checks if the user is logged in to Bing and returns the user's reward points.

        Args:
            is_mobile (bool): A boolean indicating whether the user is
            accessing the website from a mobile device.

        Returns:
            str: The user's reward points as a string.
        """
        self.browser.get(
            "https://www.bing.com/fd/auth/signin?action=interactive&provider=windows_live_id"
            "&return_url=https%3A%2F%2Fwww.bing.com%2F"
        )
        is_hamburger_opened = False
        while True:
            current_url = urllib.parse.urlparse(self.browser.current_url)
            if current_url.hostname == "www.bing.com" and current_url.path == "/":
                time.sleep(3)
                self.utils.try_dismiss_bing_cookie_banner()
                with contextlib.suppress(Exception):
                    if not is_mobile:
                        return self.browser.find_element(By.ID, "id_rc").get_attribute(
                            "innerHTML"
                        )

                    if not is_hamburger_opened:
                        self.browser.find_element(By.ID, "mHamburger").click()
                        is_hamburger_opened = True
                    return self.browser.find_element(By.ID, "fly_id_rc").get_attribute(
                        "innerHTML"
                    )
            time.sleep(1)
