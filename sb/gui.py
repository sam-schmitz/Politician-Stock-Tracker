# gui.py
# By: Sam Schmitz and Gavin Roy
# The gui for the politician stock tracker

from re import L
from congressTrades import getTrades
from fillDatabase import fill
from server import stockBotAPI
from analysis import analyze_six_months_mem, analyze_given
from tkSliderWidget import Slider, Slider_Datetime

from datetime import datetime
from datetime import date
from datetime import timedelta
    
import tkinter as tk
#from tkinter import ttk, messagebox
import ttkbootstrap as ttk
    
class tkinterApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, Page3, Page4):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
    def show_analysis(self, trades):
        frame = self.frames[Page4]
        frame.start_loading()
        frame.tkraise()
        self.update()
        frame.start_analysis(trades)
        
    def show_tree(self):
        pass
    
    def hide_tree(self):
        pass
        
class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        style = ttk.Style("darkmode")
        style.configure("TFrame", background="#121212")
        ttk.Frame.__init__(self, parent, style="TFrame")
        
        style.configure("title.TLabel", background="#121212", font=("Verdana", 35), weight="bold")
        style.configure("body.TLabel", background="#121212", foreground="#ededed", font=("Verdana", 12))
        style.configure("header.TLabel", background="#121212", foreground="#ededed", font=("Verdana", 14), weight="bold")
        style.configure("startpage.TButton",  
                        font=("Verdana", 12),
                        background="#121212"
                        )
        
        label = ttk.Label(self, text="Politician Stock Tracker", style="title.TLabel", anchor="center")
        label.grid(row=0, column=0, columnspan=5, rowspan=2, padx=10, pady=25, sticky="NESW")
        
        controller.grid_columnconfigure(1, weight=1)
        controller.grid_columnconfigure(2, weight=1)
        controller.grid_columnconfigure(3, weight=1)
        controller.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)
        
        button3 = ttk.Button(self, text="Trades",
        command = lambda : controller.show_frame(Page3),
        style="startpage.TButton")
        button3.grid(row=2, column=2, padx=15, pady=10)
        
        api = stockBotAPI()
        newestDate = api.get_newest_date()
        oldestDate = api.get_oldest_date()
        api.close()

        newestScrape1 = ttk.Label(self, text="Newest Scrape:", style="header.TLabel")
        newestScrape1.grid(row=3, column=1)
        
        newestScrape2 = ttk.Label(self, text=newestDate, style="body.TLabel")
        newestScrape2.grid(row=4, column=1)
        
        oldestScrape1 = ttk.Label(self, text="Oldest Scrape:", style="header.TLabel")
        oldestScrape1.grid(row=3, column=3, padx=10)
        
        oldestScrape2 = ttk.Label(self, text=oldestDate, style="body.TLabel")
        oldestScrape2.grid(row=4, column=3, padx=10)
        
class ComboboxSearch(ttk.Combobox):
    
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.bind("<KeyRelease>", self._filter_options)
        
    def _filter_options(self, event):
        search_term = self.get().lower()
        filtered_options = [item for item in self['values'] if search_term in item.lower()]
        self['values'] = filtered_options
   
        
