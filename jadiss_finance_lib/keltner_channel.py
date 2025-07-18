# 켈트너 채널(Keltner Channel)은 체스터 켈트너가 개발한 기술적 지표로, 이동평균을 중심으로 상하 밴드를 형성하여 가격의 변동성과 추세를 분석합니다.
# 켈트너 채널은 볼린저 밴드와 유사하지만, 표준편차 대신 ATR(Average True Range)을 사용하여 밴드의 폭을 결정합니다.
# 켈트너 채널의 구성 요소:
# 중심선(Middle Line): 일반적으로 EMA(지수이동평균)를 사용합니다.
# 상단선(Upper Line): 중심선 + (ATR × 배수)
# 하단선(Lower Line): 중심선 - (ATR × 배수)
# 켈트너 채널의 특징:
# 추세 식별: 채널의 방향은 시장의 추세를 나타냅니다.
# 지지/저항: 상단선과 하단선은 각각 저항선과 지지선 역할을 합니다.
# 변동성 측정: 채널의 폭은 시장의 변동성을 나타냅니다.
# 볼린저 밴드와 비교: 켈트너 채널은 일반적으로 볼린저 밴드보다 더 부드럽게 움직입니다.
# 켈트너 채널 해석:
# 가격이 상단선 위로 이동: 강한 상승 추세, 과매수 가능성
# 가격이 하단선 아래로 이동: 강한 하락 추세, 과매도 가능성
# 가격이 채널 내에서 움직임: 정상적인 시장 상태
# 채널 폭 확대: 변동성 증가, 추세 강화 가능성
# 채널 폭 축소: 변동성 감소, 추세 약화 또는 전환 가능성
# 매매 신호:
# 가격이 하단선에서 반등: 매수 신호
# 가격이 상단선에서 반락: 매도 신호
# 가격이 채널을 돌파: 추세 강화 또는 추세 전환 신호

import pandas as pd
import numpy as np

def keltner_channel(high, low, close, ema_period=20, atr_period=10, multiplier=2):
    """
    켈트너 채널 계산
    
    입력 타입:
    high (pd.Series): 고가 데이터 시리즈
    low (pd.Series): 저가 데이터 시리즈
    close (pd.Series): 종가 데이터 시리즈
    ema_period (int): EMA 계산 기간 (기본값: 20)
    atr_period (int): ATR 계산 기간 (기본값: 10)
    multiplier (float): ATR 승수 (기본값: 2)
    
    출력 타입:
    dict: {'Middle': pd.Series, 'Upper': pd.Series, 'Lower': pd.Series, 'Width': pd.Series} - 켈트너 채널 값을 포함한 딕셔너리
    """
    # 중심선 계산 (EMA)
    middle = close.ewm(span=ema_period, adjust=False).mean()
    
    # ATR 계산
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=atr_period).mean()
    
    # 상단선과 하단선 계산
    upper = middle + (multiplier * atr)
    lower = middle - (multiplier * atr)
    
    # 채널 폭 계산
    width = ((upper - lower) / middle) * 100
    
    # NaN 및 무한대 값 처리
    middle = middle.replace([np.inf, -np.inf], np.nan).fillna(0)
    upper = upper.replace([np.inf, -np.inf], np.nan).fillna(0)
    lower = lower.replace([np.inf, -np.inf], np.nan).fillna(0)
    width = width.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return {
        'Middle': middle,
        'Upper': upper,
        'Lower': lower,
        'Width': width
    }