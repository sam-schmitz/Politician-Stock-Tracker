#testTrade.py
#By: Sam Schmitz
#test code for trade.py

import unittest
from unittest.mock import (MagicMock, patch, Mock)
import datetime

import sb.trade

def _cPrice(tick):
    if tick == 'MSFT':
        return 100
    elif tick == 'AMZN':
        return 100
    elif tick == 'AAPL':
        return 100
    return None

def _pPrice(tick, d):
    if (tick=='MSFT' or tick=='AMZN' or tick=='AAPL'):
        if d == datetime.datetime(2024, 1, 1):
            return 20
        if d == datetime.datetime(2024, 1, 15):
            return 40
        if d == datetime.datetime(2024, 1, 25):
            return 60
        if d == datetime.datetime(2024, 1, 30):
            return 80
        if d == datetime.datetime(2024, 2, 1):
            return 100
    return None

def _stock_sector(tick):
    if tick == 'MSFT':
        return 'INFORMATION TECHNOLOGY'
    return None

sb.trade.cPrice = _cPrice
sb.trade.pPrice = _pPrice
sb.trade.stock_sector = _stock_sector
from sb.trade import trade

class testTrade(unittest.TestCase):

    def setUp(self):
        self.t = trade('MSFT', 'BUY', datetime.datetime(2024, 1, 1), datetime.datetime(2024, 1, 15), 'Biden, Joe')

    def test_trade_init(self):
        self.assertEqual(self.t.tick, 'MSFT')
        self.assertEqual(self.t.saleType, 'BUY')
        self.assertEqual(self.t.dateB, datetime.datetime(2024, 1, 1))
        self.assertEqual(self.t.priceB, 20)
        self.assertEqual(self.t.dateD, datetime.datetime(2024, 1, 15))
        self.assertEqual(self.t.priceD, 40)
        self.assertEqual(self.t.member, 'Biden, Joe')
        self.assertEqual(self.t.sector, 'INFORMATION TECHNOLOGY')
        self.assertEqual(self.t.delay, 14)

    def test_trade_cPrice(self):
        self.assertEqual(self.t.cPrice(), 100)

    def test_trade_pPrice(self):
        self.assertEqual(self.t.pPrice(datetime.datetime(2024, 1, 25)), 60)