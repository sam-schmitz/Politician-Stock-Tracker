# fillDatabase.py
# By: Sam Schmitz, Gavin Roy
# fills the database

import sqlite3
from datetime import datetime, timedelta, date

from congressTrades import get_trades_d_to_d
from server import stockBotAPI

def fill(d1, d2):
    sba = stockBotAPI()
    _check_dates(d1, d2, sba)
    trades = get_trades_d_to_d(d1, d2)
    for t in trades:
        sba.add_trade(trade=t)
    sba.close()
    return trades

def _check_dates(d1, d2, api):
    if isinstance(d1, datetime) == False:
        raise TypeError("d1 should be a date or datetime object")
    if isinstance(d2, datetime)==False:
        raise TypeError("d2 should be a date or datetime object")
    nd = api.get_newest_date()
    od = api.get_oldest_date()
    newD = date(nd.year, nd.month, nd.day) + timedelta(days=1)
    oldD = date(od.year, od.month, od.day) - timedelta(days=1)
    d1 = date(d1.year, d1.month, d1.day)
    d2 = date(d2.year, d2.month, d2.day)
    if d1 < d2:
        raise KeyError("d2 is before than d1")
    if d1!=oldD and d2!=newD:
        raise KeyError(f"The data from {nd} to {od} is already in the table. Please select a date that borders this range.")
    if d1 > date.today():
        raise KeyError("d1 is earlier than today")
    
        
if __name__ == "__main__":
    #filled with (2024, 3, 26) - (2024, 3, 14)
    d1 = date(2024, 3, 26)
    #d1 = '2024-03-13'
    #d1 = date.today()
    #d2 = d1 - timedelta(days=3)
    #d2 = 20240313
    d2 = date(2024, 3, 22)
    #data = fill(d1, d2)
    data = fill(datetime(d1.year, d1.month, d1.day), datetime(d2.year, d2.month, d2.day))
    for trade in data:
        print(trade.tick, trade.member, trade.dateD)
    #d = date.today()-timedelta(days=3)
    #fill(datetime(d.year, d.month, d.day))
    print(d2)
    #fill_members()
