# createServer.py
# By: Sam Schmitz, Gavin Roy
# creates the database to be used by server.py

import sqlite3
from os import path

if __name__ == "__main__":
    conn = sqlite3.connect("sbDatabase.db")
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE ")
    cursor.execute("CREATE TABLE ")
    cursor.execute("CREATE TABLE ")
    conn.commit()
    
    print(conn.total_changes)
