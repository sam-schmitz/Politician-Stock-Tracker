# fillDatabase.py
# By: Sam Schmitz, Gavin Roy
# fills the database
# current fill can be found at the bottom by the main statement

import sqlite3
from datetime import datetime, timedelta, date

from congressTrades import get_trades_d_to_d
from server import stockBotAPI

def fill(d1, d2):   #fills the database with data from d1 - d2
    #d1, d2 -> datetime obj
    sba = stockBotAPI()
    check = _check_dates(d1, d2, sba)
    
    #scrape the data
    trades = get_trades_d_to_d(d1, d2)  
    
    #enter the data into the db
    for t in trades:
        sba.add_trade(trade=t)
        
    #update the db with the new dates 
    if check == "d1":
        sba.add_oldest_date(d2)
    else:
        sba.add_newest_date(d1)
        
    sba.close()
    return trades

def _check_dates(d1, d2, api):  #validates the dates 
    #check the value's type
    if isinstance(d1, datetime) == False:
        raise TypeError("d1 should be a date or datetime object")
    if isinstance(d2, datetime)==False:
        raise TypeError("d2 should be a date or datetime object")
    
    #compare d1 and d2 to the dates in the db
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
    if d1==oldD:
        return "d1"
    return "d2"

def fill_members(): #adds a most of the members to the db
    sba = stockBotAPI()
    pol = []
    
    #imports for scraping
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from chromedriver_py import binary_path

    #scrape the members
    driver = webdriver.Chrome(executable_path=binary_path)
    driver.get("https://www.congress.gov/help/field-values/member-bioguide-ids")
    tbody = driver.find_element(By.XPATH, "//table[@class='std full']/tbody")
    tb = tbody.text.split("\n")
    #print(tb)
    for tr in tb[1:]:   #(last, first)
        #turns the name from last, first to first last
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
        #some members have a ' or " in their name 
        try:
            query = f'''INSERT INTO members (Name) VALUES ("{p}")'''
            print(query)
            sba.query(query)
        except sqlite3.OperationalError:
            query = f'''INSERT INTO members (Name) VALUES ('{p}')'''
            print(query)
            sba.query(query)
    sba.close()
    
def fill_committees():  #fills the database table committees with their asocitated sectors/industries
    #not finished yet
    sba = stockBotAPI()
    committees = ["Agriculture", "Appropriations", "Armed Services", "Budget",
                  "Education and the Workforce", "Energy and Commerce", "Ethics",
                  "Financial Services", "Foreign Affairs", "Homeland Security", 
                  "House Administration", "Judiciary", "Natural Resourses", 
                  "Oversight and Accountability", "Rules", "Science, Space, and Technology",
                  "Small Business", "Transporation", "Veterans' Affairs", "Ways and Means",
                  "Agriculture, Nutrition, and Forestry", "Appropriations", "Banking, Housing, and Urban Affairs",
                  "Budget", "Commerce, Science, and Transportation", "Energy and Natural Resources", 
                  "Enviornment and Public Works", "Finance", "Foregin Relations", "Health, Education, Labor, and Pensions",
                  "Homeland Security and Governmental Affairs", "Judiciary", "Rules and Administration",
                  "Small Business and Entrpreneurship"]
    sectors = {"Agriculture" : None,
                "Appropriations" : None,
                "Armed Services" : "Consumer Defense",
                "Budget" : "Financial Services",             
                "Education and the Workforce" : None,
                "Energy and Commerce" : "Energy", 
                "Ethics" : None,                
                "Financial Services" : "Financial Services",
                "Foreign Affairs" : None,
                "Homeland Security" : "Consumer Defensive", 
                "House Administration" : None,
                "Judiciary" : None,
                "Natural Resourses" : "Basic Materials", 
                "Oversight and Accountability" : None,
                "Rules" : None,
                "Science, Space, and Technology" : "Technology",
                "Small Business" : None,
                "Transporation" : "Industrial/Consumer Cyclical",
                "Veterans' Affairs" : None,
                "Ways and Means" : None,
                "Agriculture, Nutrition, and Forestry" : "Basic Materials",
                "Appropriations" : None,
                "Banking, Housing, and Urban Affairs" : "Financial Services",
                "Budget" : "Financial Services",
                "Commerce, Science, and Transportation" : "Technology",
                "Energy and Natural Resources" : "Energy", 
                "Enviornment and Public Works" : "Utilities",
                "Finance" : "Financial Services",
                "Foregin Relations" : None,
                "Health, Education, Labor, and Pensions" : "Healthcare",
                "Homeland Security and Governmental Affairs" : "Consumer Defensive",
                "Judiciary" : None,
                "Rules and Administration" : None,
                "Small Business and Entrpreneurship" : None}
    
    industries = {"Agriculture" : "Agricultural Inputs/Farm & Heavy Construction Machinery",
                "Appropriations" : None,
                "Armed Services" : "Aerospace & Defense",
                "Budget" : None,             
                "Education and the Workforce" : "Education & Training Services",
                "Energy and Commerce" : None, 
                "Ethics" : None,                
                "Financial Services" : None,
                "Foreign Affairs" : None,
                "Homeland Security" : "Aerospace & Defense", 
                "House Administration" : None,
                "Judiciary" : None,
                "Natural Resourses" : None, 
                "Oversight and Accountability" : None,
                "Rules" : None,
                "Science, Space, and Technology" : None,
                "Small Business" : None,
                "Transporation" : "Auto Manufacturers/",
                "Veterans' Affairs" : None,
                "Ways and Means" : None,
                "Agriculture, Nutrition, and Forestry" : None,
                "Appropriations" : None,
                "Banking, Housing, and Urban Affairs" : None,
                "Budget" : None,
                "Commerce, Science, and Transportation" : None,
                "Energy and Natural Resources" : None, 
                "Enviornment and Public Works" : None,
                "Finance" : None,
                "Foregin Relations" : None,
                "Health, Education, Labor, and Pensions" : None,
                "Homeland Security and Governmental Affairs" : None,
                "Judiciary" : None,
                "Rules and Administration" : None,
                "Small Business and Entrpreneurship" : None}
    sba.close()
    
        
if __name__ == "__main__":
    #filled with (2024, 4, 11) - (2024, 1, 1)
    #check the database for duplicates
        #When it finds the right page it grabs everything on the page not what fits the range
    d1 = date(2024, 1, 31)
    #d1 = '2024-03-13'
    #d1 = date.today()
    #d2 = d1 - timedelta(days=3)
    #d2 = 20240313
    d2 = date(2024, 1, 1)
    #data = fill(d1, d2)
    data = fill(datetime(d1.year, d1.month, d1.day), datetime(d2.year, d2.month, d2.day))
    for trade in data:
        print(trade.tick, trade.member, trade.dateD)
    #d = date.today()-timedelta(days=3)
    #fill(datetime(d.year, d.month, d.day))
    print(d2)
    #fill_members()
