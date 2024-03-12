# gui.py
# By: Sam Schmitz and Gavin Roy
# The gui for the politician stock tracker

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
        
    def show_tree(self):
        pass
    
    def hide_tree(self):
        pass
        
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
        
        def getCurrentClicked():
            d1 = date.today()
            d2 = d1-timedelta(days=3)
            print("fill called with: ", datetime(d1.year, d1.month, d1.day), datetime(d2.year, d2.month, d2.day))
            trades = fill(datetime(d1.year, d1.month, d1.day), datetime(d2.year, d2.month, d2.day))
            for trade in trades:
                self.treev.insert("", 'end', text="L",
                             values = (trade.tick, trade.saleType, trade.member))

        buttonGetAll = ttk.Button(self, text="Get Current", command = getCurrentClicked)
        buttonGetAll.grid(row=1, column=4, padx=10, pady=10)
        
        self.treev = ttk.Treeview(self, selectmode='browse')
        self.treev.grid(row=3, column=4)
        #treev.pack(side='right')
        verscrlbar = ttk.Scrollbar(self, orient="vertical", command=self.treev.yview)
        #verscrlbar.pack(side='right', fill='x')
        self.treev.configure(xscrollcommand = verscrlbar.set)
        self.treev["columns"] = ("1", "2", "3")
        self.treev['show'] = 'headings'
        self.treev.column("1", width=90, anchor='c')
        self.treev.column("2", width=90, anchor='se')
        self.treev.column("3", width=90, anchor='se')
        self.treev.heading("1", text="Tick")
        self.treev.heading("2", text="Sale Type")
        self.treev.heading("3", text="Member")
        
                
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