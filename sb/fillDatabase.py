# fillDatabase.py
# By: Sam Schmitz, Gavin Roy
# fills the database

import sqlite3
from datetime import datetime, timedelta, date

from congressTrades import get_trades_d_to_d
from server import stockBotAPI

def fill(d1, d2):
    trades = get_trades_d_to_d(d1, d2)
    """sba = stockBotAPI()
    for t in trades:
        sba.add_trade(trade=t)
    sba.close()"""
    return trades
        
def fill_members():
    #Only adds member names 
        #need to get member commitees/relevent sectors
    sba = stockBotAPI()
    pol = []
    
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from chromedriver_py import binary_path

    driver = webdriver.Chrome(executable_path=binary_path)
    driver.get("https://www.congress.gov/help/field-values/member-bioguide-ids")
    tbody = driver.find_element(By.XPATH, "//table[@class='std full']/tbody")
    tb = tbody.text.split("\n")
    #print(tb)
    for tr in tb[1:]:
        c = tr.find(",")
        p = tr.find("(")
        tr = tr[:p]
        tr = tr[c+2:] + tr[:c]
        pol.append(tr)
        print(tr)
    
    #query = '''INSERT INTO members (Name) 
    #VALUES '''
    for p in pol:
        #query += f"({p}), "
        try:
            query = f'''INSERT INTO members (Name) VALUES ("{p}")'''
            print(query)
            sba.query(query)
        except sqlite3.OperationalError:
            query = f'''INSERT INTO members (Name) VALUES ('{p}')'''
            print(query)
            sba.query(query)
    sba.close()

if __name__ == "__main__":
    #d1 = date(2024, 3, 5)
    d1 = date.today()
    d2 = d1 - timedelta(days=5)
    fill(datetime(d1.year, d1.month, d1.day), datetime(d2.year, d2.month, d2.day))
    #d = date.today()-timedelta(days=3)
    #fill(datetime(d.year, d.month, d.day))
    print(d2)
    #fill_members()
