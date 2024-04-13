#stockChecker.py
# By: Sam Schmitz
# methods for finding the price of a stock in US $

import datetime, time
from datetime import date
import requests
from bs4 import BeautifulSoup

def cPrice(tick):
    """Checks the current price of a stock
    tick=the 'ticker' of the stock"""
    url = f"https://finance.yahoo.com/quote/{tick}/"
    response = requests.get(url, headers={'Connection': 'keep-alive',
                'Expires': '-1',
                'Upgrade_Insecure-Requests' : '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
                })
    soup = BeautifulSoup(response.text, "html.parser")
    return float(soup.find("fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)").text.replace(',', ''))

def pPrice(tick, d):
    """Gets adjusted close price of a stock at a specific date
    tick=the 'ticker' of the stock
    date = the specfic date (YYYY-MM-DD) or datetime Must be valid date of the stock market
    return price(int)"""
    if type(d).__name__=="str":
        d = date_to_datetime(d)
    if vDate(d) == False:
        raise TypeError("Stock Market was not open on: ", d)
    d = d.date()
    if d == date.today():
        return cPrice(tick)
    #get data from yahoo
    dd = int(time.mktime(d.timetuple()))
    url = f"https://finance.yahoo.com/quote/{tick}/history?period1={str(dd)}&period2={str(dd+86400)}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
    header = {'Connection': 'keep-alive',
                'Expires': '-1',
                'Upgrade_Insecure-Requests' : '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
                }
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "html.parser")
    #sort the data
    return float(soup.find("td", class_="Py(10px) Pstart(10px)").find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").find_next_sibling("td").text.replace(',', ''))

def stockGain(tick, date1, date2=datetime.datetime.today()):
    """Calculates the total gain or lose over a period of time
    tick=the 'ticker' of the stock
    date1 = the start of the period (YYYY-MM-DD)
    date2 = the end of the period (default current date)"""
    return round((pPrice(tick, date2) - pPrice(tick, date1)), 2)

def stockPercentGain(tick, date1, date2=datetime.datetime.today()):
    """Calculates the percent gain or loss over a period of time
    tick = the 'ticker' of the stock
    date1 = the start of the period (YYYY-MM-DD)
    date2 = the end of the period (default current date)
    returns percent as a decimal"""
    p1 = pPrice(tick, date1)
    p2 = pPrice(tick, date2)
    return (p2-p1) / p1

def stock_sector(tick):
    """uses whalewisdom.com to find the sector the stock belongs to
    """
    url = f"https://finance.yahoo.com/quote/{tick}/profile/"
    header = {'Connection': 'keep-alive',
                'Expires': '-1',
                'Upgrade_Insecure-Requests' : '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
                }
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find("p", class_="D(ib) Va(t)").find("span").find_next_sibling("span").text

def stock_industry(tick):
    url = f"https://finance.yahoo.com/quote/{tick}/profile/"
    header = {'Connection': 'keep-alive',
                'Expires': '-1',
                'Upgrade_Insecure-Requests' : '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
                }
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find("p", class_="D(ib) Va(t)").find("span").find_next_sibling("span").find_next_sibling("span").find_next_sibling("span").text

def date_to_datetime(date):
    """Turns a date(str or datetime) to a datetime object
    "2022-01-01" -> datetime"""
    dateS = date.split("-")
    return datetime.datetime(int(dateS[0]), int(dateS[1]), int(dateS[2]))

def datetime_to_date(datet):
    """turns a datetime object to a string (YYYY-MM-DD)
    """
    return f"{datet.year}-{datet.month}-{datet.day}"

def vDate(date):
    """Checks if a date is valid(stock market was open)
    input: datetime
    output: bool
    """
    return date.weekday() < 5


if __name__ == "__main__":
    print("cPrice ^GSPC", cPrice('^GSPC'))
    print("pPrice ^GSPC 2022-01-03", pPrice('^GSPC', '2022-01-03'))
    print("pPrice ^GSPC, today:", pPrice('^GSPC', datetime.datetime.today()))
    #should be 399.93
    print("stock gain ^GSPC:", stockGain('^GSPC', '2022-01-03'))
    print("INTC Sector:", stock_sector('INTC'))
    print("INTC Industry: ", stock_industry('INTC'))
    #print(pPrice('^GSPC', '2022-10-2')) #raises TypeError
