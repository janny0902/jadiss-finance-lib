import pandas as pd
from jadiss_finance_lib.rsi import rsi

def test_rsi():
    prices = pd.Series([100, 101, 102, 101, 100, 98, 99, 100, 101, 102])
    rsi_values = rsi(prices)
    assert not rsi_values.empty
