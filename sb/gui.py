# gui.py
# By: Sam Schmitz and Gavin Roy
# The gui for the politician stock tracker

from congressTrades import getTrades
from fillDatabase import fill
from server import stockBotAPI
from analysis import analyze_six_months_mem, analyze_given
from tkSliderWidget import Slider, Slider_Datetime

from datetime import datetime
from datetime import date
from datetime import timedelta
    
import tkinter as tk
from tkinter import ttk, messagebox
    
class tkinterApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #10 x 10
        
        self.frames = {}
        
        for F in (StartPage, Page1, Page2, Page3):
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
        label.grid(row=0, column=0, columnspan=5, rowspan=2, padx=10, pady=10)
        
        #button1 = ttk.Button(self, text="Page 1",
        #command = lambda : controller.show_frame(Page1))
        #button1.grid(row=1, column=1, padx=10, pady=10)
        
        button2 = ttk.Button(self, text="Ananlysis",
        command = lambda : controller.show_frame(Page2))
        button2.grid(row=2, column=1, padx=10, pady=10)
        
        button3 = ttk.Button(self, text="Trades",
        command = lambda : controller.show_frame(Page3))
        button3.grid(row=2, column=3, padx=10, pady=10)
        
        api = stockBotAPI()
        newestDate = api.get_newest_date()
        oldestDate = api.get_oldest_date()
        api.close()

        newestScrape1 = ttk.Label(self, text="Newest Scrape:")
        newestScrape1.grid(row=3, column=1)
        
        newestScrape2 = ttk.Label(self, text=newestDate)
        newestScrape2.grid(row=4, column=1)
        
        oldestScrape1 = ttk.Label(self, text="Oldest Scrape:")
        oldestScrape1.grid(row=3, column=3)
        
        oldestScrape2 = ttk.Label(self, text=oldestDate)
        oldestScrape2.grid(row=4, column=3)
        
class Page1(tk.Frame):  #scrapes for new data
    
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
        verscrlbar = ttk.Scrollbar(self, orient="vertical", command=self.treev.yview)
        self.treev.configure(xscrollcommand = verscrlbar.set)
        self.treev["columns"] = ("1", "2", "3")
        self.treev['show'] = 'headings'
        self.treev.column("1", width=90, anchor='c')
        self.treev.column("2", width=90, anchor='se')
        self.treev.column("3", width=90, anchor='se')
        self.treev.heading("1", text="Tick")
        self.treev.heading("2", text="Sale Type")
        self.treev.heading("3", text="Member")
        
                
class Page2(tk.Frame):  #data analysis page
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        rowTitle = 1
        label = ttk.Label(self, text="Analysis", font=("Verdana", 35))
        label.grid(row=rowTitle, column=0, columnspan=4, padx=10, pady=10)
        
        #button1 = ttk.Button(self, text="Page 1", 
        #command = lambda : controller.show_frame(Page1))
        #button1.grid(row=1, column=1, padx=10, pady=10)
        
        rowMenu = 0
        button2 = ttk.Button(self, text="Back", 
        command = lambda : controller.show_frame(StartPage))
        button2.grid(row=rowMenu, column=0, padx=10, pady=10)
        
        def analyze_selection():
            selection = combo.get()
            d = dateSelector.get()
            dateConverter = {"all" : None,
                             "1 Day" : date.today()-timedelta(days=1),
                             "1 Month" : date.today()-timedelta(days=30),
                             "6 Months": date.today()-timedelta(days=180)}
            d = dateConverter[d]
            analysis = analyze_six_months_mem(selection, d)
            if analysis == None:
                messagebox.showinfo(
                    message="No trades found in the timeframe",
                    title='Results')
            else:
                messagebox.showinfo(
                    message=f"The average gain from trades for {selection} is: {analysis[0]}\n The average gain after disclosure is: {analysis[1]}",
                    title="Results")

        rowAnalysisLabels = 2
        labelMembers = ttk.Label(self, text="Member:")
        labelMembers.grid(row=rowAnalysisLabels, column=0)
        
        labelDate = ttk.Label(self, text="Date:")
        labelDate.grid(row=rowAnalysisLabels, column=1)

        rowAnalysisButtons = 3
        buttonAnalyze = ttk.Button(self, text="Display Selection",
                            command=analyze_selection)
        buttonAnalyze.grid(row=rowAnalysisButtons, column=2, padx=10, pady=5)
        
        sba = stockBotAPI()
        members = sba.get_all_members()
        members = ['all'] + members
        sba.close()

        combo = ttk.Combobox(
            self, 
            state="readonly",
            values=members)
        combo.current(0)
        combo.grid(row=rowAnalysisButtons, column=0, padx=10, pady=5)
        
        dateOptions = ["all","1 Day", "1 Month", "6 Months"]
        dateSelector = ttk.Combobox(self,
                                    state="readonly",
                                    values=dateOptions)
        dateSelector.current(0)
        dateSelector.grid(row=rowAnalysisButtons, column=1, padx=10, pady=5)
        
        
        
