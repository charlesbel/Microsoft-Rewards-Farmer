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
    browser_versions: dict[str, Any] = {}

    def generate_user_agent(self) -> dict[str, str]:
        """
        Generates a dictionary containing user agents for both mobile and PC devices.

        Returns:
            A dictionary containing user agents for both mobile and PC devices.
        """
        return {
            "Mobile": self.user_agent(mobile=True),
            "PC": self.user_agent(mobile=False),
        }

    def user_agent(
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

        system = self.__get_system_components(mobile)
        app = self.__get_app_components(mobile, fetch)
        ua_template = (
            self.USER_AGENT_TEMPLATE.get("edge_mobile", "")
            if mobile
            else self.USER_AGENT_TEMPLATE.get("edge_pc", "")
        )

        return ua_template.format(system=system, app=app)

    def __get_system_components(self, mobile: bool) -> str:
        """
        Generates the system components for the user agent string.

        Args:
            mobile: A boolean indicating whether the user agent should be generated for a mobile device.

        Returns:
            A string containing the system components for the user agent string.
        """
        os_id = self.OS_CPU.get("android") if mobile else self.OS_CPU.get("win")
        ua_platform = (
            self.OS_PLATFORM.get("android") if mobile else self.OS_PLATFORM.get("win")
        )
        if mobile:
            os_id = f"{os_id}; {self.MOBILE_DEVICE}"
        return f"{ua_platform}; {os_id}"

    def __get_app_components(self, mobile: bool, fetch: bool) -> dict[str, Any]:
        """
        Generates the application components for the user agent string.

        Args:
            mobile: A boolean indicating whether the user agent should be generated for a mobile device.
            fetch: A boolean indicating whether to fetch the latest browser versions.

        Returns:
            A dictionary containing the application components for the user agent string.
        """
        chrome_minor_version = (
            self.CHROME_VERSION_MOBILE if mobile else self.CHROME_VERSION_PC
        )
        chrome_version = self.__generate_version(
            self.CHROME_VERSION_MAJOR, chrome_minor_version
        )

        edge_minor_version = (
            self.EDGE_VERSION_MOBILE if mobile else self.EDGE_VERSION_PC
        )
        edge_version = self.__generate_version(
            self.EDGE_VERSION_MAJOR, edge_minor_version
        )
        if fetch and not self.grabbed:
            try:
                fetched_edge_version = self.get_edge_version()
                # TODO: Add a logger to increase verbosity
                # if fetched_edge_version != edge_version:
                #     log_msg = (
                #         f"Fetched Edge version {fetched_edge_version} "
                #         f"is different from the expected {edge_version}"
                #     )
                #     logger.trace(log_msg)
                fetched_chrome_version = self.get_chrome_version()
                # if fetched_chrome_version != chrome_version:
                #     log_msg = (
                #         f"Fetched Chrome version {fetched_chrome_version} "
                #         f"is different from the expected {chrome_version}"
                #     )
                #     logger.trace(log_msg)
                self.browser_versions = {
                    "chrome_version": fetched_chrome_version,
                    "edge_version": fetched_edge_version,
                }
                self.grabbed = True
            except Exception:  # pylint: disable=broad-except
                print("Failed to get webdriver version.")
                # logger.warning("Failed to get webdriver version.")
        if not self.browser_versions:
            self.browser_versions = {
                "chrome_version": chrome_version,
                "edge_version": edge_version,
            }
        return self.browser_versions

    @staticmethod
    def __generate_version(major: list[str], minor: str) -> str:
        """
        Generate a version.

        Args:
            major (list[str]): A list of three strings representing the major version.
            minor (str): A string representing the minor version.

        Returns:
            str: A string representing the generated version.
        """
        return f"{major[0]}.{major[1]}.{major[2]}.{minor}"

    def get_chrome_version(self) -> str:
        """
        Get the latest version of Chrome.

        Returns:
            str: The latest version of Chrome.
        """
        latest_release_url = (
            "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        )
        return self.get_webdriver_page(latest_release_url).text

    def get_edge_version(self) -> str:
        """
        Get the latest version of Microsoft Edge.

        Returns:
            str: The latest version of Microsoft Edge.
        """
        edge_release_url = (
            "https://msedgewebdriverstorage.blob.core.windows.net"
            "/edgewebdriver/LATEST_STABLE"
        )
        response = self.get_webdriver_page(edge_release_url)
        return response.content.decode("utf-16").split("\r")[0].split("\n")[0]

    @staticmethod
    def get_webdriver_page(url: str) -> Response:
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
