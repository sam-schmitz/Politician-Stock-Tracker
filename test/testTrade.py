#testTrade.py
#By: Sam Schmitz
#test code for trade.py

import unittest
from unittest.mock import (MagicMock, patch, Mock)

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
        if d == datetime(2024, 1, 1):
            return 20
        if d == datetime(2024, 1, 15):
            return 40
        if d == datetime(2024, 1, 25):
            return 60
        if d == datetime(2024, 1, 30):
            return 80
        if d == datetime(2024, 2, 1):
            return 100
    return None

def _stock_sector(tick):
    if tick == 'MSFT':
        return 'INFORMATION TECHNOLOGY'
    return None