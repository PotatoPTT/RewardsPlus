import contextlib
import uuid
from pathlib import Path
from typing import Any

import ipapi
import undetected_chromedriver as uc
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
        self.userAgent = GenerateUserAgent().userAgent(mobile)
        self.webdriver = self.browserSetup()
        self.utils = Utils(self.webdriver)

    def __enter__(self) -> "Browser":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.closeBrowser()

    def closeBrowser(self) -> None:
        """Perform actions to close the browser cleanly."""
        # close web browser
        with contextlib.suppress(Exception):
            self.webdriver.quit()

    def browserSetup(
        self,
    ) -> WebDriver:
        options = uc.ChromeOptions()
        options.add_argument(f"--user-agent={self.userAgent}")
        options.add_argument(f"--lang={self.localeLang}")
        options.add_argument("--log-level=3")
        options.add_argument("--window-size=1500,843")
        userDataDir = self.setupProfiles()
        options.add_argument(f"--user-data-dir={userDataDir.as_posix()}")
        if self.headless:
            browser = uc.Chrome(options=options, headless=True, version_main=116)
        else:
            browser = uc.Chrome(options=options)
        if self.browserType == "mobile":
            browser.set_window_size(720, 1080)
        else:
            browser.set_window_size(1500, 843)
        return browser

    def setupProfiles(self) -> Path:
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

        sessionUuid = uuid.uuid5(uuid.NAMESPACE_DNS, self.username)
        sessionsDir = sessionsDir / str(sessionUuid) / self.browserType
        sessionsDir.mkdir(parents=True, exist_ok=True)
        return sessionsDir

    def getCCodeLang(self, lang: str, geo: str) -> tuple:
        if lang is None or geo is None:
            try:
                nfo = ipapi.location()
                if isinstance(nfo, dict):
                    if lang is None:
                        lang = nfo["languages"].split(",")[0].split("-")[0]
                    if geo is None:
                        geo = nfo["country"]
            except Exception:  # pylint: disable=broad-except
                return ("pt-BR", "BR")
        return (lang, geo)