class Page3(ttk.Frame):  #displays trades
    
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style="TFrame")
        style = ttk.Style()
        style.configure("m.TButton", 
                        background="#121212", 
                        foreground="#ededed", 
                        font=("Verdana", 10))
        style.configure("Page3.TButton", 
                        background="#121212", 
                        foreground="#ededed", 
                        font=("Verdana", 10))
        style.configure("saletype.on.TButton", 
                        background="#121212", 
                        foreground="#ededed", 
                        font=("Verdana", 10))
        style.configure("saletype.off.TButton", 
                        background="#bebebe", 
                        foreground="#121212", 
                        font=("Verdana", 10))
        style.configure("Treeview", 
                        background="#161616", 
                        foreground="#ededed")
        style.configure("Treeview.Heading", 
                        background="#bebebe", 
                        foreground="#121212")
        
        rowMenu = 0
        rowTitle = 1
        rowButtons = 2
        rowButtons2 = 3
        rowTable = 4
        
        self.grid_rowconfigure(rowTable, weight=1)
        self.grid_columnconfigure(1, weight=1)

        label = ttk.Label(self, text="Trades", 
                          font=("Verdana", 35), 
                          style="title.TLabel")
        label.grid(row=rowTitle, column=0, columnspan=3, 
                   padx=10, pady=10)
        
        button1 = ttk.Button(self, text="Back", 
        command = lambda : controller.show_frame(StartPage), 
        style="m.TButton")
        button1.grid(row=rowMenu, column=0, 
                     padx=10, pady=10, sticky='NW')
        
        self.treev = ttk.Treeview(self, selectmode='browse')
        self._create_treeview()
        self.treev.grid(row=rowTable, column=0, columnspan=3)
        
        self.sba = stockBotAPI()
        newest_date = self.sba.get_newest_date()
        oldest_date = self.sba.get_oldest_date()
        
        buttonAnalyze = ttk.Button(self, text='Analyze',
                                   command=lambda : controller.show_analysis(self.analysis()),
                                   style="Page3.TButton")
        buttonAnalyze.grid(row=rowButtons, column=2, 
                           padx=10, pady=10, sticky='S')
        
        buttonApplyFilters = ttk.Button(self, text='Apply Filters',
                                        command=self.display_trades,
                                        style="Page3.TButton")
        buttonApplyFilters.grid(row=rowButtons2, column=2, 
                                padx=10, pady=10, sticky="N")
        
        filters = CollapsiblePane(self)
        filters.grid(row=rowButtons, column=0, rowspan=2, sticky="W")
        rowDates = 1
        rowDelay = 2
        rowTicks = 3
        rowCompanyNames = 4
        rowTradeType = 5
        rowMember = 6
        
        #dates
        labelDate = ttk.Label(filters.frame, text="Dates:", 
                              style="body.TLabel"
                              ).grid(row=rowDates, column=2, pady=5, padx=10)
        self.dateSlider = Slider_Datetime(filters.frame, 
                                          min_val=oldest_date, 
                                          max_val=newest_date, 
                                          init_lis=[oldest_date, newest_date])
        self.dateSlider.grid(row=rowDates, column=3, columnspan=2)
        
        #delay
        labelDelay = ttk.Label(filters.frame, text="Delay:",
                               style="body.TLabel"
                               ).grid(row=rowDelay, column=2, pady=5, padx=10)
        self.delaySlider = Slider(filters.frame, 
                                  min_val=0, 
                                  max_val=50, 
                                  init_lis=[50], 
                                  step_size=1.0)
        self.delaySlider.grid(row=rowDelay, column=3, columnspan=2)
        
        self.trades = self.sba.get_all_trades()
        
        #ticks
        self.ticks = [trade['tick'] for trade in self.trades]
        labelTick = ttk.Label(filters.frame, text="Ticks:", 
                              style="body.TLabel"
                              ).grid(row=rowTicks, column=2, pady=5, padx=10)
        self.comboboxTick = ComboboxSearch(filters.frame, values=self.ticks)
        self.comboboxTick.grid(row=rowTicks, column=3, columnspan=2, 
                               sticky='ew')
        
        #company names
        self.companyNames = [trade['companyName'] for trade in self.trades]
        labelCompanyName = ttk.Label(filters.frame, text="Company Name:", 
                                     style="body.TLabel"
                                     ).grid(row=rowCompanyNames, column=2, pady=5, padx=10)
        self.comboboxCN = ComboboxSearch(filters.frame, values=self.companyNames)
        self.comboboxCN.grid(row=rowCompanyNames, column=3, columnspan=2,
                             sticky='ew')


        #trade type
        labelTradeType = ttk.Label(filters.frame, text="Trade Type:",
                                   style="body.TLabel"
                                   ).grid(row=rowTradeType, column=2, pady=5, padx=10)
        self.buyButton = tk.BooleanVar()
        self.sellButton = tk.BooleanVar()
        self.buyButton.set(True)
        self.sellButton.set(True)
        bButton = ttk.Checkbutton(filters.frame, 
                                  text="Buy", 
                                  style="saletype.on.TButton", 
                                  variable=self.buyButton)
        sButton = ttk.Checkbutton(filters.frame, 
                                  text="Sell", 
                                  style="saletype.on.TButton", 
                                  variable=self.sellButton)
        bButton.grid(row=rowTradeType, column=3, 
                     pady=5, padx=10)
        sButton.grid(row=rowTradeType, column=4, 
                     pady=5, padx=10)
        
        #members
        labelMembers = ttk.Label(filters.frame, 
                                 text="Members:", 
                                 style="body.TLabel"
                                 ).grid(row=rowMember, column=2, 
                                        padx=10, pady=5)
        self.memberNames = self.sba.get_all_members()
        self.memberNames = ["all"] + self.memberNames
        self.comboboxMembers = ComboboxSearch(filters.frame, 
                                              values = self.memberNames)
        self.comboboxMembers.grid(row=rowMember, column=3, columnspan=2)
        """self.selected_member = tk.StringVar(filters.frame)
        self.selected_member.set("all")
        self.member_selecter = tk.OptionMenu(filters.frame, self.selected_member, *self.memberNames)
        self.member_selecter.grid(row=rowMember, column=3, pady=5, padx=10)"""
        
        self.display_trades()

        
    def display_trades(self):
        self._update_filter()
        self.treev.delete(*self.treev.get_children())
        for trade in self.trades:
            if self.filter_trade(trade):
                trade['id'] = self.treev.insert("", 'end',
                                                text="L",
                        values = (trade["tick"], 
                                  trade["saleType"], 
                                  trade["member"], 
                                  trade['dateDis'].strftime("%m-%d-%Y"), 
                                  trade['dateB'].strftime("%m-%d-%Y"), 
                                  trade['delay'], 
                                  trade['companyName'])
                        )
        
    def filter_trade(self, trade):
        if trade['dateDis'] > self.filter['d1']:
            return False
        if trade['dateDis'] < self.filter['d2']:
            return False
        if trade['delay'] > self.filter['delay']:
            return False
        if self.filter['tick'] != '':
            if self.filter['tick'] not in trade['tick']: 
                return False
        if self.filter['companyName'] != '':
            if self.filter['companyName'] not in trade['companyName']:
                return False
        if trade['saleType'] == 'BUY':
            if self.filter['buy'] == False:
                return False
        elif trade['saleType'] == 'SELL':
            if self.filter['sell'] == False:
                return False
        if self.filter['member'] != '' or self.filter['member'] != 'all':
            if self.filter['member'] not in trade['member']:
                return False
        return True
    
    def analysis(self):
        self.display_trades()
        t = []
        self._update_filter()
        for trade in self.trades:
            if self.filter_trade(trade):
                t.append(trade)
        return t
        analysis = analyze_given(t)
        if analysis == None:
            messagebox.showinfo(
                message="No trades found in the timeframe",
                title='Results')
        else:
            messagebox.showinfo(
                message=f"The average gain is: {analysis[0]}\n The average gain after disclosure is: {analysis[1]}",
                title="Results")
            
    def _update_filter(self):
        dateSliderValues = self.dateSlider.getValues()
        self.filter = {'d1' : dateSliderValues[1],
                       'd2' : dateSliderValues[0],
                       'delay' : self.delaySlider.getValues()[0],
                       'tick' : self.comboboxTick.get(),
                       'companyName': self.comboboxCN.get(),
                       'member' : self.comboboxMembers.get(),
                       'buy' : self.buyButton.get(),
                       'sell': self.sellButton.get()}
        print(self.filter)
            
    def _hide_trade(self, id):
        self.tree.detach(id)
    
    def _unhide_trade(self, id):
        self.tree.reattach(id, '', 0)   #0 == position where the row is reattached to
        
    def _create_treeview(self):
        verscrlbar = ttk.Scrollbar(self, orient="vertical", command=self.treev.yview)
        self.treev.configure(xscrollcommand = verscrlbar.set)
        self.treev["columns"] = ("1", "2", "3", "4", "5", "6", "7")
        self.treev['show'] = 'headings'
        self.treev.column("1", width=90, anchor='c')
        self.treev.column("2", width=90, anchor='se')
        self.treev.column("3", width=90, anchor='se')
        self.treev.column("4", width=90, anchor='se')
        self.treev.column("5", width=90, anchor='se')
        self.treev.column("6", width=90, anchor='se')
        self.treev.column("7", width=90, anchor='se')
        self.treev.heading("1", text="Tick")
        self.treev.heading("2", text="Sale Type")
        self.treev.heading("3", text="Member")
        self.treev.heading("4", text="Date Disclosed")
        self.treev.heading("5", text="Date Bought")
        self.treev.heading("6", text="Delay")
        self.treev.heading("7", text="Company Name")
             
    def _on_select(self, event):
        selected_item = self.comboboxTick.get()
        self.entry_var.set(selected_item)
        
