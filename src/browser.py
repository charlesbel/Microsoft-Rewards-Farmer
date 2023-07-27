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


def setupProfiles(is_mobile: bool, session_name: str):
    """
    Sets up the sessions profile for the chrome browser.
    Uses the session name to create a unique profile for the session.

    Args:
        is_mobile: A boolean indicating whether the device is mobile or desktop.
        session_name: A string containing the name of the session.

    Returns:
        None
    """
    current_path = Path(__file__)
    parent = current_path.parent.parent
    sessions_dir = parent / "sessions"

    # In effort to avoid any issues with the session name, we will seed the session name as a uuid.
    session_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, session_name)
    sessions_dir = (
        sessions_dir / str(session_uuid) / ("mobile" if is_mobile else "desktop")
    )
    sessions_dir.mkdir(parents=True, exist_ok=True)
    return sessions_dir
