import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from .constants import DESKTOP_USER_AGENT, MOBILE_USER_AGENT


def browserSetup(
    sessionName: str,
    headlessMode: bool = False,
    isMobile: bool = False,
    lang: str = "en",
) -> WebDriver:
    options = Options()
    options.add_argument(
        f"user-agent={MOBILE_USER_AGENT if isMobile else DESKTOP_USER_AGENT}"
    )
    options.add_argument(f"lang={lang}")
    if headlessMode:
        options.add_argument("--headless")
    options.add_argument("log-level=3")
    currentPath = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(currentPath)
    options.add_argument(
        f'--user-data-dir={parent}/sessions/{"mobile" if isMobile else "desktop"}/{sessionName}'
    )
    return webdriver.Chrome(options=options)
