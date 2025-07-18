# ADX(Average Directional Index, 평균 방향성 지수)는 웰스 와일더가 개발한 기술적 지표로, 추세의 강도를 측정합니다.
# ADX는 추세의 방향이 아닌 강도만을 측정하므로, 상승 추세와 하락 추세 모두에서 높은 값을 가질 수 있습니다.
# ADX의 구성 요소:
# +DI(Plus Directional Indicator): 상승 추세의 강도를 나타냅니다.
# -DI(Minus Directional Indicator): 하락 추세의 강도를 나타냅니다.
# ADX: +DI와 -DI의 차이를 평균화하여 추세의 전체적인 강도를 나타냅니다.
# ADX의 해석:
# 0-25: 약한 추세 또는 추세 없음
# 25-50: 강한 추세
# 50-75: 매우 강한 추세
# 75-100: 극도로 강한 추세
# 매매 신호:
# +DI가 -DI를 상향 돌파: 매수 신호
# -DI가 +DI를 상향 돌파: 매도 신호
# ADX가 상승 중: 현재 추세의 강도가 증가 중
# ADX가 하락 중: 현재 추세의 강도가 약화 중

import pandas as pd
import numpy as np

def adx(high, low, close, period=14):
    """
    ADX(평균 방향성 지수) 계산
    
    입력 타입:
    high (pd.Series): 고가 데이터 시리즈
    low (pd.Series): 저가 데이터 시리즈
    close (pd.Series): 종가 데이터 시리즈
    period (int): 계산 기간 (기본값: 14)
    
    출력 타입:
    dict: {'ADX': pd.Series, '+DI': pd.Series, '-DI': pd.Series} - ADX, +DI, -DI 값을 포함한 딕셔너리
    """
    # 가격 변화 계산
    high_diff = high.diff()
    low_diff = low.diff()
    
    # True Range 계산
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    # +DM, -DM 계산
    plus_dm = pd.Series(0.0, index=high.index)
    minus_dm = pd.Series(0.0, index=high.index)
    
    for i in range(1, len(high)):
        if high_diff.iloc[i] > 0 and high_diff.iloc[i] > abs(low_diff.iloc[i]):
            plus_dm.iloc[i] = high_diff.iloc[i]
        else:
            plus_dm.iloc[i] = 0.0
            
        if low_diff.iloc[i] < 0 and abs(low_diff.iloc[i]) > high_diff.iloc[i]:
            minus_dm.iloc[i] = abs(low_diff.iloc[i])
        else:
            minus_dm.iloc[i] = 0.0
    
    # +DI, -DI 계산
    plus_di = 100 * (plus_dm.rolling(window=period).sum() / atr.rolling(window=period).sum())
    minus_di = 100 * (minus_dm.rolling(window=period).sum() / atr.rolling(window=period).sum())
    
    # DX 계산
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    
    # ADX 계산 (DX의 이동평균)
    adx_value = dx.rolling(window=period).mean()
    
    # NaN 및 무한대 값 처리
    plus_di = plus_di.replace([np.inf, -np.inf], np.nan).fillna(0)
    minus_di = minus_di.replace([np.inf, -np.inf], np.nan).fillna(0)
    adx_value = adx_value.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return {
        'ADX': adx_value,
        '+DI': plus_di,
        '-DI': minus_di
    }