class Page4(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.sba = stockBotAPI()
        
        style = ttk.Style()
        style.configure("subtitle.TLabel", font=("Verdana", 25))
        
        rowMenu = 1
        rowTitle = 2
        rowDetails = 3
        rowTable = 4

        self.grid_rowconfigure(rowTable, weight=1)
        
        button1 = ttk.Button(self, text="Back", 
        command = lambda : controller.show_frame(Page3),
        style="Page3.TButton")
        button1.grid(row=rowMenu, column=1, 
                     padx=10, pady=10, sticky='NW')
        
        labelTitle = ttk.Label(self, text="Analysis", style="title.TLabel")
        labelTitle.grid(row=rowTitle, column=1, columnspan=2, 
                        padx=10, pady=10)
        
        self.labelDetails = ttk.Label(self, text="", style="body.TLabel")
        self.labelDetails.grid(row=rowDetails, column=1,
                               padx=10, pady=10, sticky="W")
        
        self._create_treeview()
        self.treev.grid(row=rowTable, column=1, columnspan=2,
                        padx=10, pady=10)
        
    def start_analysis(self, trades):
        analysis = analyze_given(trades)
        
        totalGainB = analysis[0]*analysis[3]
        totalGainD = analysis[1]*analysis[3]

        displayText = f"""Average proft gained per trade: {analysis[0]}
Average profit gained per trade after disclosure: {analysis[1]}
Total amount invested: ${round(analysis[2], 2)}
Total profit gained: {round(totalGainB, 2)}
Total profit gained after disclosure: {round(totalGainD, 2)}
% gain overall: {round((totalGainB/analysis[2])*100, 2)}%
% gain after disclosure: {round((totalGainD/analysis[2])*100, 2)}%
Biggest Earner: {analysis[4]['tick']} ${analysis[4]['size']} {analysis[4]['member']} {analysis[4]['dateB']}"""
        
        self.labelLoading.grid_remove()
        self.labelDetails.grid(row=3, column=1, columnspan=2,
                               padx=10, pady=10)
        self.labelDetails.config(text=displayText)
        for trade in analysis[5]:
            if self.filter_trade(trade):
                trade['id'] = self.treev.insert("", 'end', text="L",
                        values = (trade["tick"],
                                  trade["saleType"],
                                  trade["member"],
                                  round(trade['priceC'], 2),
                                  trade['dateB'].strftime("%m-%d-%Y"),
                                  trade['priceB'],
                                  round(trade['gainB'], 2)
                            ))
        
    def start_loading(self):
        self.labelDetails.grid_remove()
        self.labelLoading = ttk.Label(self, text="Loading...", style="subtitle.TLabel")
        self.labelLoading.grid(row=3, column=1, columnspan=2)
        
    def filter_trade(self, trade):
        #might evenutally add in filters for the table
        return True
        
    def _create_treeview(self):
        self.treev = ttk.Treeview(self, selectmode='browse')
        verscrlbar = ttk.Scrollbar(self, orient="vertical", command=self.treev.yview)
        self.treev.configure(xscrollcommand = verscrlbar.set)
        self.treev["columns"] = ("1", "2", "3", "4", "5", "6", "7")
        self.treev['show'] = 'headings'
        self.treev.column("1", width=90, anchor='c')
        self.treev.column("2", width=90, anchor='se')
        self.treev.column("3", width=90, anchor='se')
        self.treev.column("4", width=90, anchor='se')
        self.treev.column("5", width=90, anchor='se')
        self.treev.column("6", width=90, anchor='se')
        self.treev.column("7", width=90, anchor='se')
        self.treev.heading("1", text="Tick")
        self.treev.heading("2", text="Sale Type")
        self.treev.heading("3", text="Member")
        self.treev.heading("4", text="Current Price")
        self.treev.heading("5", text="Date Bought")
        self.treev.heading("6", text="Price Bought")
        self.treev.heading("7", text="Gain After Bought")
        
        
        
        
    
                
 
class CollapsiblePane(ttk.Frame):
    
    def __init__(self, parent, expanded_text="Filters <<", collapsed_text="Filters >>"):
        style = ttk.Style()
        ttk.Frame.__init__(self, parent, style="cp.TFrame")
        self.parent = parent
        self._expanded_text = expanded_text
        self._collapsed_text = collapsed_text
        self.columnconfigure(1, weight=1)
        
        
        style.configure("cp.TCheckbutton", font=("Verdana", 12), background="#121212")
        style.configure("cp.TSeparator")
        style.configure("cp.TButton")

        self._variable = tk.IntVar()
        self._button = ttk.Checkbutton(self, variable=self._variable,
                                       command = self._activate, style="cp.TButton")
        self._button.grid(row=0, column=0)
        self._seperator = ttk.Separator(self, orient="horizontal", style="cp.TSeparator")
        self._seperator.grid(row=0, column=1, sticky="we")
        self.frame = ttk.Frame(self, style="cp.TFrame")
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