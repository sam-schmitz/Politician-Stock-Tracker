#server.py
#By: Sam Schmitz, Gavin Roy
# sql lite database object for stock bot

import sqlite3

from trade import trade

class stockBotAPI:
    
    def __init__(self):
        self.conn = sqlite3.connect('sbDatabase.db')
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
        self.cursor.execute(f"INSERT INTO trades VALUES ({trade.tick})")
        self.conn.commit()
        
    def get_all_trades(self, date=None):
        #gets trades from (current, date) for all members in the database
        query = f"SELECT * FROM trades"
        if date != None:    #add to query the date info
            pass
        self.cursor.execute(query)
        self.conn.commit()
        allTrades = self.cursor.fetchall()
        return self._fetchall_to_trades(allTrades)
    
    def get_member_trades(self, member, date=None):
        #gets trades from (current, date) for a named member
        query = f""
        if date != None:    #add to query the date info
            pass
        self.cursor.execute(query)
        self.conn.commit()
        allTrades = self.cursor.fetchall()
        return self._fetchall_to_trades(allTrades)
        
    def _fetchall_to_trades(self, fetchall):
        #turns data from fetchall into a list of trade obj
        trades = []
        for trade in fetchall:
            pass
            #make a trade object for each trade
            #add it to trades
        return trades
        
        

