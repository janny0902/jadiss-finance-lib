# 피보나치 되돌림(Fibonacci Retracement)은 피보나치 수열에서 파생된 비율을 사용하여 가격의 지지선과 저항선을 예측하는 기술적 분석 도구입니다.
# 피보나치 수열에서 도출된 주요 비율(23.6%, 38.2%, 50%, 61.8%, 78.6%)을 사용하여 가격의 조정 수준을 예측합니다.
# 피보나치 되돌림의 계산 방법:
# 1. 주요 고점과 저점을 식별합니다.
# 2. 상승 추세에서는 고점에서 저점으로, 하락 추세에서는 저점에서 고점으로 피보나치 레벨을 그립니다.
# 3. 피보나치 비율에 따라 되돌림 레벨을 계산합니다.
# 피보나치 되돌림의 주요 레벨:
# 0.0%: 추세의 끝점 (고점 또는 저점)
# 23.6%: 약한 되돌림 레벨
# 38.2%: 중요한 되돌림 레벨
# 50.0%: 심리적으로 중요한 중간 지점 (피보나치 수열에서 직접 도출되지는 않음)
# 61.8%: 황금 비율, 가장 중요한 되돌림 레벨
# 78.6%: 깊은 되돌림 레벨
# 100.0%: 추세의 시작점 (저점 또는 고점)
# 피보나치 되돌림의 활용:
# 지지/저항 레벨: 피보나치 레벨은 잠재적인 지지선과 저항선으로 작용합니다.
# 매매 진입점: 추세 방향으로의 거래 진입점을 식별하는 데 사용됩니다.
# 목표가 설정: 피보나치 확장을 통해 목표가를 설정할 수 있습니다.
# 추세 확인: 가격이 특정 피보나치 레벨에서 반응하는지 관찰하여 추세의 강도를 확인합니다.

import pandas as pd
import numpy as np

def fibonacci_retracement(high, low, trend='uptrend'):
    """
    피보나치 되돌림 레벨 계산
    
    입력 타입:
    high (pd.Series): 고가 데이터 시리즈
    low (pd.Series): 저가 데이터 시리즈
    trend (str): 추세 방향 ('uptrend' 또는 'downtrend', 기본값: 'uptrend')
    
    출력 타입:
    dict: 피보나치 되돌림 레벨을 포함한 딕셔너리
    """
    # 주요 고점과 저점 식별
    highest_high = high.max()
    lowest_low = low.min()
    
    # 피보나치 비율
    fib_ratios = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
    
    # 피보나치 레벨 계산
    if trend == 'uptrend':
        # 상승 추세 (저점 → 고점)
        price_range = highest_high - lowest_low
        fib_levels = {
            f'Level_{ratio:.3f}': highest_high - (price_range * ratio)
            for ratio in fib_ratios
        }
    else:
        # 하락 추세 (고점 → 저점)
        price_range = highest_high - lowest_low
        fib_levels = {
            f'Level_{ratio:.3f}': lowest_low + (price_range * ratio)
            for ratio in fib_ratios
        }
    
    # 추가 정보
    fib_levels['Highest'] = highest_high
    fib_levels['Lowest'] = lowest_low
    fib_levels['Trend'] = trend
    
    return fib_levels