# createServer.py
# By: Sam Schmitz, Gavin Roy
# creates/resets the database to be used by server.py

import datetime
import sqlite3

if __name__ == "__main__":
    #Only run if the database needs to be created or reset.
    #Running may cause all stored data to be lost. 

    #connect to the db
    conn = sqlite3.connect("sbDatabase.db")
    cursor = conn.cursor()
    
    #cursor.execute('''DROP TABLE members; ''')
    #conn.commit()
    
    #cursor.execute('DROP TABLE trades; ''')
    #conn.commit()

    #cursor.execute('DROP TABLE stocks; ')
    #conn.commit()

    #cursor.execute('DROP TABLE newestDate; ')
    #conn.commit()
    #cursor.execute('DROP TABLE oldestDate; ')
    #conn.commit()

    cursor.execute(''' CREATE TABLE IF NOT EXISTS trades
                   (tradeID INTEGER PRIMARY KEY, stockID INTEGER FORGEIN KEY,
                   saleType TEXT, memberID INTEGER FORGEIN KEY,
                   dateBought INTEGER, priceBought INTEGER, dateDisclosed
                   INTEGER, priceDisclosed INTEGER, Delay INTEGER, Crossover
                   TEXT, size INTEGER)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS members
                   (memberID INTEGER PRIMARY KEY, comittees TEXT, Name TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS stocks
                   (stockID INTEGER PRIMARY KEY, tick TEXT, sector TEXT,
                   industry TEXT, companyName TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS newestDate
                   (date INTEGER)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS oldestDate
                   (date INTEGER)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS committees
                   (committeeID INTEGER PRIMARY KEY, name TEXT, industry TEXT, sector TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS committeeMembers 
                   (memberID INTEGER FORGEIN KEY, committeeID INTEGER FORGEIN KEY)''')
    
    conn.commit()
    
    #if you need to fill the database with members
    #from fillDatabase import fill_members
    #fill_members()

    #for filling the db with committees 
        #not currently working
    #from fillDatabase import fill_committees
    #fill_committees()
        
    #sets up the oldest and newest date tables
    """date = datetime.now()
    query = f'INSERT INTO newestDate (date) VALUES ({date.strftime("%Y%m%d")})'
    cursor.execute(query)
    query = f'INSERT INTO oldestDate (date) VALUES ({date.strftime("%Y%m%d")})'
    cursor.execute(query)
    conn.commit()"""
    
    
    
    print(conn.total_changes)
