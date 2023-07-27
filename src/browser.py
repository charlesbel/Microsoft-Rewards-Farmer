import uuid
from pathlib import Path

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
    userDataDir = setupProfiles(isMobile, sessionName)
    options.add_argument(f"--user-data-dir={userDataDir.as_posix()}")
    return webdriver.Chrome(options=options)


def setupProfiles(isMobile: bool, sessionName: str) -> Path:
    """
    Sets up the sessions profile for the chrome browser.
    Uses the session name to create a unique profile for the session.

    Args:
        isMobile: A boolean indicating whether the device is mobile or desktop.
        sessionName: A string containing the name of the session.

    Returns:
        Path
    """
    currentPath = Path(__file__)
    parent = currentPath.parent.parent
    sessionsDir = parent / "sessions"

    # In effort to avoid any issues with the session name, we will seed the session name as a uuid.
    sessionUuid = uuid.uuid5(uuid.NAMESPACE_DNS, sessionName)
    sessionsDir = sessionsDir / str(sessionUuid) / ("mobile" if isMobile else "desktop")
    sessionsDir.mkdir(parents=True, exist_ok=True)
    return sessionsDir
