# fillDatabase.py
# By: Sam Schmitz, Gavin Roy
# fills the database

import sqlite3
from datetime import datetime, timedelta, date

from congressTrades import get_trades_d_to_d
from server import stockBotAPI

def fill(d1, d2):
    trades = get_trades_d_to_d(d1, d2)
    sba = stockBotAPI()
    for t in trades:
        sba.add_trade(trade=t)
    sba.close()
    return trades
        
if __name__ == "__main__":
    #filled with (2024, 3, 21) - (2024, 3, 14)
    d1 = date(2024, 3, 13)
    #d1 = date.today()
    d2 = d1 - timedelta(days=3)
    data = fill(datetime(d1.year, d1.month, d1.day), datetime(d2.year, d2.month, d2.day))
    for trade in data:
        print(trade.tick, trade.member, trade.dateD)
    #d = date.today()-timedelta(days=3)
    #fill(datetime(d.year, d.month, d.day))
    print(d2)
    #fill_members()
