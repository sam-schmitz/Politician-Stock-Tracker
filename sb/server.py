#server.py
#By: Sam Schmitz, Gavin Roy
# sql lite database object for stock bot

import sqlite3

from trade import trade

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
        query = f'''SELECT comittees
                    FROM members
                    WHERE Name={trade.member}'''
        memberInfo = self.cursor.execute(query).fetchall()
        #calculate crossover
        query = f'''INSERT INTO trades (stockID, saleType, memberID, dateBought, priceBought, dateDisclosed, priceDisclosed, Delay, Crossover) 
                    VALUES ({"stockID"}, {trade.saleType}, {"memberID"}, {trade.dateB}, {trade.priceB}, {trade.dateD}, {trade.priceD}, {trade.delay}, {"crossover"})'''
        #use brakets {} to move data from the trade obj to query str
        self.cursor.execute(query)
        self.conn.commit()
        
    def get_all_trades(self, date=None):
        #gets trades from (current, date) for all members in the database
        query = f'''SELECT s.tick, t.saleType, 
                    t.dateBought, t.dateDistributed, t.memberID, t.priceBought, t.priceDisclosed
                    FROM stocks s
                    INNER JOIN trades t ON s.stockID = t.stockID'''
        if date != None:    #add to query the date info
            pass
        #can I get all of the data?
        rawData = self.cursor.execute(query).fetchall()
        trades = []
        for t in rawData:
            trades.append({"tick":t[0], 
                           'saleType':t[1], 
                           "dateB":t[2], 
                           'dateDis':t[3], 
                           'member':t[4]
                           'priceB':t[5]
                           'priceD':t[6]})
        return trades
    
    def get_member_trades(self, member, date=None):
        #gets trades from (current, date) for a named member
        query = f'''SELECT s.tick, t.saleType,
                    t.dateBought, t.dateDistributed, t.memberID, t.priceBought, t.priceDisclosed
                    FROM stocks s
                    INNER JOIN trades t ON s.stockID = t.stockID
                    WHERE t.memberID = 'Joe Biden' '''
        if date != None:    #add to query the date info
            pass
        #I need the priceBought and priceDisclosed
        rawData = self.cursor.execute(query).fetchall()
        trades = []
        for t in rawData:
            trades.append({"tick":t[0], 
                           'saleType':t[1], 
                           "dateB":t[2], 
                           'dateDis':t[3], 
                           'member':t[4]
                           'priceB':t[5]
                           'priceD':t[6]})
        return trades
        #return self._fetchall_to_trades(allTrades)
        
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
        
        

