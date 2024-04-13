#congressTrades.py
#By: Sam Schmitz
#scrapes the stock trades made by members of congress from capitaltrades.com

from datetime import datetime
from datetime import date
from datetime import timedelta
from selenium import webdriver
#import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
#import chromedriver_binary
from chromedriver_py import binary_path
from time import sleep
from trade import trade

#used for selenium connection
HEADER = {'Connection': 'keep-alive',
            'Expires': '-1',
            'Upgrade_Insecure-Requests' : '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
            }

def getTrades(date, member=None):
    """Go to capitaltrades.com/trades and find all trades recorded after a certain date
    inclusive for date (date tracked at timezone 0)
    date = (YYYY-MM-DD)
    returns a list of trade objects
    """
    stockData = []
    stop = False
    pageNum = 0
    mem = None
    if member is not None:
        mem = getMemberCode(member)
    print("Ticks not found: ")
    while stop != True:
        pageNum += 1
        stop, data = _getPageInfo(date, pageNum, member=mem)
        stockData += data
    return stockData


def _getPageInfo(dateStop, pageNum, member=None):
    """Gets the trades from a page on capitaltrades.com using selenium
    dateStop = the date to stop expressed as a unix date
    pageNum = an int that tells the page to search
    returns a list of [tick, saleType(buy or sell), datebought, dateDis] for each stock found
    """
    #chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(executable_path=binary_path)
    #to update driver pip install chromedriver-py --upgrade

    if member != None:
        driver.get(f"https://www.capitoltrades.com/trades?page={str(pageNum)}&pageSize=50&politician={member}")
    else:
        driver.get(f"https://www.capitoltrades.com/trades?page={str(pageNum)}&pageSize=50")
    sleep(2)    #needs to sleep so that the javascript reliably loads
    
    #p_element = driver.find_element(By.CLASS_NAME, "q-pagination")
    #print(p_element.text)

    pageInfo = []
    stop = False
    print("dateStop: ", dateStop)
    
    for i in range(1, 51):  #range (1, 51) is all of the rows in website's table
        #checkdate
        dateDis = driver.find_element(By.XPATH, f"//div[@class='trade-table-scroll-wrapper']/table/tbody/tr[{i}]/td[3]").text.replace("\n", " ")
        dateDis = abrev_to_unix(dateDis)
        if dateDis < dateStop:
            stop = True
            print(dateDis, dateStop)
            break
        
        #gather the trade data
        tick = driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]/td[2]").text.replace(":US", "").split("\n")    #the tick is formated as [full tick name, TICK]
        saleType = driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]/td[7]").text
        dateBought = driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]/td[4]").text.replace("\n", " ")
        dateBought = abrev_to_unix(dateBought)
        member = driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]/td[1]").text.split("\n")
        size = driver.find_element(By.XPATH, f"//table/tbody/tr[{i}]/td[8]").text
        size = _range_to_size(size)
        
        if tick[1] != "N/A":    #some ticks are not actual stocks and will cause errors
            try:
                pageInfo.append(trade(tick[1], saleType, dateBought, dateDis, member[0], size))
            except AttributeError:
                print(tick[1])
            except IndexError:
                print(tick[1])
            except KeyError:
                print("Likely an ETF: ", tick[1])   #could also be a cryptocurrency
        #print("row data:", tick[1], saleType, dateBought, dateDis, member)
    return stop, pageInfo

def get_trades_d_to_d(d1, d2, member=None):
    #similar to get_trades but gathers info in between a range of dates
    stockData = []
    stop = False
    pageNum = 0
    mem = None  #used in _get_page_info functions
    if member is not None:
        mem = getMemberCode(member)
        
    #find the page where the range of dates starts
    print("date start: ", d1)
    while stop != True:
        pageNum += 1
        stop = _get_page_info_start(d1, pageNum, member=mem)
    #resets the loop parameters
    stop = False
    pageNum -= 1
    
    #collects the data
    print("Ticks not found: ")
    while stop != True:
        pageNum += 1
        stop, data = _getPageInfo(d2, pageNum, member=mem)
        stockData += data
        
    #an attempt to remove data from before d1
    t = 0
    while True:
        if stockData[t].dateD <= d1:
            break
        print(stockData[t].dateD)
        stockData.pop(t)
        t += 1
    return stockData

def _get_page_info_start(dateStart, pageNum, member=None):
    #open the webpage
    driver = webdriver.Chrome(executable_path=binary_path)
    if member != None:
        driver.get(f"https://www.capitoltrades.com/trades?page={str(pageNum)}&pageSize=50&politician={member}")
    else:
        driver.get(f"https://www.capitoltrades.com/trades?page={str(pageNum)}&pageSize=50")
    sleep(2)
    
    stop = False
    for i in range(1, 51):
        #checkdate
        dateDis = driver.find_element(By.XPATH, f"//div[@class='trade-table-scroll-wrapper']/table/tbody/tr[{i}]/td[3]").text.replace("\n", " ")
        dateDis = abrev_to_unix(dateDis)
        if dateDis <= dateStart:
            stop = True
            print("stop found: ", dateDis)
            break
    return stop

def _range_to_size(r):
    #trade volume is given in a range
    #this method converts that range to an int for later use
    find = r.find("K")
    r2 = r[:find]
    if len(r2) > 3:
        find = r.find("M")
        r2 = r[:find+1]
    ranges = {"< 1": 0,
              "1" : 1,
              "15": 2,
              "50": 3,
              "100": 4,
              "250": 5,
              "500": 6,
              "1M": 7,
              "5M": 8}
    return ranges[r2]

def abrev_to_unix(abrev):
    """turns the abreviated version of a date(ex:2022 13 Oct) into a datetime form
    """
    try:
        try:
            return datetime.strptime(abrev[:11], '%Y %d %b')
        except:
            return datetime.strptime(abrev[:10], '%Y %d %b')
    except:
        if abrev.find('yesterday') == 0:
            dateR = date.today() - timedelta(days=1)
        else:
            dateR = date.today()
        return datetime(dateR.year, dateR.month, dateR.day)

def getMemberCode(member):
    """return a congress members code for capitaltrades
    example member: Doe, John
    """
    #svc = webdriver.ChromeService(executable_path=binary_path)
    driver = webdriver.Chrome(executable_path=binary_path)
    driver.get("https://www.congress.gov/help/field-values/member-bioguide-ids")
    tbody = driver.find_element(By.XPATH, "//table[@class='std full']/tbody")
    tb = tbody.text.split("\n")
    for tr in tb:
        if member in tr:
            return tr[-7:]


if __name__ == "__main__":
    d = date.today()-timedelta(days=3)
    #for t in getTrades(datetime(d.year, d.month, d.day)):
        #print(t.tick, t.saleType, t.delay)
    #print(getMemberCode("Abdnor, James"))
    #print("trades made by Earl Blumenauer since Jan 1, 2023: ")
    #for t in getTrades(datetime(2023, 1, 1), member="Blumenauer, Earl"):
        #print(t.tick, t.saleType, t.delay)
    d2 = d-timedelta(days=3)
    for t in get_trades_d_to_d(datetime(d.year, d.month, d.day), datetime(d2.year, d2.month, d2.day)):
        print(t.tick, t.member, t.saleType, t.delay)
