import pandas as pd
from my_finance_lib.macd import macd

def test_macd():
    prices = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    macd_line, signal_line = macd(prices)
    assert not macd_line.empty
    assert not signal_line.empty
