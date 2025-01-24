import pytest
import pandas as pd
import numpy as np
from jadiss_finance_lib.macd_oci import macd_oci

def test_macd_oci():
    prices = [45.15, 46.23, 47.15, 48.05, 47.78, 48.30, 47.92, 48.28, 48.80, 48.50, 49.10, 49.32, 48.97, 49.45, 49.72, 49.94, 50.05, 50.38, 50.57, 50.79, 50.98]

    macd, signal_line, oci = macd_oci(prices)

    assert isinstance(macd, pd.Series), "MACD should be a pandas Series"
    assert isinstance(signal_line, pd.Series), "Signal Line should be a pandas Series"
    assert isinstance(oci, pd.Series), "OCI should be a pandas Series"

    assert not macd.isnull().values.any(), "MACD should not contain NaN values"
    assert not signal_line.isnull().values.any(), "Signal Line should not contain NaN values"
    assert not oci.isnull().values.any(), "OCI should not contain NaN values"