class Page3(tk.Frame):  #displays trades
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        rowMenu = 0
        rowTitle = 1
        rowButtons = 2
        rowTable = 3
        label = ttk.Label(self, text="Trades", font=("Verdana", 35))
        label.grid(row=rowTitle, column=0, columnspan=2, padx=10, pady=10)
        
        button1 = ttk.Button(self, text="Back", 
        command = lambda : controller.show_frame(StartPage))
        button1.grid(row=rowMenu, column=0, padx=10, pady=10)
        
        self._create_treeview()
        self.treev.grid(row=rowTable, column=0, columnspan=2)
        
        self.sba = stockBotAPI()
        newest_date = self.sba.get_newest_date()
        oldest_date = self.sba.get_oldest_date()
        self.filter = {'d1' : newest_date,
                       'd2' : oldest_date}
        self.trades = self.sba.get_all_trades()
        self.display_trades()
        
        buttonAnalyze = ttk.Button(self, text='Analyze',
                                   command=self.analysis)
        buttonAnalyze.grid(row=rowButtons, column=1, padx=10, pady=10)
        
        filters = CollapsiblePane(self)
        filters.grid(row=rowButtons, column=0)
        labelDate = ttk.Label(filters.frame, text="Dates:").grid(row=1, column=2, pady=10)
        dateslider = Slider_Datetime(filters.frame, min_val=oldest_date, max_val=newest_date, init_lis=[oldest_date, newest_date]).grid(row=1, column=3)

        
    def display_trades(self):
        self.treev.delete(*self.treev.get_children())
        for trade in self.trades:
            if self.filter_trade(trade):
                trade['id'] = self.treev.insert("", 'end', text="L",
                        values = (trade["tick"], trade["saleType"], trade["member"], trade['dateDis'], trade['dateB']))
        
    def filter_trade(self, trade):
        if trade['dateDis'] > self.filter['d1']:
            return False
        if trade['dateDis'] < self.filter['d2']:
            return False
        return True
    
    def analysis(self):
        t = []
        for trade in self.trades:
            if self.filter_trade(trade):
                t.append(trade)
        analysis = analyze_given(t)
        if analysis == None:
            messagebox.showinfo(
                message="No trades found in the timeframe",
                title='Results')
        else:
            messagebox.showinfo(
                message=f"The average gain is: {analysis[0]}\n The average gain after disclosure is: {analysis[1]}",
                title="Results")
            
    def _hide_trade(self, id):
        self.tree.detach(id)
    
    def _unhide_trade(self, id):
        self.tree.reattach(id, '', 0)   #0 == position where the row is reattached to
        
    def _create_treeview(self):
        self.treev = ttk.Treeview(self, selectmode='browse')
        verscrlbar = ttk.Scrollbar(self, orient="vertical", command=self.treev.yview)
        self.treev.configure(xscrollcommand = verscrlbar.set)
        self.treev["columns"] = ("1", "2", "3", "4", "5")
        self.treev['show'] = 'headings'
        self.treev.column("1", width=90, anchor='c')
        self.treev.column("2", width=90, anchor='se')
        self.treev.column("3", width=90, anchor='se')
        self.treev.column("4", width=90, anchor='se')
        self.treev.column("5", width=90, anchor='se')
        self.treev.heading("1", text="Tick")
        self.treev.heading("2", text="Sale Type")
        self.treev.heading("3", text="Member")
        self.treev.heading("4", text="Date Disclosed")
        self.treev.heading("5", text="Date Bought")
                
 
class CollapsiblePane(ttk.Frame):
    
    def __init__(self, parent, expanded_text="Filters <<", collapsed_text="Filters >>"):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self._expanded_text = expanded_text
        self._collapsed_text = collapsed_text
        self.columnconfigure(1, weight=1)
        self._variable = tk.IntVar()
        self._button = ttk.Checkbutton(self, variable=self._variable,
                                       command = self._activate, style="TButton")
        self._button.grid(row=0, column=0)
        self._seperator = ttk.Separator(self, orient="horizontal")
        self._seperator.grid(row=0, column=1, sticky="we")
        self.frame = ttk.Frame(self)
        self._activate()
        
    def _activate(self):
        if not self._variable.get():
            self.frame.grid_forget()
            self._button.configure(text=self._collapsed_text)
        elif self._variable.get():
            self.frame.grid(row=1, column=0, columnspan=2)
            self._button.configure(text=self._expanded_text)
            
    def toggle(self):
        self._variable.set(not self._variable.get())
        self._activate()
        
if __name__ == "__main__":
    app = tkinterApp()
    app.mainloop()