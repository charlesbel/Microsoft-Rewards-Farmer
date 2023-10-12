import random
from typing import Any

import requests
from requests import HTTPError, Response


class GenerateUserAgent:
    """A class for generating user agents for Microsoft Rewards Farmer."""

    # Reduced device name, ref: https://developer.chrome.com/blog/user-agent-reduction-android-model-and-version/
    MOBILE_DEVICE = "K"

    USER_AGENT_TEMPLATES = {
        "edge_pc": (
            "Mozilla/5.0"
            " ({system}) AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/{app[chrome_reduced_version]} Safari/537.36"
            " Edg/{app[edge_version]}"
        ),
        "edge_mobile": (
            "Mozilla/5.0"
            " ({system}) AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/{app[chrome_reduced_version]} Mobile Safari/537.36"
            " EdgA/{app[edge_version]}"
        ),
    }

    OS_PLATFORMS = {"win": "Windows NT 10.0", "android": "Linux"}
    OS_CPUS = {"win": "Win64; x64", "android": "Android 13"}

    def userAgent(
        self,
        browserConfig: dict[str, Any],
        mobile: bool = False,
    ) -> tuple[str, dict[str, Any], Any]:
        """
        Generates a user agent string for either a mobile or PC device.

        Args:
            mobile: A boolean indicating whether the user agent should be generated for a mobile device.

        Returns:
            A string containing the user agent for the specified device.
        """

        system = self.getSystemComponents(mobile)
        app = self.getAppComponents(mobile)
        uaTemplate = (
            self.USER_AGENT_TEMPLATES.get("edge_mobile", "")
            if mobile
            else self.USER_AGENT_TEMPLATES.get("edge_pc", "")
        )

        newBrowserConfig = None
        if userAgentMetadata := browserConfig.get("userAgentMetadata"):
            platformVersion = userAgentMetadata["platformVersion"]

        else:
            # ref : https://textslashplain.com/2021/09/21/determining-os-platform-version/
            platformVersion = (
                f"{random.randint(9,13) if mobile else random.randint(1,15)}.0.0"
            )
            newBrowserConfig = browserConfig
            newBrowserConfig["userAgentMetadata"] = {
                "platformVersion": platformVersion,
            }
        uaMetadata = {
            "mobile": mobile,
            "platform": "Android" if mobile else "Windows",
            "fullVersionList": [
                {"brand": "Not/A)Brand", "version": "99.0.0.0"},
                {"brand": "Microsoft Edge", "version": app["edge_version"]},
                {"brand": "Chromium", "version": app["chrome_version"]},
            ],
            "brands": [
                {"brand": "Not/A)Brand", "version": "99"},
                {"brand": "Microsoft Edge", "version": app["edge_major_version"]},
                {"brand": "Chromium", "version": app["chrome_major_version"]},
            ],
            "platformVersion": platformVersion,
            "architecture": "" if mobile else "x86",
            "bitness": "" if mobile else "64",
            "model": "",
        }

        return uaTemplate.format(system=system, app=app), uaMetadata, newBrowserConfig

    def getSystemComponents(self, mobile: bool) -> str:
        """
        Generates the system components for the user agent string.

        Args:
            mobile: A boolean indicating whether the user agent should be generated for a mobile device.

        Returns:
            A string containing the system components for the user agent string.
        """
        osId = self.OS_CPUS.get("android") if mobile else self.OS_CPUS.get("win")
        uaPlatform = (
            self.OS_PLATFORMS.get("android") if mobile else self.OS_PLATFORMS.get("win")
        )
        if mobile:
            osId = f"{osId}; {self.MOBILE_DEVICE}"
        return f"{uaPlatform}; {osId}"

    def getAppComponents(self, mobile: bool) -> dict[str, str]:
        """
        Generates the application components for the user agent string.

        Returns:
            A dictionary containing the application components for the user agent string.
        """
        edgeWindowsVersion, edgeAndroidVersion = self.getEdgeVersions()
        edgeVersion = edgeAndroidVersion if mobile else edgeWindowsVersion
        edgeMajorVersion = edgeVersion.split(".")[0]

        chromeVersion = self.getChromeVersion()
        chromeMajorVersion = chromeVersion.split(".")[0]
        chromeReducedVersion = f"{chromeMajorVersion}.0.0.0"

        return {
            "edge_version": edgeVersion,
            "edge_major_version": edgeMajorVersion,
            "chrome_version": chromeVersion,
            "chrome_major_version": chromeMajorVersion,
            "chrome_reduced_version": chromeReducedVersion,
        }

    def getEdgeVersions(self) -> tuple[str, str]:
        """
        Get the latest version of Microsoft Edge.

        Returns:
            str: The latest version of Microsoft Edge.
        """
        response = self.getWebdriverPage(
            "https://edgeupdates.microsoft.com/api/products"
        )
        data = response.json()
        if stableProduct := next(
            (product for product in data if product["Product"] == "Stable"),
            None,
        ):
            releases = stableProduct["Releases"]
            androidRelease = next(
                (release for release in releases if release["Platform"] == "Android"),
                None,
            )
            windowsRelease = next(
                (
                    release
                    for release in releases
                    if release["Platform"] == "Windows"
                    and release["Architecture"] == "x64"
                ),
                None,
            )
            if androidRelease and windowsRelease:
                return (
                    windowsRelease["ProductVersion"],
                    androidRelease["ProductVersion"],
                )
        raise HTTPError("Failed to get Edge versions.")

    def getChromeVersion(self) -> str:
        """
        Get the latest version of Google Chrome.

        Returns:
            str: The latest version of Google Chrome.
        """
        response = self.getWebdriverPage(
            "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json"
        )
        data = response.json()
        return data["channels"]["Stable"]["version"]

    @staticmethod
    def getWebdriverPage(url: str) -> Response:
        response = None
        response = requests.get(url)
        if response.status_code != requests.codes.ok:  # pylint: disable=no-member
            raise HTTPError(
                f"Failed to get webdriver page {url}. "
                f"Status code: {response.status_code}"
            )
        return response
