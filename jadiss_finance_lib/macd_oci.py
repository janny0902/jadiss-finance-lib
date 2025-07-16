# MACD OCI(Option Chain Indicator)는 기본 MACD 지표에 OCI 개념을 추가한 변형 지표입니다. OCI는 MACD Line과 Signal Line 간의 차이를 나타내며, 이는 일반적인 MACD Histogram과 동일한 개념입니다.
# MACD OCI의 구성 요소:
# MACD Line:
# 단기 EMA에서 장기 EMA를 뺀 값으로, 추세의 방향과 강도를 나타냅니다.
# Signal Line:
# MACD Line의 지수이동평균으로, 보다 부드러운 신호를 제공합니다.
# OCI (Option Chain Indicator):
# MACD Line에서 Signal Line을 뺀 값으로, 두 선 간의 발산 정도를 측정합니다. 양수일 때는 상승 모멘텀, 음수일 때는 하락 모멘텀을 나타냅니다.
# MACD OCI의 특징:
# 모멘텀 분석:
# OCI를 통해 추세의 모멘텀 변화를 더 세밀하게 분석할 수 있습니다.
# 조기 신호:
# OCI의 변화를 통해 MACD Line과 Signal Line의 교차를 예측할 수 있습니다.
# 발산 분석:
# 두 선 간의 발산과 수렴 패턴을 분석하여 추세 전환점을 파악합니다.
# 매매 신호:
# OCI가 0선을 상향 돌파하면 매수 신호, 하향 돌파하면 매도 신호로 해석할 수 있습니다.
# OCI의 극값에서 반전 신호를 찾을 수 있습니다.

import pandas as pd
import numpy as np

def macd_oci(prices, fast=12, slow=26, signal=9):
    """
    MACD OCI 지표 계산
    
    입력 타입:
    prices (pd.Series): 가격 데이터 시리즈
    fast (int): 단기 EMA 기간 (기본값: 12)
    slow (int): 장기 EMA 기간 (기본값: 26)
    signal (int): 시그널 라인 기간 (기본값: 9)
    
    출력 타입:
    dict: {'MACD': pd.Series, 'Signal': pd.Series, 'OCI': pd.Series} - MACD OCI 지표들을 포함한 딕셔너리
    """
    prices = pd.Series(prices)
    
    fast_ema = prices.ewm(span=fast, adjust=False).mean()
    slow_ema = prices.ewm(span=slow, adjust=False).mean()
    macd = fast_ema - slow_ema
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    oci = macd - signal_line
    
    # NaN 및 무한대 값 처리
    macd = macd.replace([np.inf, -np.inf], np.nan).fillna(0)
    signal_line = signal_line.replace([np.inf, -np.inf], np.nan).fillna(0)
    oci = oci.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return {
        'MACD': macd,
        'Signal': signal_line,
        'OCI': oci
    }
