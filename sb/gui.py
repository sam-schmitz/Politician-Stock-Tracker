# gui.py
# By: Sam Schmitz and Gavin Roy
# The gui for the politician stock tracker

from tkinter import *

from congressTrades import getTrades

from datetime import datetime
from datetime import date
from datetime import timedelta

if __name__ == "__main__":
    #set up the tkinter window
    root = Tk()
    root.title("Politician Stock Tracker")
    root.geometry('700x400')
    #make the first label
    lbl = Label(root, text = "Stocks:")
    lbl.grid(column=0, row=1)
    #lbGetAll displays the results of getAll
    lblGetAll = Label(root, text="")
    lblGetAll.grid(column=1, row=1)
    
    def getAllClicked():    #allows the getAll button to grab all the trades from the last 3 days
        d = date.today()-timedelta(days=3)
        ticks = []
        for t in getTrades(datetime(d.year, d.month, d.day)):
            ticks.append(t.tick)
        lblGetAll.configure(text = str(ticks))
    # creates the button for getAll
    getAllbtn = Button(root, text="Get recent trades", fg = "red", command=getAllClicked)
    getAllbtn.grid(column=0, row=0)
    
    def getOneClicked():    # action for getOne
        d = date.today()-timedelta(days=180)    # checks the past ~6 months
        ticks = []
        for t in getTrades(datetime(d.year, d.month, d.day), entryGetOne.get()):
            ticks.append(t.tick)
            lblGetOne.configure(text = str(ticks))
    # entryGetOne holds the name to be scraped
    entryGetOne = Entry(root, width=20)
    getOnebtn = Button(root, text="Get recent trades for member", fg="red", command=getOneClicked)
    entryGetOne.grid(column=0, row=2)
    getOnebtn.grid(column=1, row=2)
    # lblGetOne displays the results of getOne
    lblGetOne = Label(root, text="")
    lblGetOne.grid(column=0, row=3)

    root.mainloop() # runs root
