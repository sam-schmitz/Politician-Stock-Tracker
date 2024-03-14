# analysis.py
# By: Sam Schmitz
# methods for analyzing the data 

from datetime import datetime, timedelta, date

from server import stockBotAPI
from stockChecker import cPrice

def analyze_six_months_mem(mem):
    #calculates the average percent the given member has made
        #both since they made the trade and since they disclosed it
    api = stockBotAPI()
    #d = date.today()-timedelta(days=180)
    #trades = api.get_member_trades(mem, datetime(d.year, d.month, d.day))
    trades = api.get_member_trades(mem)
    totalGainB = 0
    totalGainD = 0
    totalInvested = 0
    sizeToEstAmt = {0 : 500,
                   1 : 8000,
                   2 : 32500,
                   3 : 75000,
                   4 : 175000,
                   5 : 375000,
                   6 : 750000,
                   7 : 2500000,
                   8 : 7500000}
    biggestEarner = None
    biggestGain = 0
    for t in trades:
        if t["saleType"] == "BUY":
            print("Buy Found: " , t['tick'], t['dateDis'])
            cp = cPrice(t['tick'])
            estAmt = sizeToEstAmt[t['size']]
            totalGainB += (cp - t["priceB"]) * estAmt
            gainB = (cp - t["priceD"]) * estAmt
            totalGainD += gainB
            totalInvested += estAmt
            print(totalGainB, totalGainD)
            if gainB > biggestGain:
                biggestEarner = t
                biggestGain = gainB
                print(f"Biggest Earner: {t['tick']} ${estAmt} {t['member']} {t['dateB']}'")
    avgGainB = totalGainB/len(trades)
    avgGainD = totalGainD/len(trades)
    print("Average proft gained per trade: ", avgGainB)
    print("Average profit gained per trade after disclosure: ", avgGainD)
    print("Total amount invested: ", totalInvested)
    print("Total profit gained: ", totalGainB)
    print("Total profit gained after disclosure: ", totalGainD)
    print("% gain overall: ", (totalGainB/totalInvested)*100 )
    print("% gain after disclosure: ", (totalGainD/totalInvested)*100)
    print(f"Biggest Earner: {biggestEarner['tick']} ${sizeToEstAmt[biggestEarner['size']]} {biggestEarner['member']} {biggestEarner['dateB']}'")
    return avgGainB, avgGainD, totalInvested

def analyze_all():
    api = stockBotAPI()
    trades = api.get_all_trades()
    totalGainB = 0
    totalGainD = 0
    totalInvested = 0
    sizeToEstAmt = {0 : 500,
                   1 : 8000,
                   2 : 32500,
                   3 : 75000,
                   4 : 175000,
                   5 : 375000,
                   6 : 750000,
                   7 : 2500000,
                   8 : 7500000}
    biggestEarner = None
    biggestGain = 0
    for t in trades:
        if t["saleType"] == "BUY":
            print("Buy Found: " , t['tick'], t['dateDis'])
            cp = cPrice(t['tick'])
            estAmt = sizeToEstAmt[t['size']]
            totalGainB += (cp - t["priceB"]) * estAmt
            gainB = (cp - t["priceD"]) * estAmt
            totalGainD += gainB
            totalInvested += estAmt
            print(totalGainB, totalGainD)
            if gainB > biggestGain:
                biggestEarner = t
                biggestGain = gainB
                print(f"Biggest Earner: {t['tick']} ${estAmt} {t['member']} {t['dateB']}'")
    avgGainB = totalGainB/len(trades)
    avgGainD = totalGainD/len(trades)
    print("Average proft gained per trade: ", avgGainB)
    print("Average profit gained per trade after disclosure: ", avgGainD)
    print("Total amount invested: ", totalInvested)
    print("Total profit gained: ", totalGainB)
    print("Total profit gained after disclosure: ", totalGainD)
    print("% gain overall: ", (totalGainB/totalInvested)*100 )
    print("% gain after disclosure: ", (totalGainD/totalInvested)*100)
    print(f"Biggest Earner: {biggestEarner['tick']} ${sizeToEstAmt[biggestEarner['size']]} {biggestEarner['member']} {biggestEarner['dateB']}'")
    return avgGainB, avgGainD, totalInvested
    
if __name__ == "__main__":
    analyze_all()
    #six_months_avg_mem("Tommy Tuberville")


