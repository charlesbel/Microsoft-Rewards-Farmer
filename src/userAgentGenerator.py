"""User Agent Builder"""

from typing import Any

import requests
from requests import HTTPError, Response


class GenerateUserAgent:
    """A class for generating user agents for Microsoft Rewards Farmer."""

    EDGE_VERSION_MAJOR = ["115", "0", "1901"]
    CHROME_VERSION_MAJOR = ["114", "0", "5735"]

    CHROME_VERSION_PC = "90"
    CHROME_VERSION_MOBILE = "90"

    EDGE_VERSION_PC = "183"
    EDGE_VERSION_MOBILE = "183"

    MOBILE_DEVICE = "HD1913"

    USER_AGENT_TEMPLATE = {
        "edge_pc": (
            "Mozilla/5.0"
            " ({system}) AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/{app[chrome_version]} Safari/537.36"
            " Edg/{app[edge_version]}"
        ),
        "edge_mobile": (
            "Mozilla/5.0"
            " ({system}) AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/{app[chrome_version]} Mobile Safari/537.36"
            " EdgA/{app[edge_version]}"
        ),
    }

    OS_PLATFORM = {"win": "Windows NT 10.0", "android": "Linux"}
    OS_CPU = {"win": "Win64; x64", "android": "Android 10"}
    grabbed: bool = False
    browserVersions: dict[str, Any] = {}

    def userAgent(
        self,
        mobile: bool = False,
        fetch: bool = True,
    ) -> str:
        """
        Generates a user agent string for either a mobile or PC device.

        Args:
            mobile: A boolean indicating whether the user agent should be generated for a mobile device.
            fetch: A boolean indicating whether to fetch the latest browser versions.

        Returns:
            A string containing the user agent for the specified device.
        """

        system = self.__getSystemComponents(mobile)
        app = self.__getAppComponents(mobile, fetch)
        uaTemplate = (
            self.USER_AGENT_TEMPLATE.get("edge_mobile", "")
            if mobile
            else self.USER_AGENT_TEMPLATE.get("edge_pc", "")
        )

        return uaTemplate.format(system=system, app=app)

    def __getSystemComponents(self, mobile: bool) -> str:
        """
        Generates the system components for the user agent string.

        Args:
            mobile: A boolean indicating whether the user agent should be generated for a mobile device.

        Returns:
            A string containing the system components for the user agent string.
        """
        osId = self.OS_CPU.get("android") if mobile else self.OS_CPU.get("win")
        uaPlatform = (
            self.OS_PLATFORM.get("android") if mobile else self.OS_PLATFORM.get("win")
        )
        if mobile:
            osId = f"{osId}; {self.MOBILE_DEVICE}"
        return f"{uaPlatform}; {osId}"

    def __getAppComponents(self, mobile: bool, fetch: bool) -> dict[str, Any]:
        """
        Generates the application components for the user agent string.

        Args:
            mobile: A boolean indicating whether the user agent should be generated for a mobile device.
            fetch: A boolean indicating whether to fetch the latest browser versions.

        Returns:
            A dictionary containing the application components for the user agent string.
        """
        chromeMinorVersion = (
            self.CHROME_VERSION_MOBILE if mobile else self.CHROME_VERSION_PC
        )
        chromeVersion = self.__generateVersion(
            self.CHROME_VERSION_MAJOR, chromeMinorVersion
        )

        edgeMinorVersion = self.EDGE_VERSION_MOBILE if mobile else self.EDGE_VERSION_PC
        edgeVersion = self.__generateVersion(self.EDGE_VERSION_MAJOR, edgeMinorVersion)
        if fetch and not self.grabbed:
            try:
                fetchedEdgeVersion = self.getEdgeVersion()
                # TODO: Add a logger to increase verbosity
                # if fetched_edge_version != edge_version:
                #     log_msg = (
                #         f"Fetched Edge version {fetched_edge_version} "
                #         f"is different from the expected {edge_version}"
                #     )
                #     logger.trace(log_msg)
                fetchedChromeVersion = self.getChromeVersion()
                # if fetched_chrome_version != chrome_version:
                #     log_msg = (
                #         f"Fetched Chrome version {fetched_chrome_version} "
                #         f"is different from the expected {chrome_version}"
                #     )
                #     logger.trace(log_msg)
                self.browserVersions = {
                    "chrome_version": fetchedChromeVersion,
                    "edge_version": fetchedEdgeVersion,
                }
                self.grabbed = True
            except Exception:  # pylint: disable=broad-except
                print("Failed to get webdriver version.")
                # logger.warning("Failed to get webdriver version.")
        if not self.browserVersions:
            self.browserVersions = {
                "chrome_version": chromeVersion,
                "edge_version": edgeVersion,
            }
        return self.browserVersions

    @staticmethod
    def __generateVersion(major: list[str], minor: str) -> str:
        """
        Generate a version.

        Args:
            major (list[str]): A list of three strings representing the major version.
            minor (str): A string representing the minor version.

        Returns:
            str: A string representing the generated version.
        """
        return f"{major[0]}.{major[1]}.{major[2]}.{minor}"

    def getChromeVersion(self) -> str:
        """
        Get the latest version of Chrome.

        Returns:
            str: The latest version of Chrome.
        """
        latestReleaseUrl = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        return self.getWebdriverPage(latestReleaseUrl).text

    def getEdgeVersion(self) -> str:
        """
        Get the latest version of Microsoft Edge.

        Returns:
            str: The latest version of Microsoft Edge.
        """
        edge_release_url = (
            "https://msedgewebdriverstorage.blob.core.windows.net"
            "/edgewebdriver/LATEST_STABLE"
        )
        response = self.getWebdriverPage(edge_release_url)
        return response.content.decode("utf-16").split("\r")[0].split("\n")[0]

    @staticmethod
    def getWebdriverPage(url: str) -> Response:
        """
        Get the webdriver page.

        Args:
            url (str): The URL of the webdriver page.

        Returns:
            Response: The response object of the webdriver page.
        """
        response = None
        try:
            response = requests.get(url=url, timeout=10)
        except Exception:  # pylint: disable=broad-except # noqa
            # Prevent SSLCertVerificationError / CERTIFICATE_VERIFY_FAILED
            url = url.replace("https://", "http://")
            response = requests.get(url=url, timeout=10)
        if response.status_code != requests.codes.ok:  # pylint: disable=no-member
            raise HTTPError(
                f"Failed to get webdriver page {url}. "
                f"Status code: {response.status_code}"
            )
        return response
        
        
    def getCMDArgs(self, mobile: bool = False, fetch: bool = True):
        agentString = self.userAgent(mobile, fetch)
        
        if mobile:
            platform = "Android"
            edgeVersionString = f"{self.EDGE_VERSION_MAJOR[0]}.{self.EDGE_VERSION_MAJOR[1]}.{self.EDGE_VERSION_MAJOR[1]}.{self.EDGE_VERSION_MOBILE}"
            chromeVersionString = f"{self.CHROME_VERSION_MAJOR[0]}.{self.CHROME_VERSION_MAJOR[1]}.{self.CHROME_VERSION_MAJOR[1]}.{self.CHROME_VERSION_MOBILE}"
        else:
            platform = "Windows"
            edgeVersionString = f"{self.EDGE_VERSION_MAJOR[0]}.{self.EDGE_VERSION_MAJOR[1]}.{self.EDGE_VERSION_MAJOR[1]}.{self.CHROME_VERSION_PC}"
            chromeVersionString = f"{self.CHROME_VERSION_MAJOR[0]}.{self.CHROME_VERSION_MAJOR[1]}.{self.CHROME_VERSION_MAJOR[1]}.{self.CHROME_VERSION_PC}"
        
        cmd_args = {
            "userAgent": agentString,

            # DO NOT USE THE DATA BELOW. IT'S AN EXAMPLE AND IT DOESN'T MATCH THE USERAGENT ABOVE

            "userAgentMetadata": {
                "brands": [
                    {"brand": "Chromium", "version": self.CHROME_VERSION_MAJOR[0]},
                    {"brand": "Microsoft Edge", "version": self.EDGE_VERSION_MAJOR[0]},
                    {"brand": "Not;A=Brand", "version": "99"},
                ],
                "mobile": mobile,
                "model": "KB2003",
                "platform": platform,
                "platformVersion": "12.0.0",
                "fullVersion": edgeVersionString,
                "fullVersionList": [
                    {"brand": "Chromium", "version": chromeVersionString},
                    {"brand": "Microsoft Edge", "version": edgeVersionString},
                    {"brand": "Not;A=Brand", "version": "99.0.0.0"},
                ],
                "architecture": "",
                "bitness": "",
                "wow64": False,
            },
        }
        
        return cmd_args
