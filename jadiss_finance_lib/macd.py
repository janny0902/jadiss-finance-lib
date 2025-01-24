import pandas as pd
import numpy as np

def macd(prices, slow=26, fast=12, signal=9):
    exp1 = prices.ewm(span=fast, adjust=False).mean()
    exp2 = prices.ewm(span=slow, adjust=False).mean()
    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    
    # NaN 및 무한대 값 처리
    macd_line = macd_line.replace([np.inf, -np.inf], np.nan).fillna(0)
    signal_line = signal_line.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return macd_line, signal_line
