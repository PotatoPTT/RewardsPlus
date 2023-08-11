import random
import time

from src.browser import Browser
from src.utils import prGreen, prRed

SHOPPING_RIGHT = 0
SHOPPING_ATTEMPT = 0
MAX_SHOPPING_ATTEMPT = 10


class Shopping:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.webdriver = browser.webdriver

    def completeShoppingQuiz(self):
        print("[SHOP] Trying to complete Shopping...")
        try:
            while (
                SHOPPING_ATTEMPT < MAX_SHOPPING_ATTEMPT and SHOPPING_RIGHT < 10
            ):  # SHOPPING_ATTEMPT
                self.shoppingQuiz()
            prGreen("[SHOP] Completed Shopping successfully !")
        except Exception as e:
            prRed("[SHOP] Something exploded !")
            print(e)
            pass
        time.sleep(random.randint(10, 15))
        return SHOPPING_RIGHT

    def shoppingQuiz(self):
        global SHOPPING_RIGHT
        global MAX_SHOPPING_ATTEMPT
        global SHOPPING_ATTEMPT

        self.webdriver.get("https://www.msn.com/en-us/shopping")
        time.sleep(10)
        for j in range(1, 8):
            height = 1000 * j
            self.webdriver.execute_script(f"window.scrollTo(0, {height});")
            time.sleep(2)
        numbers = [670, 920, 1170]

        self.webdriver.execute_script(
            """var msnShoppingGamePane = document.querySelector("shopping-page-base")
            ?.shadowRoot.querySelector("shopping-homepage")
            ?.shadowRoot.querySelector("msft-feed-layout")
            ?.shadowRoot.querySelector("msn-shopping-game-pane");
            if (msnShoppingGamePane != null) {
            msnShoppingGamePane.scrollIntoView({behavior: 'smooth'});
            msnShoppingGamePane.stopCardsAnimation = true; }"""
        )
        time.sleep(1)
        time.sleep(1)
        if (
            self.webdriver.execute_script(
                'return document.querySelector("#root > div > div > fluent-design-system-provider > div > div:nth-child(4) > div > shopping-page-base").shadowRoot.querySelector("div > div.shopping-page-content > shopping-homepage").shadowRoot.querySelector("div > msft-feed-layout").shadowRoot.querySelector("msn-shopping-game-pane").gameState'
            )
            == "idle"
        ):
            print("[SHOP] Shopping already done!")
            SHOPPING_ATTEMPT = MAX_SHOPPING_ATTEMPT
            return
        self.webdriver.execute_script(
            """var msnShoppingGamePane = document.querySelector("shopping-page-base")
            ?.shadowRoot.querySelector("shopping-homepage")
            ?.shadowRoot.querySelector("msft-feed-layout")
            ?.shadowRoot.querySelector("msn-shopping-game-pane");
            if (msnShoppingGamePane != null) {
            msnShoppingGamePane.scrollIntoView({behavior: 'smooth'});
            msnShoppingGamePane.stopCardsAnimation = true; }"""
        )
        time.sleep(10)
        # for loop was here
        for i in range(SHOPPING_ATTEMPT, MAX_SHOPPING_ATTEMPT):
            SHOPPING_ATTEMPT += 1
            selectedIndex = random.randint(0, 2)
            selectedNumber = numbers[selectedIndex]
            if (
                self.webdriver.execute_script(
                    'return document.querySelector("#root > div > div > fluent-design-system-provider > div > div:nth-child(4) > div > shopping-page-base").shadowRoot.querySelector("div > div.shopping-page-content > shopping-homepage").shadowRoot.querySelector("div > msft-feed-layout").shadowRoot.querySelector("msn-shopping-game-pane").gameState'
                )
                == "lose"
            ):
                prRed("[SHOP] Something gone wrong!")
                return
            self.clickXY(selectedNumber, 200)  # 670, 920, 1170
            time.sleep(2)
            self.webdriver.save_screenshot(
                f"./database/shopping/screenshots/{SHOPPING_ATTEMPT}screenshot.png"
            )
            if (
                self.webdriver.execute_script(
                    'return document.querySelector("#root > div > div > fluent-design-system-provider > div > div:nth-child(4) > div > shopping-page-base").shadowRoot.querySelector("div > div.shopping-page-content > shopping-homepage").shadowRoot.querySelector("div > msft-feed-layout").shadowRoot.querySelector("msn-shopping-game-pane").gameState'
                )
                == "win"
            ):
                SHOPPING_RIGHT += 1
                print(
                    f"[SHOP] Shopping Attempt {SHOPPING_ATTEMPT}: It got one! {SHOPPING_RIGHT}/10"
                )
                self.webdriver.execute_script(
                    """var msnShoppingGamePane = document.querySelector("shopping-page-base")
                    ?.shadowRoot.querySelector("shopping-homepage")
                    ?.shadowRoot.querySelector("msft-feed-layout")
                    ?.shadowRoot.querySelector("msn-shopping-game-pane");
                    if (msnShoppingGamePane != null) {
                    msnShoppingGamePane.scrollIntoView({behavior: 'smooth'});
                    msnShoppingGamePane.stopCardsAnimation = true; }"""
                )
                time.sleep(2)
                return
            elif (
                self.webdriver.execute_script(
                    'return document.querySelector("#root > div > div > fluent-design-system-provider > div > div:nth-child(4) > div > shopping-page-base").shadowRoot.querySelector("div > div.shopping-page-content > shopping-homepage").shadowRoot.querySelector("div > msft-feed-layout").shadowRoot.querySelector("msn-shopping-game-pane").gameState'
                )
                == "idle"
            ):
                print("[SHOP] Shopping already done!")
                SHOPPING_ATTEMPT = MAX_SHOPPING_ATTEMPT
                return
            else:
                print(
                    f"[SHOP] Shopping Attempt {SHOPPING_ATTEMPT}: {SHOPPING_RIGHT}/10"
                )
            time.sleep(10)

    def clickXY(self, x, y, delay=True):
        from selenium.webdriver.common.action_chains import ActionChains

        actions = ActionChains(self.webdriver)
        actions.move_by_offset(x, y)
        if delay:
            time.sleep(0.5)
        actions.click().perform()
        actions.move_by_offset(-x, -y).perform()
