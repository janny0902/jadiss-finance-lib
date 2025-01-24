import pandas as pd
from jadiss_finance_lib.macd import macd

def test_macd():
    prices = pd.Series([100, 101, 102, 101, 100, 98, 99, 100, 101, 102])
    macd_line, signal_line = macd(prices)
    assert not macd_line.empty
    assert not signal_line.empty
