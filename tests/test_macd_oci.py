import pytest
import pandas as pd
import numpy as np
from jadiss_finance_lib.macd_oci import macd_oci

def test_macd_oci():
    prices = pd.Series([100, 101, 102, 101, 100, 98, 99, 100, 101, 102])
    macd, signal_line, oci = macd_oci(prices)
    assert not macd.empty
    assert not signal_line.empty
    assert not oci.empty
