import pandas as pd
from my_finance_lib.rsi import rsi

def test_rsi():
    prices = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    rsi_values = rsi(prices)
    assert not rsi_values.empty
