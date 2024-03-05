# fillDatabase.py
# By: Sam Schmitz, Gavin Roy
# fills the database

import sqlite3
from datetime import datetime, timedelta, date

from congressTrades import getTrades
from server import stockBotAPI

def fill(date):
    trades = getTrades(date)
    api = stockBotAPI
    for t in trades:
        api.add_trade(t)

if __name__ == "__main__":
    #d1 = date(2024, 5, 3)
    #d2 = date(2024, 5, 3)-timedelta(days=5)
    #fill(datetime(d1.year, d1.month, d1.day), datetime(d2.year, d2.month, d2.day))
    d = date.today()-timedelta(days=3)
    fill(datetime(d.year, d.month, d.day))
    #print(d2)
