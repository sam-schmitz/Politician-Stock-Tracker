# analysis.py
# By: Sam Schmitz
# methods for analyzing the data 

from datetime import datetime, timedelta, date

from server import stockBotAPI
from stockChecker import cPrice, pPrice

def six_months_avg_mem(mem):
    #calculates the average percent the given member has made
        #both since they made the trade and since they disclosed it
    api = stockBotAPI()
    d = date.today()-timedelta(days=180)
    trades = api.get_member_trades(mem, datetime(d.year, d.month, d.day))
    totalGainPercentB = 0
    totalGainPercentD = 0
    for t in trades:
        if t[1] == "BUY":
            cPrice = cPrice(t[0])
            priceB = pPrice(t[2])
            priceD = pPrice(t[3])
            totalGainPercentB += (cPrice/priceB)/priceB
            totalGainPercentD += (cPrice/priceD)/priceD
    avgGainB = totalGainPercentB/trades.length
    avgGainD = totalGainPercentD/trades.length
    print("Average % gained: ", avgGainB)
    print("Average % gained after disclosed: ", avgGainD)


