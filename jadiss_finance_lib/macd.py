# MACD(Moving Average Convergence Divergence)는 기술적 분석에서 가장 널리 사용되는 모멘텀 지표 중 하나입니다. 두 개의 지수이동평균(EMA) 간의 관계를 분석하여 추세의 변화와 매매 신호를 포착합니다.
# MACD의 구성 요소:
# MACD Line:
# 단기 EMA(일반적으로 12일)에서 장기 EMA(일반적으로 26일)를 뺀 값입니다. 이 선이 0선 위에 있으면 상승 추세, 아래에 있으면 하락 추세를 나타냅니다.
# Signal Line:
# MACD Line의 EMA(일반적으로 9일)입니다. MACD Line과의 교차점에서 매매 신호를 생성합니다.
# Histogram:
# MACD Line에서 Signal Line을 뺀 값으로, 두 선 간의 차이를 막대그래프로 표현합니다. 히스토그램이 0선을 교차할 때 추세 변화의 조기 신호를 제공합니다.
# MACD의 특징:
# 추세 추종:
# 이동평균을 기반으로 하여 추세의 방향과 강도를 파악할 수 있습니다.
# 지연성:
# 이동평균의 특성상 가격 변화에 다소 늦게 반응합니다.
# 다양한 신호:
# 선의 교차, 0선 돌파, 다이버전스 등 다양한 방식으로 신호를 해석할 수 있습니다.
# 매매 신호:
# MACD Line이 Signal Line을 상향 돌파하면 매수 신호, 하향 돌파하면 매도 신호로 해석됩니다.
# MACD Line이 0선을 상향 돌파하면 강세 확인, 하향 돌파하면 약세 확인 신호입니다.

import pandas as pd
import numpy as np

def macd(prices, fast=12, slow=26, signal=9):
    """
    MACD 지표 계산
    
    입력 타입:
    prices (pd.Series): 가격 데이터 시리즈
    fast (int): 단기 EMA 기간 (기본값: 12)
    slow (int): 장기 EMA 기간 (기본값: 26)
    signal (int): 시그널 라인 기간 (기본값: 9)
    
    출력 타입:
    dict: {'MACD': pd.Series, 'Signal': pd.Series, 'Histogram': pd.Series} - MACD 지표들을 포함한 딕셔너리
    """
    fast_ema = prices.ewm(span=fast, adjust=False).mean()
    slow_ema = prices.ewm(span=slow, adjust=False).mean()
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    
    # NaN 및 무한대 값 처리
    macd_line = macd_line.replace([np.inf, -np.inf], np.nan).fillna(0)
    signal_line = signal_line.replace([np.inf, -np.inf], np.nan).fillna(0)
    histogram = histogram.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return {
        'MACD': macd_line,
        'Signal': signal_line,
        'Histogram': histogram
    }
