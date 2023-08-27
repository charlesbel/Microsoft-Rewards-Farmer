import logging

from src.browser import Browser

from .activities import Activities


class ShoppingGame:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.webdriver = browser.webdriver
        self.activities = Activities(browser)

    def completeShoppingGame(self):
        logging.info("[SHOPPING GAME] Trying to complete the Shopping Game...")
        self.webdriver.get(
            "https://www.msn.com/en-us/shopping?isembedded=1&disableheader=1"
        )

        # Max time should be 10(attempting to find game pane) + 10 * 10(Each game takes ~10 seconds) + 10 for whatever else happens
        self.webdriver.set_script_timeout(120)
        res = self.webdriver.execute_async_script(
            """const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
            let gamePane = null;
            let max_attempts = 100; // 10 seconds
            let attempts = 0;
            while (attempts != max_attempts && (!gamePane || !gamePane.displayedShoppingEntities)) {
                gamePane = document.querySelector('shopping-page-base')?.shadowRoot?.querySelector('shopping-homepage')?.shadowRoot?.querySelector('msft-feed-layout')?.shadowRoot?.querySelector('msn-shopping-game-pane');
                attempts++;
                await sleep(100);
            }

            if (!gamePane || !gamePane.shadowRoot) {
                return arguments[0]([0, "[SHOPPING GAME] Failed to get game element."]);
            }

            if (gamePane.shadowRoot.querySelector('.game-panel-max-tries')) {
                return arguments[0]([1, "[SHOPPING GAME] Already completed"]);
            }

            // Jump to gamePane, mainly for debugging. No technical use currently.
            window.scrollTo(0, gamePane.getBoundingClientRect().top)


            for (let i = 0; i < gamePane.gameSettings.dailyGamesLimit; i++) {
                await sleep(1000);
                let cheapest = gamePane.displayedShoppingEntities.sort((a, b) => parseFloat(a.priceInfo.price) < parseFloat(b.priceInfo.price))[0];
                let cheapestElem = gamePane.shadowRoot.querySelector(`msn-shopping-card[id="${cheapest.id}"]`);
                console.log(cheapest.priceInfo.price, gamePane.displayedShoppingEntities.map(x => x.priceInfo.price))
                
                // debugging, remove in prod
                if (!cheapestElem) {
                    console.log("Failed to get cheapest element...");
                    i--;
                    continue;
                }
                if (!cheapestElem.querySelector('.shopping-select-overlay-button')) {
                    console.log("Failed to get overlay button...");
                    i--;
                    continue;
                }

                cheapestElem.querySelector('.shopping-select-overlay-button').click();
                // Wait for `Play again` button to appear
                await sleep(1000);
                if (!gamePane.shadowRoot.querySelector('.game-panel-button')) {
                    console.log("Failed to get play again button...");
                    await sleep(50000);
                }
                gamePane.shadowRoot.querySelector('.game-panel-button').click()

                // Wait for play again delay(plus a bit) to complete
                await sleep(8000);
            }

            arguments[0]([3, "[SHOPPING GAME] Completed the Shopping Game successfully!"]);"""
        )

        if res[0] == 0:
            logging.error(res[1])
        elif res[0] == 1:
            logging.warning(res[1])
        elif res[0] == 2:
            logging.info(res[1])
