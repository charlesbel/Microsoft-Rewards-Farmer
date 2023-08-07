from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from src import Discord
from src.constants import BASE_URL
from src.utils import prGreen, prRed, prYellow


class Redeem:
    def auto_redeem(self, email, total, webhook):        
        prGreen(f"[REDEEM] Attempting to auto redeem rewards...")

        # go to the main rewards page
        self.webdriver.get(BASE_URL)

        notEnoughPoints = False
        try:
            # check if the set goal btn is there.
            # if true, account hasn't set a goal yet to auto redeem
            print(10)
            element = WebDriverWait(self.webdriver, 10).until(
                ec.element_to_be_clickable((By.ID, "goalSet"))
            )
            print(8)
            prRed(
                f"[REDEEM] {email} doesn't have a set goal. Couldn't redeem anything. "
            )

            return
        except TimeoutException:
            try:
                # wait for remove goal button first
                element = WebDriverWait(self.webdriver, 10).until(
                    ec.element_to_be_clickable((By.ID, "removeGoal"))
                )
                # if failed, buttons couldn't be loaded
                print(6)
                # Wait for the redeem button to be there
                notEnoughPoints = True
                element = WebDriverWait(self.webdriver, 10).until(
                    ec.element_to_be_clickable((By.ID, "redeemNow"))
                )
                # if failed, account doesn't have enough points to redeem their goal
                notEnoughPoints = False
                print(5)
                # go to the redeem page of the reward
                element.click()

                # get the number for the thing being bought
                url_parts = self.webdriver.current_url.split('/')
                number = url_parts[url_parts.index("redeem") + 1].split('?')[0]

                element = WebDriverWait(self.webdriver, 10).until(
                    ec.element_to_be_clickable((By.ID, f"redeem-pdp_{number}-cloned"))
                )
                print(4)
                # clicking redeem on the reward page
                element.click()

                # get the last redeeming button
                element = WebDriverWait(self.webdriver, 10).until(
                    ec.element_to_be_clickable((By.ID, "redeem-checkout-review-confirm"))
                )
                print(1)
                # get the text to send back for statistics
                pointsText = self.webdriver.find_element(By.CSS_SELECTOR, ".text-body.margin-top-8.spacer-32-bottom")
                thingRedeeming = pointsText.find_element(By.XPATH, "./preceding-sibling::*[1]")

                points = pointsText.get_attribute('innerHTML').rstrip().replace('\n', '')
                thing = thingRedeeming.get_attribute('innerHTML')
                print(2)

                # last redeem button
                element.click()

                prGreen(f"[REDEEM] {email} has redeemed {thing} for {points}.")
                print(3)
                
                if webhook:
                    Discord.send_to_webhook(f"`{email}` has redeemed {thing} for {points}.")

            except TimeoutException:
                if notEnoughPoints:
                    prYellow(
                        f"[REDEEM] {email} doesn't have enough points to auto redeem. Skipping."
                    )
                    return
                
                # all buttons couldn't load for some reason
                prRed(f"[REDEEM] Timed out on redeeming buttons for {email}")
