#testTrade.py
#By: Sam Schmitz
#test code for trade.py

import unittest
from unittest.mock import (MagicMock, patch, Mock)
import datetime

import sb.trade

def _stock_sector(tick):
    if tick == 'MSFT':
        return 'INFORMATION TECHNOLOGY'
    return None

def history_side_effect(start=None, end=None):
    if start == "2024-01-01":
        return ({'Open': [20.1342], 'Close': [100.001]})
    elif start == "2024-01-15":
        return ({'Open': [40.5467], 'Close': [100.001]})
    elif start == "2024-01-25":
        return ({'Open': [60.874], 'Close': [100.001]})
    elif (start==None) and (end==None):
        return ({'Open': [98.738, 99.32], 'Close': [97.234, 100.001]})
    
def ticker_side_effect(name):
    if name == 'MSFT':
        ticker_mock = MagicMock()
        ticker_mock.history.side_effect = history_side_effect()
        return ticker_mock

sb.trade.stock_sector = _stock_sector
from sb.trade import trade

class testTrade(unittest.TestCase):
    
    @patch('sb.trade.yf')

    def setUp(self, mock_yf):
        ticker_mock = MagicMock()
        ticker_mock.history.side_effect = history_side_effect
        mock_yf.Ticker.return_value = ticker_mock
        self.mock = ticker_mock
        self.t = trade('MSFT', 'BUY', datetime.datetime(2024, 1, 1), datetime.datetime(2024, 1, 15), 'Biden, Joe')

    def test_trade_init(self):
        print(self.t.yf.history())
        self.assertEqual(self.t.tick, 'MSFT')
        self.assertEqual(self.t.yf, self.mock)
        self.assertEqual(self.t.saleType, 'BUY')
        self.assertEqual(self.t.dateB, datetime.datetime(2024, 1, 1))
        self.assertEqual(self.t.priceB, 20.13)
        self.assertEqual(self.t.dateD, datetime.datetime(2024, 1, 15))
        self.assertEqual(self.t.priceD, 40.55)
        self.assertEqual(self.t.member, 'Biden, Joe')
        self.assertEqual(self.t.sector, 'INFORMATION TECHNOLOGY')
        self.assertEqual(self.t.delay, 14)

    def test_trade_cPrice(self):
        self.assertEqual(self.t.cPrice(), 100.00)

    def test_trade_pPrice(self):
        self.assertEqual(self.t.pPrice(datetime.datetime(2024, 1, 25)), 60.87)
        self.assertEqual(self.t.pPrice(datetime.datetime(2024, 1, 1)), 20.13)
        self.assertEqual(self.t.pPrice(datetime.datetime(2024, 1, 15)), 40.55)