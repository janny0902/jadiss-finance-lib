# RSI(Relative Strength Index)는 기술적 분석에서 가장 널리 사용되는 모멘텀 오실레이터 지표입니다. 가격의 상승과 하락 속도를 비교하여 과매수/과매도 상태를 판단합니다.
# RSI의 계산 방법:
# 상승폭(Gain):
# 전일 대비 상승한 가격 변동의 평균을 계산합니다.
# 하락폭(Loss):
# 전일 대비 하락한 가격 변동의 평균을 계산합니다.
# RS(Relative Strength):
# 상승폭 평균을 하락폭 평균으로 나눠 값입니다.
# RSI:
# 100 - (100 / (1 + RS)) 공식으로 계산되며, 0~100 범위의 값을 가집니다.
# RSI의 특징:
# 과매수/과매도:
# 일반적으로 70 이상은 과매수, 30 이하는 과매도로 간주합니다.
# 바운드 오실레이터:
# 0~100 범위로 제한되어 있어 과도한 변동성을 방지합니다.
# 다이버전스:
# 가격과 RSI 간의 다이버전스를 통해 추세 전환 신호를 포착할 수 있습니다.
# 매매 신호:
# RSI가 70을 넘어서면 매도 고려, 30 아래로 떨어지면 매수 고려합니다.
# 50선을 기준으로 상승/하락 추세를 판단할 수 있습니다.

import pandas as pd
import numpy as np

def rsi(prices, period=14):
    """
    RSI 지표 계산
    
    입력 타입:
    prices (pd.Series): 가격 데이터 시리즈
    period (int): RSI 계산 기간 (기본값: 14)
    
    출력 타입:
    dict: {'RSI': pd.Series} - RSI 값들을 포함한 딕셔너리
    """
    delta = prices.diff(1)
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi_value = 100 - (100 / (1 + rs))
    
    # NaN 및 무한대 값 처리
    rsi_value = rsi_value.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return {
        'RSI': rsi_value
    }
