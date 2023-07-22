"""Browser setup module."""
import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from .constants import DESKTOP_USER_AGENT, MOBILE_USER_AGENT


def browser_setup(
    session_name: str,
    headless_mode: bool = False,
    is_mobile: bool = False,
    lang: str = "en",
) -> WebDriver:
    """
    Sets up a Selenium WebDriver instance with the specified options.

    Args:
        session_name (str): The name of the session to use.
        headless_mode (bool, optional): Run the browser in headless mode. Defaults to False.
        is_mobile (bool, optional): Is a mobile user agent. Defaults to False.
        lang (str, optional): The language to use. Defaults to "en".

    Returns:
        WebDriver: The configured WebDriver instance.
    """
    options = Options()
    options.add_argument(
        f"user-agent={MOBILE_USER_AGENT if is_mobile else DESKTOP_USER_AGENT}"
    )
    options.add_argument(f"lang={lang}")
    if headless_mode:
        options.add_argument("--headless")
    options.add_argument("log-level=3")
    user_data_dir = set_user_data_dir(is_mobile, session_name)
    options.add_argument(f"--user-data-dir={user_data_dir.as_posix()}")
    return webdriver.Chrome(options=options)


def set_user_data_dir(is_mobile, session_name):
    """
    Sets the user data directory for a Selenium WebDriver instance based on
    the type of device being used and a session name.

    Args:
        options: A `Options` instance for the Selenium WebDriver.
        is_mobile: A boolean indicating whether the device is mobile or desktop.
        session_name: A string containing the name of the session.

    Returns:
        None
    """
    current_path = Path(os.path.realpath(__file__))
    parent = current_path.parent.parent
    sessions_dir = parent / "sessions" / ("mobile" if is_mobile else "desktop")
    sessions_dir.mkdir(parents=True, exist_ok=True)
    return sessions_dir / session_name
