#server.py
#By: Sam Schmitz, Gavin Roy
# a obj that allows the user to acsess the data in the db

import sqlite3

from trade import trade
from datetime import datetime

import yfinance as yf

class stockBotAPI:
    
    def __init__(self, db=None):    #creates the connection
        if db == None:
            db = 'sbDatabase.db'
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        print('DB Init')
        
    def query(self, query): #allows the user to query the db
        self.cursor.execute(query)
        self.conn.commit()
        
    def fetchall(self): #collect data from a previous query
        return self.cursor.fetchall()
    
    def close(self):    #close the connection to save resources
        self.cursor.close()
        self.conn.close()
        print('SQLite connection closed')
        
    def add_trade(self, trade):
        # trade is a trade obj

        #stuff for crossover (not working yet)
        """query = f'''SELECT comittees
                    FROM members
                    WHERE Name={trade.member}'''
        memberInfo = self.cursor.execute(query).fetchall()
        
        #calculate crossover"""
    
        #find the stockID for the tick
        queryFetchStock = f'''SELECT stockID FROM stocks
                              WHERE tick="{trade.tick}"'''
        stockID = self.cursor.execute(queryFetchStock).fetchall()
        
        #stock might not be in the db
        if stockID == []:
            #add the stock to the db
            self.add_stock(trade.tick)
            stockID = self.cursor.execute(queryFetchStock).fetchall()
        
        #find the memberID for the member
        queryFetchMember = f'''SELECT memberID FROM members 
                               WHERE NAME="{trade.member}"'''
        memberID = self.cursor.execute(queryFetchMember).fetchall()
        
        #member might not be in the db
        if memberID == []:
            #add the memeber to the db
            self.add_member(trade.member)
            memberID = self.cursor.execute(queryFetchMember).fetchall()
        
        #query to add a new row to the trades table
        query = f'''INSERT INTO trades (stockID, saleType, memberID, dateBought, priceBought, dateDisclosed, priceDisclosed, Delay, size) 
                    VALUES ({stockID[0][0]}, '{trade.saleType}', {memberID[0][0]}, '{trade.dateB.strftime("%Y%m%d")}', {trade.priceB}, '{trade.dateD.strftime("%Y%m%d")}', {trade.priceD}, {trade.delay}, {trade.size})'''
        print(query)
        self.cursor.execute(query)
        self.conn.commit()
        
    def add_stock(self, tick):  #adds a stock to the db table stocks
        #get the stocks info
        tyf = yf.Ticker(tick)
        info = tyf.info
        
        query = f"""INSERT INTO stocks (tick, companyName, sector, industry) 
        VALUES ('{tick}', '{info['longName']}', '{info['sector']}', '{info['industry']}')"""
        print(query)
        
        #some stocks have ' or " in their name
        try:
            self.cursor.execute(query)
        except:
            query = f'''INSERT INTO stocks (tick, companyName, sector, industry) VALUES ("{tick}", "{info['longName']}", "{info['sector']}", "{info['industry']}")'''
            self.cursor.execute(query)
        self.conn.commit()
        
    def add_member(self, name): #adds a member to the members table
        query = f"INSERT INTO members (Name) VALUES ('{name}')"
        self.cursor.execute(query)
        self.conn.commit()
        
    def add_newest_date(self, date):    #update the date of the newest data
        query = f'''INSERT INTO newestDate (date)
        VALUES ({date.strftime("%Y%m%d")})'''
        self.cursor.execute(query)
        self.conn.commit()
    
    def add_oldest_date(self, date):    #update the date of the oldest data
        query = f'''INSERT INTO oldestDate (date)
        VALUES ({date.strftime("%Y%m%d")})'''
        self.cursor.execute(query)
        self.conn.commit()
        
    def get_all_trades(self, date=None):    #gets trades from (current, date) for all members in the database
        #combine rows from trades, stocks, and members
        query = f'''SELECT s.tick, t.saleType, 
                    t.dateBought, t.dateDisclosed, m.Name, t.priceBought, t.priceDisclosed, t.size, t.Delay, s.companyName
                    FROM stocks s
                    INNER JOIN trades t ON s.stockID = t.stockID
                    INNER JOIN members m ON t.memberID = m.memberID'''
        
        #if a date is given check add it to the parameters
        if date != None: 
            query += f" AND t.dateDisclosed > '{date.strftime('%Y%m%d')}'"
            f'''SELECT t.dateBought, t.dateDisclosed FROM trades t
                             WHERE t.dateBought = "{date}",
                             t.dateDisclosed = "{date}"''' #queries date info
            
        rawData = self.cursor.execute(query).fetchall()
        
        #turn the rawData from the db to useable data in a dictionary
        trades = []
        for t in rawData:   
            trades.append({"tick":t[0], 
                           'saleType':t[1], 
                           "dateB":datetime.strptime(str(t[2]), '%Y%m%d'), 
                           'dateDis':datetime.strptime(str(t[3]), '%Y%m%d'), 
                           'member':t[4],
                           'priceB':t[5],
                           'priceD':t[6],
                           'size':t[7],
                           'delay':t[8],
                           'companyName':t[9]})
        return trades
    
    def get_member_trades(self, member, date=None):     #gets trades from (current, date) for a named member
        #combines data from trades, members, and stocks
        query = f'''SELECT s.tick, t.saleType,
                    t.dateBought, t.dateDisclosed, m.Name, t.priceBought, t.priceDisclosed, t.size, t.Delay, s.companyName
                    FROM stocks s
                    INNER JOIN trades t ON s.stockID = t.stockID
                    INNER JOIN members m ON t.memberID = m.memberID
                    WHERE m.Name = "{member}"'''
        
        #if a date is given add a check to the query
        if date != None: 
            query += f" AND t.dateDisclosed > {date.strftime('%Y%m%d')}"
            """f'''SELECT t.dateBought, t.dateDistributed FROM trades t
                             WHERE t.dateBought = "{trade.dateB}",
                             t.dateDistributed = "{trade.dateD}"''' #queries date info"""
            print(query)
            
        rawData = self.cursor.execute(query).fetchall()
        
        #turn the rawData from the db to useable data in a dictionary
        trades = []
        for t in rawData:
            trades.append({"tick":t[0], 
                           'saleType':t[1], 
                           "dateB":datetime.strptime(str(t[2]), '%Y%m%d'), 
                           'dateDis':datetime.strptime(str(t[3]), '%Y%m%d'), 
                           'member':t[4],
                           'priceB':t[5],
                           'priceD':t[6],
                           'size':t[7],
                           'delay':t[8],
                           'companyName':t[9]})
        return trades
        #return self._fetchall_to_trades(allTrades)

    def get_all_members(self):
        #returns a list of all members in the database
        query = f"""SELECT Name 
        FROM members"""
        rawData = self.cursor.execute(query).fetchall()
        members = []
        for t in rawData:
            members.append(t[0])
        return members
    
    def get_newest_date(self):  #returns the date of the newest scraped data
        query = f'''SELECT MAX(date) FROM newestDate ''' 
        return datetime.strptime(str(self.cursor.execute(query).fetchone()[0]), '%Y%m%d')
    
    def get_oldest_date(self):  #returns the date of the oldest scraped data
        query = f'''SELECT MIN(date) FROM oldestDate ''' 
        d = str(self.cursor.execute(query).fetchone()[0])
        return datetime.strptime(str(self.cursor.execute(query).fetchone()[0]), '%Y%m%d')
        
    def _fetchall_to_trades(self, fetchall):
        #turns data from fetchall into a list of trade obj
        trades = []
        for t in fetchall:
            trades.append(trade(t[0], t[1], t[2], t[3], t[4]))
        return trades

if __name__ == "__main__":
    api = stockBotAPI()
    api.close()
        
        

