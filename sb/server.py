#server.py
#By: Sam Schmitz, Gavin Roy
# sql lite database object for stock bot

import sqlite3

from trade import trade
from datetime import datetime

class stockBotAPI:
    
    def __init__(self, db=None):
        if db == None:
            db = 'sbDatabase.db'
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        print('DB Init')
        
    def query(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        
    def fetchall(self):
        return self.cursor.fetchall()
    
    def close(self):
        self.cursor.close()
        self.conn.close()
        print('SQLite connection closed')
        
    def add_trade(self, trade):
        # trade is a trade obj
        """query = f'''SELECT comittees
                    FROM members
                    WHERE Name={trade.member}'''
        memberInfo = self.cursor.execute(query).fetchall()
        
        #calculate crossover"""
    
        #check if stock is in the stock table
            #if not add the stock to the table

        queryFetchStock = f'''SELECT stockID FROM stocks
                              WHERE tick="{trade.tick}"'''
        stockID = self.cursor.execute(queryFetchStock).fetchall()
        if stockID == []:
            self.add_stock(trade.tick)
            stockID = self.cursor.execute(queryFetchStock).fetchall()
        
        queryFetchMember = f'''SELECT memberID FROM members 
                               WHERE NAME="{trade.member}"'''
        #print(queryFetchMember)
        memberID = self.cursor.execute(queryFetchMember).fetchall()
        if memberID == []:
            self.add_member(trade.member)
            memberID = self.cursor.execute(queryFetchMember).fetchall()
        
        query = f'''INSERT INTO trades (stockID, saleType, memberID, dateBought, priceBought, dateDisclosed, priceDisclosed, Delay, size) 
                    VALUES ({stockID[0][0]}, '{trade.saleType}', {memberID[0][0]}, '{trade.dateB.strftime("%m %d %Y")}', {trade.priceB}, '{trade.dateD.strftime("%m %d %Y")}', {trade.priceD}, {trade.delay}, {trade.size})'''
        print(query)
        #need to figure out how to add IDs to the query
        #use brakets {} to move data from the trade obj to query str

        self.cursor.execute(query)
        self.conn.commit()
        
    def add_stock(self, tick):
        query = f"""INSERT INTO stocks (tick) 
        VALUES ('{tick}')"""
        self.cursor.execute(query)
        self.conn.commit()
        
    def add_member(self, name):
        query = f"INSERT INTO members (Name) VALUES ('{name}')"
        self.cursor.execute(query)
        self.conn.commit()
        
    def get_all_trades(self, date=None):
        #gets trades from (current, date) for all members in the database
        query = f'''SELECT s.tick, t.saleType, 
                    t.dateBought, t.dateDisclosed, m.Name, t.priceBought, t.priceDisclosed, t.size
                    FROM stocks s
                    INNER JOIN trades t ON s.stockID = t.stockID
                    INNER JOIN members m ON t.memberID = m.memberID'''
        if date != None:    #add to query the date info
            pass
        rawData = self.cursor.execute(query).fetchall()
        trades = []
        for t in rawData:
            trades.append({"tick":t[0], 
                           'saleType':t[1], 
                           "dateB":datetime.strptime(t[2], '%m %d %Y'), 
                           'dateDis':datetime.strptime(t[3], '%m %d %Y'), 
                           'member':t[4],
                           'priceB':t[5],
                           'priceD':t[6],
                           'size':t[7]})
        return trades
    
    def get_member_trades(self, member, date=None):
        #gets trades from (current, date) for a named member
        query = f'''SELECT s.tick, t.saleType,
                    t.dateBought, t.dateDisclosed, m.Name, t.priceBought, t.priceDisclosed, t.size
                    FROM stocks s
                    INNER JOIN trades t ON s.stockID = t.stockID
                    INNER JOIN members m ON t.memberID = m.memberID
                    WHERE m.Name = {member}'''
        if date != None:    #add to query the date info
            pass
        #I need the priceBought and priceDisclosed
        rawData = self.cursor.execute(query).fetchall()
        trades = []
        for t in rawData:
            trades.append({"tick":t[0], 
                           'saleType':t[1], 
                           "dateB":datetime.strptime(t[2], '%m %d %Y'), 
                           'dateDis':datetime.strptime(t[3], '%m %d %Y'), 
                           'member':t[4],
                           'priceB':t[5],
                           'priceD':t[6],
                           'size':t[7]})
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
        
    def _fetchall_to_trades(self, fetchall):
        #turns data from fetchall into a list of trade obj
        #I need the data in 0-4 to be tick, saleType, dateBought, dateDis, member
        trades = []
        for t in fetchall:
            trades.append(trade(t[0], t[1], t[2], t[3], t[4]))
        return trades

if __name__ == "__main__":
    api = stockBotAPI()
    api.close()
        
        

