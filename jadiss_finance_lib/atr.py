# ATR(Average True Range, 평균 실제 범위)는 웰스 와일더가 개발한 기술적 지표로, 시장의 변동성을 측정합니다.
# ATR은 가격의 방향성이 아닌 변동성만을 측정하므로, 상승장과 하락장 모두에서 사용할 수 있습니다.
# ATR의 구성 요소:
# True Range(TR): 다음 세 값 중 가장 큰 값
# - 현재 고가 - 현재 저가
# - |현재 고가 - 이전 종가|
# - |현재 저가 - 이전 종가|
# ATR: True Range의 이동평균
# ATR의 특징:
# 변동성 측정: 시장의 변동성을 절대값으로 측정합니다.
# 방향성 무관: 가격의 방향이 아닌 변동 폭만을 고려합니다.
# 스톱로스 설정: 적절한 스톱로스 수준을 결정하는 데 활용됩니다.
# 돌파 확인: 가격 돌파의 유효성을 판단하는 데 사용됩니다.
# ATR 활용:
# 변동성 기반 매매: 변동성이 확대될 때 진입하거나 축소될 때 이탈
# 스톱로스 설정: 현재 ATR의 배수로 스톱로스 설정
# 포지션 사이징: 변동성에 따른 적절한 포지션 크기 결정
# 돌파 필터링: ATR 배수 이상의 돌파만 유효한 신호로 간주

import pandas as pd
import numpy as np

def atr(high, low, close, period=14):
    """
    ATR(평균 실제 범위) 계산
    
    입력 타입:
    high (pd.Series): 고가 데이터 시리즈
    low (pd.Series): 저가 데이터 시리즈
    close (pd.Series): 종가 데이터 시리즈
    period (int): 계산 기간 (기본값: 14)
    
    출력 타입:
    dict: {'ATR': pd.Series, 'TR': pd.Series} - ATR, TR 값을 포함한 딕셔너리
    """
    # True Range 계산
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # ATR 계산 (와일더의 스무딩 방식)
    atr_value = pd.Series(index=tr.index)
    atr_value.iloc[period-1] = tr.iloc[:period].mean()
    
    for i in range(period, len(tr)):
        atr_value.iloc[i] = (atr_value.iloc[i-1] * (period-1) + tr.iloc[i]) / period
    
    # NaN 및 무한대 값 처리
    tr = tr.replace([np.inf, -np.inf], np.nan).fillna(0)
    atr_value = atr_value.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return {
        'ATR': atr_value,
        'TR': tr
    }