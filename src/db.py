import json
import time
from datetime import datetime
import os

import mysql.connector
import pytz

from src.utils import prRed


class DataBase:
    def __init__(self):
        self.mydb = self.connectDB()

    def insertPoints(self, POINTS_COUNTER, SHOPPING_RIGHT):
        if self.mydb is None:
            prRed("No database connection.")
            return

        mycursor = self.createCursor()
        if mycursor is None:
            return

        mycursor = self.createCursor()
        if mycursor is None:
            return False

        now = datetime.now(tz=pytz.timezone("America/Sao_Paulo"))
        if self.existInDatabase("points", "date", self.getDate()) and now.hour <= 17:
            sql = "UPDATE `points` SET `pointsQuantity` = %s, `shoppingRight` = %s WHERE `points`.`date` = %s"
            data = (POINTS_COUNTER, SHOPPING_RIGHT, self.getDate())
        elif now.hour >= 12:
            sql = "INSERT INTO `points` (`date`, `pointsQuantity`, `shoppingRight`) VALUES (%s, %s, %s)"
            data = (self.getDate(), POINTS_COUNTER, SHOPPING_RIGHT)
        else:
            return
        try:
            mycursor.execute(sql, data)
            self.mydb.commit()
        except Exception as e:
            print(e)
            return
        finally:
            mycursor.close()

    def existInDatabase(self, database, column, name):
        mycursor = self.createCursor()
        if mycursor is None:
            return False
        sql = f"SELECT * FROM {database} WHERE {column} = %s"
        data = (name,)
        mycursor.execute(sql, data)
        if mycursor.fetchone() is None:
            return False
        else:
            return True

    def createCursor(self, attempts=5, delay=5):
        if self.mydb is None:
            prRed("No database connection.")
            return
        for attempt in range(attempts):
            try:
                cursor = self.mydb.cursor()
                return cursor

            except Exception as e:
                print(e)
                time.sleep(delay)
        return None

    def connectDB(self):
        try:
            return mysql.connector.connect(
                host=self.getConfig("databaseIP"),
                port=self.getConfig("databasePort"),
                user=self.getConfig("databaseUser"),
                password=self.getConfig("databasePassword"),
                database=self.getConfig("database"),
            )
        except Exception as e:
            print(e)
            return None

    def getConfig(self, config):
        try:
            scriptDir = os.path.dirname(os.path.abspath(__file__))
            configPath = os.path.join(scriptDir, "../database/config.json")
            with open(configPath, "r") as file:
                aux = json.load(file)
                return aux.get(config)
        except Exception as e:
            print(e)
            return False

    def getDate(self):
        import pytz

        data_atual = datetime.now(tz=pytz.timezone("America/Sao_Paulo"))
        return data_atual.strftime("%Y-%m-%d")

    def updatePoints(self, POINTS_COUNTER, SHOPPING_RIGHT):
        if self.mydb is None:
            prRed("No database connection.")
            return
        self.mydb = self.connectDB()
        if self.mydb is None:
            prRed("No database connection.")
            return
        self.insertPoints(POINTS_COUNTER, SHOPPING_RIGHT)
        self.mydb.close()
