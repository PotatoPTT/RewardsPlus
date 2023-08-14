import argparse
import json
import os
import random
import time
from datetime import date, datetime
from pathlib import Path

from src import (
    Browser,
    DailySet,
    DataBase,
    Login,
    MorePromotions,
    PunchCards,
    Searches,
    Shopping,
)
from src.constants import VERSION
from src.utils import prGreen, prPurple, prRed, prYellow

POINTS_COUNTER = 0
USA = False
USEDB = True


def main():
    loadedAccounts = setupAccounts()
    executeBot(loadedAccounts)


def argumentParser():
    parser = argparse.ArgumentParser(description="Microsoft Rewards Farmer")
    parser.add_argument(
        "-v", "--visible", action="store_true", help="Optional: Visible browser"
    )
    parser.add_argument(
        "-l", "--lang", type=str, default=None, help="Optional: Language (ex: en)"
    )
    parser.add_argument(
        "-g", "--geo", type=str, default=None, help="Optional: Geolocation (ex: US)"
    )
    return parser.parse_args()


def bannerDisplay():
    farmerBanner = """
    ███╗   ███╗███████╗    ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗██████╗
    ████╗ ████║██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗
    ██╔████╔██║███████╗    █████╗  ███████║██████╔╝██╔████╔██║█████╗  ██████╔╝
    ██║╚██╔╝██║╚════██║    ██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║██╔══╝  ██╔══██╗
    ██║ ╚═╝ ██║███████║    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
    ╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝"""
    prRed(farmerBanner)
    prPurple(f"        by Charles Bel (@charlesbel) MOD BY:PTT    version {VERSION}\n")


def setupAccounts() -> dict:
    accountPath = Path(__file__).resolve().parent / "database/accounts.json"
    if not accountPath.exists():
        accountPath.write_text(
            json.dumps(
                [{"username": "Your Email", "password": "Your Password"}], indent=4
            ),
            encoding="utf-8",
        )
        noAccountsNotice = """
    [ACCOUNT] Accounts credential file "accounts.json" not found.
    [ACCOUNT] A new file has been created, please edit with your credentials and save.
    """
        prPurple(noAccountsNotice)
        exit()
    loadedAccounts = json.loads(accountPath.read_text(encoding="utf-8"))
    random.shuffle(loadedAccounts)
    return loadedAccounts


def executeBot(loadedAccounts):
    for currentAccount in loadedAccounts:
        prYellow(
            "********************{ "
            + currentAccount.get("username", "")
            + " }********************"
        )
        with Browser(
            mobile=False, account=currentAccount, args=argumentParser()
        ) as desktopBrowser:
            accountPointsCounter = Login(desktopBrowser).login()
            shoppingRight = 0
            startingPoints = accountPointsCounter
            prGreen(
                f"[POINTS] You have {desktopBrowser.utils.formatNumber(accountPointsCounter, num_decimals=0)} points on your account !"
            )
            if USA:
                DailySet(desktopBrowser).completeDailySet()
                PunchCards(desktopBrowser).completePunchCards()
            MorePromotions(desktopBrowser).completeMorePromotions()
            shoppingRight = Shopping(desktopBrowser).completeShoppingQuiz()

            (
                remainingSearches,
                remainingSearchesM,
            ) = desktopBrowser.utils.getRemainingSearches()
            if remainingSearches != 0:
                accountPointsCounter = Searches(desktopBrowser).bingSearches(
                    remainingSearches
                )

            if remainingSearchesM != 0:
                desktopBrowser.closeBrowser()
                sleep = random.randint(120, 200)
                print(f"[SLEEP] Sleeping for {sleep} seconds")
                time.sleep(sleep)
                with Browser(
                    mobile=True, account=currentAccount, args=argumentParser()
                ) as mobileBrowser:
                    accountPointsCounter = Login(mobileBrowser).login()
                    accountPointsCounter = Searches(mobileBrowser).bingSearches(
                        remainingSearchesM
                    )

            prGreen(
                f"[POINTS] You have earned {desktopBrowser.utils.formatNumber(accountPointsCounter - startingPoints, num_decimals=0)} points today !"
            )
            if USEDB:
                DataBase().updatePoints(accountPointsCounter, shoppingRight)
            prGreen(
                f"[POINTS] You are now at {desktopBrowser.utils.formatNumber(accountPointsCounter, num_decimals=0)} points !\n"
            )


def check_file_exists():
    today = date.today()
    date_format = today.strftime("%Y-%m-%d")
    if os.path.exists(f"{date_format}.date"):
        print("Already Done!")
        exit()


def create_and_delete_files():
    import pytz

    now = datetime.now(tz=pytz.timezone("America/Sao_Paulo"))
    if now.hour < 14:
        return
    today = date.today()
    date_format = today.strftime("%Y-%m-%d")
    with open(f"{date_format}.date", "w") as file:
        file.write("OH MY GAH")
    files = os.listdir()
    for file_name in files:
        if file_name.endswith(".date") and file_name != f"{date_format}.date":
            os.remove(file_name)


if __name__ == "__main__":
    main()
