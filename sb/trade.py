#trade.py
#By: Sam Schmitz
#contains the trade class

import datetime
import yfinance as yf

class trade:

	def __init__(self, tick, saleType, dateBought, dateDis, member, size):
		self.tick = tick
		self.yf = yf.Ticker(self.tick)
		self.saleType = saleType
		self.dateB = dateBought	#date bought
		self.priceB = self.pPrice(self.dateB)
		self.dateD = dateDis	#date disclosed
		self.priceD = self.pPrice(self.dateD)
		self.member = member
		self.delay = int((self.dateD - self.dateB).days)
		info = self.yf.get_info()
		#problems with ETFs
		self.sector = info['sector']
		self.industry = info['industry']
		self.size = size	#1->1K-15K 2->15K-50K 3->50K-250K 4->250K-500K 5->500K-1M

	def cPrice(self):
		data =  self.yf.history()
		print(data)
		return round(data["Close"][-1], 2)

	def pPrice(self, d):
		start = d.strftime("%Y-%m-%d")
		d2 = d + datetime.timedelta(days=1)
		end = d2.strftime("%Y-%m-%d")
		df = self.yf.history(start=start, end=end)
		return round(df['Open'][0], 2)
	
if __name__ == "__main__":
	test = trade('MSFT', 'BUY', datetime.datetime(2023, 1, 5), datetime.datetime(2023, 1, 3), 'Biden, Joe', 3)
	print("cPrice:", test.cPrice())
	print("pPrice: ", test.pPrice(datetime.datetime(2024, 1, 2)))