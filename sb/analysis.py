# analysis.py
# By: Sam Schmitz
# methods for analyzing the data 

from datetime import date
from math import isnan
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

def analyze_given(trades):
    return _analyze(trades)
    
def _analyze(trades):
    #get a list of each tick so that we can scrape for the current prices in one go
    tickers = []
    for t in trades:
        tickers.append(t['tick'])
    d1 = date.today()
    
    #collect the current price data from yf
    df = yf.download(tickers, start=d1) #no data if it is a weekend
    #print(df) 
    
    for t in range(len(trades)):    #put the current price with the associated trade
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
    tradesAnalysis = []
    for t in trades:
        if t["saleType"] == "BUY":
            print(f"Buy Found: Tick: {t['tick']}, DateDis {t['dateDis']}, cPrice: {t['cPrice']}, priceB: {t['priceB']}, priceD: {t['priceD']}")
            cp = t['cPrice']
            if isnan(cp):
                print(f"Data not found for {t['tick']}")
                continue
            
            #find the percent gain in the stock price since the member bought it
            estAmt = sizeToEstAmt[t['size']]
            pGainB = (cp-t['priceB'])/t['priceB']
            pGainD = (cp-t['priceD'])/t['priceD']
            
            #use the stock gain to calculate the gain in the traders portfolio
            gainB = pGainB * estAmt
            totalGainB += gainB
            gainD = pGainD * estAmt
            print(f"gainB: {gainB}, gainD: {gainD}")
            
            #update the runnning totals for the group
            totalGainD += gainD
            totalInvested += estAmt
            print(f"totalGainB: {totalGainB}, totalGainD: {totalGainD}")
            
            #check if this trade is the biggest earner
            if gainD > biggestGain:
                biggestEarner = t
                biggestGain = gainD
                print(f"Biggest Earner: {t['tick']} ${estAmt} {t['member']} {t['dateB']}, {gainB}")
                
            tradesAnalysis.append({'tick': t['tick'],
                           'gainB' : gainB,
                           'gainD' : gainD,
                           'member': t['member'],
                           'estAmt': estAmt,
                           'priceB': t['priceB'],
                           'priceD': t['priceD'],
                           'priceC' : cp,
                           'saleType' : t['saleType'],
                           'dateB' : t['dateB'],
                           'dateD' : t['dateDis']})
            
    avgGainB = round(totalGainB/len(trades), 2)
    avgGainD = round(totalGainD/len(trades), 2)
    
    print("Average proft gained per trade: ", avgGainB)
    print("Average profit gained per trade after disclosure: ", avgGainD)
    print("Total amount invested: ", totalInvested)
    print("Total profit gained: ", totalGainB)
    print("Total profit gained after disclosure: ", totalGainD)
    print("% gain overall: ", ((totalInvested-totalGainB)/totalGainB)*100 )
    print("% gain after disclosure: ", (totalGainD/totalInvested)*100)
    print(f"Biggest Earner: {biggestEarner['tick']} ${sizeToEstAmt[biggestEarner['size']]} {biggestEarner['member']} {biggestEarner['dateB']}'")
    
    biggestEarner['size'] = sizeToEstAmt[biggestEarner['size']]
    return (avgGainB, avgGainD, totalInvested, len(trades), biggestEarner, tradesAnalysis)
    
if __name__ == "__main__":
    analyze_all()
    #analyze_six_months_mem("Tommy Tuberville", datetime(2024, 3, 13))
