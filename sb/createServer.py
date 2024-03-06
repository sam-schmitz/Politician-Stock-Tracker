# createServer.py
# By: Sam Schmitz, Gavin Roy
# creates the database to be used by server.py

import sqlite3
from os import path

if __name__ == "__main__":
    conn = sqlite3.connect("sbDatabase.db")
    cursor = conn.cursor()
    

    cursor.execute(''' CREATE TABLE IF NOT EXISTS trades
                   (tradeID INTEGER PRIMARY KEY, stockID INTEGER FORGEIN KEY,
                   buySell TEXT, memberID INTEGER FORGEIN KEY,
                   dateBought TEXT, priceBought INTEGER, dateDisclosed
                   TEXT, priceDisclosed INTEGER, Delay INTEGER, Crossover
                   TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS members
                   (memberID INTEGER PRIMARY KEY, comittees TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS stocks
                   (stockID INTEGER PRIMARY KEY, tick TEXT, sector TEXT,
                   industry TEXT, companyName TEXT)''')
    conn.commit()
    
    print(conn.total_changes)
