#server.py
#By: Sam Schmitz, Gavin Roy
# sql lite database object for stock bot

import sqlite3

class stockBotDatabase:
    
    def __init__(self):
        self.connection = sqlite3.connect('sql.db')
        self.cursor = self.connection.cursor()
        print('DB Init')
        
    def query(self, query):
        self.cursor.execute(query)
        
    def fetchall(self):
        return self.cursor.fetchall()
    
    def close(self):
        self.cursor.close()
        self.connection.close()
        print('SQLite connection closed')
