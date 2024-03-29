# analysis.py
# By: Sam Schmitz
# methods for analyzing the data 

from datetime import datetime, timedelta, date
import yfinance as yf

from server import stockBotAPI
from stockChecker import cPrice

def analyze_six_months_mem(mem, date=None):
    if mem == 'all':
        return analyze_all()
    #calculates the average percent the given member has made
        #both since they made the trade and since they disclosed it
    api = stockBotAPI()
    #d = date.today()-timedelta(days=180)
    #trades = api.get_member_trades(mem, datetime(d.year, d.month, d.day))
    trades = api.get_member_trades(mem, date)
    if len(trades) == 0:
        print("No trades meet the parameters")
        return None
    return _analyze(trades)
    
def analyze_all(date=None):
    api = stockBotAPI()
    trades = api.get_all_trades(date=date)
    if len(trades) == 0:
        print("No trades meet the parameters")
        return None
    return _analyze(trades)
    
def _analyze(trades):
    tickers = []
    for t in trades:
        tickers.append(t['tick'])
    d1 = date.today()
    
    df = yf.download(tickers, start=d1)
    print(df) 
    
    for t in range(len(trades)):
        trades[t]['cPrice'] = df[('Adj Close', trades[t]['tick'])][-1]

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
            print(f"Buy Found: Tick: {t['tick']}, DateDis {t['dateDis']}, cPrice: {t['cPrice']}")
            cp = t['cPrice']
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
    avgGainB = round(totalGainB/len(trades), 2)
    avgGainD = round(totalGainD/len(trades), 2)
    print("Average proft gained per trade: ", avgGainB)
    print("Average profit gained per trade after disclosure: ", avgGainD)
    print("Total amount invested: ", totalInvested)
    print("Total profit gained: ", totalGainB)
    print("Total profit gained after disclosure: ", totalGainD)
    print("% gain overall: ", (totalGainB/totalInvested)*100 )
    print("% gain after disclosure: ", (totalGainD/totalInvested)*100)
    print(f"Biggest Earner: {biggestEarner['tick']} ${sizeToEstAmt[biggestEarner['size']]} {biggestEarner['member']} {biggestEarner['dateB']}'")
    return (avgGainB, avgGainD, totalInvested)
    
if __name__ == "__main__":
    """d1 = date.today()
    tickers = ['AAPL', 'MSFT']
    df = yf.download(tickers, start=d1)
    print(df.info())
    print("column: ")
    print(df[('Adj Close', 'AAPL')])
    print("price: ")
    print(df[('Adj Close', 'AAPL')][-1])"""
    analyze_all()
    #analyze_six_months_mem("Tommy Tuberville", datetime(2024, 3, 13))
