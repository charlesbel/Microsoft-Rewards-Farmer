""" This module contains the Searches class, which is used to perform searches on Bing. """

import contextlib
import json
import random
import time
from datetime import date, timedelta

import requests
from selenium.common.exceptions import (
    NoAlertPresentException,
    UnexpectedAlertPresentException,
)
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from lib.utils import Utils

from .constants import DESKTOP_USER_AGENT


class Searches:
    """This class is used to perform searches on Bing and retrieve Google Trends data."""

    def __init__(self, browser: WebDriver, lang: str, geo: str):
        self.browser = browser
        self.utils = Utils(browser)
        self.lang = lang
        self.geo = geo

    def get_google_trends(self, words_count: int) -> list[str]:
        """
        Retrieves a list of trending search terms from Google Trends API.

        Args:
            words_count (int): The number of search terms to retrieve.

        Returns:
            list[str]: A list of search terms.
        """
        search_terms: list[str] = []
        i = 0
        while len(search_terms) < words_count:
            i += 1
            trends_response = requests.get(
                f"https://trends.google.com/trends/api/dailytrends?hl={self.lang}&ed="
                f'{(date.today() - timedelta(days=i)).strftime("%Y%m%d")}&geo={self.geo}&ns=15',
                timeout=10,
            )
            trends = json.loads(trends_response.text[6:])
            for topic in trends["default"]["trendingSearchesDays"][0][
                "trendingSearches"
            ]:
                search_terms.append(topic["title"]["query"].lower())
                search_terms.extend(
                    relatedTopic["query"].lower()
                    for relatedTopic in topic["relatedQueries"]
                )
            search_terms = list(set(search_terms))
        del search_terms[words_count : (len(search_terms) + 1)]
        return search_terms

    def get_related_terms(self, word: str) -> list[str]:
        """
        Retrieves a list of related search terms for a given search term from Bing.

        Args:
            word (str): The search term to retrieve related terms for.

        Returns:
            list[str]: A list of related search terms.
        """
        try:
            related_response = requests.get(
                f"https://api.bing.com/osjson.aspx?query={word}",
                headers={"User-agent": DESKTOP_USER_AGENT},
                timeout=10,
            )
            return related_response.json()[1]
        except Exception:
            return []

    def bing_searches(
        self, number_of_searches: int, is_mobile: bool = False, poinst_counter: int = 0
    ):
        """
        Performs a given number of Bing searches using search terms retrieved from Google Trends.

        Args:
            number_of_searches (int): The number of searches to perform.
            is_mobile (bool, optional): Is a mobile device. Defaults to False.
            poinst_counter (int, optional): The current points count. Defaults to 0.

        Returns:
            int: The updated points count after performing the searches.
        """
        i = 0
        search_terms = self.get_google_trends(number_of_searches)
        for word in search_terms:
            i += 1
            print("[BING]", f"{i}/{number_of_searches}")
            points = self.bing_search(word, is_mobile)
            if points <= poinst_counter:
                related_terms = self.get_related_terms(word)[:2]
                for term in related_terms:
                    points = self.bing_search(term, is_mobile)
                    if not points <= poinst_counter:
                        break
            if points > 0:
                poinst_counter = points
            else:
                break
        return poinst_counter

    def bing_search(self, word: str, is_mobile: bool):
        """
        Performs a Bing search for the given word and returns
        the number of Microsoft Rewards points earned.

        Args:
            word (str): The search term to use.
            is_mobile (bool): Whether to use the mobile version of Bing.

        Returns:
            int: The number of Microsoft Rewards points earned from the search.
        """
        self.browser.get("https://bing.com")
        self.utils.wait_until_clickable(By.ID, "sb_form_q")
        searchbar = self.browser.find_element(By.ID, "sb_form_q")
        searchbar.send_keys(word)
        searchbar.submit()
        time.sleep(random.randint(10, 15))
        string_points = None
        with contextlib.suppress(Exception):
            if not is_mobile:
                string_points = self.browser.find_element(By.ID, "id_rc").get_attribute(
                    "innerHTML"
                )

            else:
                try:
                    self.browser.find_element(By.ID, "mHamburger").click()
                    time.sleep(1)
                except UnexpectedAlertPresentException:
                    with contextlib.suppress(NoAlertPresentException):
                        self.browser.switch_to.alert.accept()
                        self.browser.find_element(By.ID, "mHamburger").click()
                string_points = self.browser.find_element(
                    By.ID, "fly_id_rc"
                ).get_attribute("innerHTML")
        return int(string_points) if string_points is not None else 0
