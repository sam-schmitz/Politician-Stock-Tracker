# gui.py
# By: Sam Schmitz and Gavin Roy
# The gui for the politician stock tracker

from genericpath import samefile
from tkinter import *
from typing import Container

from congressTrades import getTrades
from fillDatabase import fill

from datetime import datetime
from datetime import date
from datetime import timedelta
    
import tkinter as tk
from tkinter import ttk
    
class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, Page1, Page2):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Startpage", font=("Verdana", 35))
        label.grid(row=0, column=4, padx=10, pady=10)
        
        button1 = ttk.Button(self, text="Page 1",
        command = lambda : controller.show_frame(Page1))
        button1.grid(row=1, column=1, padx=10, pady=10)
        
        button2 = ttk.Button(self, text="Page 2",
        command = lambda : controller.show_frame(Page2))
        button2.grid(row=2, column=1, padx=10, pady=10)
        
class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 1", font=("Verdana", 35))
        label.grid(row=0, column=4, padx=10, pady=10)
        
        button1 = ttk.Button(self, text="StartPage", 
        command = lambda : controller.show_frame(StartPage))
        button1.grid(row=1, column=1, padx=10, pady=10)
        
        button2 = ttk.Button(self, text="Page 2", 
        command = lambda : controller.show_frame(Page2))
        button2.grid(row=2, column=2, padx=10, pady=10)
        
        def getAllClicked():
            d = date.today()-timedelta(days=3)
            print("fill called with: ", datetime.now(), datetime(d.year, d.month, d.day))
            #fill(datetime.now, datetime(d.year, d.month, d.day))

        buttonGetAll = ttk.Button(self, text="Get All", command = getAllClicked)
        buttonGetAll.grid(row=1, column=4, padx=10, pady=10)
                
        
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 2", font=("Verdana", 35))
        label.grid(row=0, column=4, padx=10, pady=10)
        
        button1 = ttk.Button(self, text="Page 1", 
        command = lambda : controller.show_frame(Page1))
        button1.grid(row=1, column=1, padx=10, pady=10)
        
        button2 = ttk.Button(self, text="Startpage", 
        command = lambda : controller.show_frame(StartPage))
        button2.grid(row=2, column=2, padx=10, pady=10)
        
if __name__ == "__main__":
    app = tkinterApp()
    app.mainloop()
    """#set up the tkinter window
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

    root.mainloop() # runs root"""
        
