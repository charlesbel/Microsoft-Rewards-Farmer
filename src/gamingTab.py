import logging
import time

from src.browser import Browser


class GamingTab:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.webdriver = browser.webdriver

    def completeGamingTab(self):
        logging.info("[GAMING TAB] Trying to complete Gaming Tab...")
        self.webdriver.get("https://www.msn.com/en-us")
        gamingBtn = self.browser.utils.waitUntilJS(
            """return document.querySelector('entry-point')?.
            shadowRoot?.querySelector('feed-navigation-hp')?.
            shadowRoot?.querySelector('feed-navigation')?.
            shadowRoot?.querySelector('feed-navigation-item#esports')?.
            shadowRoot?.querySelector('a');"""
        )

        if not gamingBtn:
            logging.error("[GAMING TAB] Failed to load page correctly.")
            return

        time.sleep(5)
        # I couldn't get clicking that button to work. I don't know why. It works in JS, but not in python
        self.webdriver.execute_script(
            "window.navigation.navigate('https://www.msn.com/en-us/gaming/feed')"
        )

        rewardsCard = self.browser.utils.waitUntilJS(
            """return document.querySelector('gaming-page')?.
            shadowRoot?.querySelector('feed-container')?.
            shadowRoot?.querySelector('grid-view-feed')?.
            shadowRoot?.querySelector('cs-super-container')?.
            shadowRoot?.querySelector('cs-personalized-feed')?.
            shadowRoot?.querySelector('cs-feed-layout')?.
            shadowRoot?.querySelector('gaming-rewards-card')"""
        )
        if not rewardsCard:
            # This occurs does not have the gaming tab rewrads card enabled on their account
            logging.error("[GAMING TAB] Failed to get rewards card")
            return

        time.sleep(5)
        self.webdriver.execute_script("arguments[0].rewardsTriggered()", rewardsCard)

        self.browser.utils.resetTabs()

        logging.info("[GAMING TAB] Completed Gaming Tab successfully!")
