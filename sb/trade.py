#trade.py
#By: Sam Schmitz
#contains the trade class

from stockChecker import cPrice, pPrice, stock_sector
import datetime

class trade:

	def __init__(self, tick, saleType, dateBought, dateDis, member):
		self.tick = tick
		self.saleType = saleType
		self.dateB = dateBought	#date bought
		self.priceB = pPrice(self.tick, self.dateB)
		self.dateD = dateDis	#date disclosed
		self.priceD = pPrice(self.tick, self.dateD)
		self.member = member
		self.sector = stock_sector(self.tick)
		self.delay = int((self.dateD - self.dateB).days)

	def cPrice(self):
		return cPrice(self.tick)

	def pPrice(self, d):
		return pPrice(self.tick, d)