# 캔들 패턴(Candle Patterns)은 일본 캔들스틱 차트에서 나타나는 특정 형태의 패턴으로, 시장의 심리와 향후 가격 움직임을 예측하는 데 사용됩니다.
# 캔들 패턴은 단일 캔들 패턴과 복합 캔들 패턴으로 나눌 수 있으며, 각각의 패턴은 특정한 시장 상황을 나타냅니다.
# 주요 캔들 패턴:
# 1. 단일 캔들 패턴:
#    - 해머(Hammer): 하락 추세에서 나타나는 반전 신호, 긴 아래 그림자와 작은 몸통
#    - 교수형(Hanging Man): 상승 추세에서 나타나는 반전 신호, 해머와 유사하지만 상승 추세에서 발생
#    - 유성형(Shooting Star): 상승 추세에서 나타나는 반전 신호, 긴 위 그림자와 작은 몸통
#    - 도지(Doji): 시가와 종가가 거의 같은 캔들, 시장의 불확실성을 나타냄
# 2. 복합 캔들 패턴:
#    - 장악형(Engulfing): 이전 캔들의 몸통을 완전히 감싸는 캔들, 추세 반전 신호
#    - 잉태형(Harami): 이전 캔들의 몸통 안에 완전히 포함되는 작은 캔들, 추세 약화 신호
#    - 십자형(Cross): 두 개의 도지가 연속으로 나타나는 패턴
#    - 별형(Star): 세 개의 캔들로 구성된 패턴, 중간 캔들이 이전 추세에서 떨어져 있음
# 캔들 패턴의 활용:
# 추세 반전: 많은 캔들 패턴은 추세 반전의 신호로 해석됩니다.
# 추세 지속: 일부 패턴은 현재 추세의 지속을 나타냅니다.
# 시장 심리: 캔들의 형태는 시장 참여자들의 심리 상태를 반영합니다.
# 매매 신호: 캔들 패턴은 매수 또는 매도 신호로 활용될 수 있습니다.

import pandas as pd
import numpy as np

def candle_patterns(open, high, low, close):
    """
    캔들 패턴 감지
    
    입력 타입:
    open (pd.Series): 시가 데이터 시리즈
    high (pd.Series): 고가 데이터 시리즈
    low (pd.Series): 저가 데이터 시리즈
    close (pd.Series): 종가 데이터 시리즈
    
    출력 타입:
    dict: 다양한 캔들 패턴의 감지 결과를 포함한 딕셔너리
    """
    # 캔들 특성 계산
    body_size = abs(close - open)
    body_avg = body_size.rolling(window=14).mean()
    upper_shadow = high - np.maximum(close, open)
    lower_shadow = np.minimum(close, open) - low
    
    # 결과 초기화
    patterns = pd.DataFrame(index=close.index)
    
    # 1. 도지(Doji) 패턴
    doji = body_size < (body_avg * 0.1)
    patterns['Doji'] = doji
    
    # 2. 해머(Hammer) 패턴
    hammer = (body_size > 0) & (lower_shadow > (body_size * 2)) & (upper_shadow < (body_size * 0.5))
    patterns['Hammer'] = hammer
    
    # 3. 교수형(Hanging Man) 패턴
    hanging_man = (body_size > 0) & (lower_shadow > (body_size * 2)) & (upper_shadow < (body_size * 0.5))
    patterns['Hanging_Man'] = hanging_man
    
    # 4. 유성형(Shooting Star) 패턴
    shooting_star = (body_size > 0) & (upper_shadow > (body_size * 2)) & (lower_shadow < (body_size * 0.5))
    patterns['Shooting_Star'] = shooting_star
    
    # 5. 장악형(Engulfing) 패턴
    bullish_engulfing = (open.shift(1) > close.shift(1)) & (open < close) & (open <= close.shift(1)) & (close >= open.shift(1))
    bearish_engulfing = (open.shift(1) < close.shift(1)) & (open > close) & (open >= close.shift(1)) & (close <= open.shift(1))
    patterns['Bullish_Engulfing'] = bullish_engulfing
    patterns['Bearish_Engulfing'] = bearish_engulfing
    
    # 6. 잉태형(Harami) 패턴
    bullish_harami = (open.shift(1) > close.shift(1)) & (open > close) & (open > close.shift(1)) & (close < open.shift(1))
    bearish_harami = (open.shift(1) < close.shift(1)) & (open < close) & (open < close.shift(1)) & (close > open.shift(1))
    patterns['Bullish_Harami'] = bullish_harami
    patterns['Bearish_Harami'] = bearish_harami
    
    # 7. 별형(Star) 패턴
    morning_star = (close.shift(2) < open.shift(2)) & (abs(close.shift(1) - open.shift(1)) < body_avg * 0.5) & (close > open) & (close > ((open.shift(2) + close.shift(2)) / 2))
    evening_star = (close.shift(2) > open.shift(2)) & (abs(close.shift(1) - open.shift(1)) < body_avg * 0.5) & (close < open) & (close < ((open.shift(2) + close.shift(2)) / 2))
    patterns['Morning_Star'] = morning_star
    patterns['Evening_Star'] = evening_star
    
    # NaN 값 처리
    patterns = patterns.fillna(False)
    
    # 결과를 딕셔너리로 변환
    result = {col: patterns[col] for col in patterns.columns}
    
    return result