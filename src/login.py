import contextlib
import time
import urllib.parse

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from .constants import BASE_URL
from .utils import Utils


class Login:
    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.utils = Utils(browser)

    def login(self, email: str, password: str, isMobile: bool = False):
        self.browser.get("https://login.live.com/")

        alreadyLoggedIn = False
        while True:
            try:
                self.utils.waitUntilVisible(
                    By.CSS_SELECTOR, 'html[data-role-name="MeePortal"]', 0.1
                )
                alreadyLoggedIn = True
                break
            except Exception:  # pylint: disable=broad-except
                try:
                    self.utils.waitUntilVisible(By.ID, "loginHeader", 0.1)
                    break
                except Exception:  # pylint: disable=broad-except
                    if self.utils.tryDismissAllMessages():
                        continue

        if not alreadyLoggedIn:
            self.executeLogin(email, password)
        self.utils.tryDismissCookieBanner()

        print("[LOGIN]", "Logged-in !")

        self.browser.get(BASE_URL)
        while True:
            self.utils.tryDismissCookieBanner()
            with contextlib.suppress(Exception):
                self.browser.find_element(By.ID, "daily-sets")
                break
            if (
                urllib.parse.urlparse(self.browser.current_url).hostname
                != urllib.parse.urlparse(BASE_URL).hostname
            ) and self.utils.tryDismissAllMessages():
                time.sleep(1)
                self.browser.get(BASE_URL)
            time.sleep(1)
        points = self.utils.getAccountPoints()

        print("[LOGIN]", "Ensuring login on Bing...")
        self.checkBingLogin(isMobile)

        return points

    def executeLogin(self, email, password):
        self.utils.waitUntilVisible(By.ID, "loginHeader", 10)
        print("[LOGIN]", "Writing email...")
        self.browser.find_element(By.NAME, "loginfmt").send_keys(email)
        self.browser.find_element(By.ID, "idSIButton9").click()

        try:
            self.enterPassword(password)
        except Exception:  # pylint: disable=broad-except
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
            self.utils.tryDismissAllMessages()
            time.sleep(1)

        self.utils.waitUntilVisible(
            By.CSS_SELECTOR, 'html[data-role-name="MeePortal"]', 10
        )

    def enterPassword(self, password):
        self.utils.waitUntilClickable(By.NAME, "passwd", 10)
        self.utils.waitUntilClickable(By.ID, "idSIButton9", 10)
        # browser.find_element(By.NAME, "passwd").send_keys(password)
        # If password contains special characters like " ' or \, send_keys() will not work
        password = password.replace("\\", "\\\\").replace('"', '\\"')
        self.browser.execute_script(
            f'document.getElementsByName("passwd")[0].value = "{password}";'
        )
        print("[LOGIN]", "Writing password...")
        self.browser.find_element(By.ID, "idSIButton9").click()
        time.sleep(3)

    def checkBingLogin(self, isMobile: bool = False):
        self.browser.get(
            "https://www.bing.com/fd/auth/signin?action=interactive&provider=windows_live_id&return_url=https%3A%2F%2Fwww.bing.com%2F"
        )
        isHamburgerOpened = False
        while True:
            currentUrl = urllib.parse.urlparse(self.browser.current_url)
            if currentUrl.hostname == "www.bing.com" and currentUrl.path == "/":
                time.sleep(3)
                self.utils.tryDismissBingCookieBanner()
                with contextlib.suppress(Exception):
                    if isMobile:
                        if not isHamburgerOpened:
                            self.browser.find_element(By.ID, "mHamburger").click()
                            isHamburgerOpened = True

                        self.browser.find_element(By.ID, "fly_id_rc").get_attribute(
                            "innerHTML"
                        )

                    else:
                        self.browser.find_element(By.ID, "id_rc").get_attribute(
                            "innerHTML"
                        )

                    break
            time.sleep(1)
