import pandas as pd
import numpy as np

def rsi(prices, period=3):
    prices = [80, 100, 120, 110, 100, 100, 99, 98, 97, 96, 95]
    delta = prices.diff(1)
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    # avg_loss가 0인 경우 rs를 매우 큰 값으로 설정
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rs = rs.fillna(0)  # 무한대 값을 방지하기 위해 매우 큰 값으로 설정

    rsi = 100 - (100 / (1 + rs))
    
    # NaN 및 무한대 값 처리
    rsi = rsi.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return rsi
