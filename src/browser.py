import contextlib
from pathlib import Path
from typing import Any

import ipapi
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from src.userAgentGenerator import GenerateUserAgent
from src.utils import Utils


class Browser:
    """WebDriver wrapper class."""

    def __init__(self, mobile: bool, account, args: Any) -> None:
        self.mobile = mobile
        self.browserType = "mobile" if mobile else "desktop"
        self.headless = not args.visible
        self.username = account["username"]
        self.password = account["password"]
        self.localeLang, self.localeGeo = self.getCCodeLang(args.lang, args.geo)
        self.userAgent = GenerateUserAgent().user_agent(mobile)
        self.webdriver = self.browserSetup()
        self.utils = Utils(self.webdriver)

    def __enter__(self) -> "Browser":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close_browser()

    def close_browser(self) -> None:
        """Perform actions to close the browser cleanly."""
        # close web browser
        with contextlib.suppress(Exception):
            self.webdriver.quit()

    def browserSetup(
        self,
    ) -> WebDriver:
        options = Options()
        options.add_argument(f"user-agent={self.userAgent}")
        options.add_argument(f"lang={self.localeLang}")
        if self.headless:
            options.add_argument("headless")
        options.add_argument("log-level=3")
        userDataDir, profileType = self.setupProfiles()
        options.add_argument(f"user-data-dir={userDataDir.as_posix()}")
        options.add_argument(f"profile-directory={profileType}")
        return webdriver.Chrome(options=options)

    def setupProfiles(self) -> tuple[Path, str]:
        """
        Sets up the sessions profile for the chrome browser.
        Uses the session name to create a unique profile for the session.

        Returns:
            tuple[Path, str]: A tuple containing the path to the session directory and the profile type.
        """
        currentPath = Path(__file__)
        parent = currentPath.parent.parent
        sessionsDir = parent / "sessions"

        profileType = f"{str(self.username)} {self.browserType}"

        sessionsDir.mkdir(parents=True, exist_ok=True)
        return sessionsDir, profileType

    def getCCodeLang(self, lang: str = "en", geo: str = "US") -> tuple:
        try:
            if lang is None:
                lang = "en"
            if geo is None:
                geo = "US"
            nfo = ipapi.location()
            if isinstance(nfo, dict):
                lang = nfo["languages"].split(",")[0].split("-")[0]
                geo = nfo["country"]
            return (lang, geo)
        except Exception:  # pylint: disable=broad-except
            return (lang, geo)
