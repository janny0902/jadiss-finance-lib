import pandas as pd
import numpy as np

def macd_oci(prices, short_window=12, long_window=26, signal_window=9):
    prices = pd.Series(prices)

    # 단기 EMA
    short_ema = prices.ewm(span=short_window, adjust=False).mean()
    # 장기 EMA
    long_ema = prices.ewm(span=long_window, adjust=False).mean()

    # MACD 계산
    macd = short_ema - long_ema

    # Signal Line 계산
    signal_line = macd.ewm(span=signal_window, adjust=False).mean()

    # OCI (Option Chain Indicator) 계산
    oci = macd - signal_line
    
    # NaN 및 무한대 값 처리
    macd = macd.replace([np.inf, -np.inf], np.nan).fillna(0)
    signal_line = signal_line.replace([np.inf, -np.inf], np.nan).fillna(0)
    oci = oci.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return macd, signal_line, oci
