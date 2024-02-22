#server.py
#By: Sam Schmitz, Gavin Roy
# sql lite database object for stock bot

import sqlite3

class stockBotDatabase:
    
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
        
    def addTrade(self, trade):
        # trade is a trade obj
        self.cursor.execute(f"INSERT INTO trades VALUES ({trade.tick})")
        self.conn.commit()
        
    def getAllTrades(self):
        self.cursor.execute(f"SELECT * FROM trades")
        self.conn.commit()
        return self.cursor.fetchall()

