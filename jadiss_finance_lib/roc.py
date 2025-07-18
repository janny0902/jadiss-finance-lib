# ROC(Rate of Change, 변화율)는 가격의 변화 속도를 측정하는 모멘텀 지표입니다.
# ROC는 현재 가격과 n기간 이전 가격의 차이를 백분율로 표시하여 가격 변화의 속도를 나타냅니다.
# ROC의 계산 방법:
# ROC = ((현재 가격 - n기간 이전 가격) / n기간 이전 가격) × 100
# ROC의 특징:
# 모멘텀 측정: 가격 변화의 속도와 강도를 측정합니다.
# 진동 지표: 0을 중심으로 양수와 음수 영역을 오가며 진동합니다.
# 다이버전스: 가격과 ROC 간의 다이버전스는 추세 반전 신호로 해석됩니다.
# ROC 해석:
# 양수 ROC: 상승 모멘텀, 값이 클수록 상승 속도가 빠름
# 음수 ROC: 하락 모멘텀, 값이 작을수록 하락 속도가 빠름
# 0선 돌파: 모멘텀 방향 전환 신호
# 극단값: 매우 높거나 낮은 ROC 값은 과매수/과매도 상태를 나타낼 수 있음
# 매매 신호:
# ROC가 음수에서 양수로 전환: 매수 신호
# ROC가 양수에서 음수로 전환: 매도 신호
# 가격과 ROC 간의 다이버전스: 추세 반전 신호

import pandas as pd
import numpy as np

def roc(prices, period=12):
    """
    ROC(변화율) 계산
    
    입력 타입:
    prices (pd.Series): 가격 데이터 시리즈
    period (int): 계산 기간 (기본값: 12)
    
    출력 타입:
    dict: {'ROC': pd.Series} - ROC 값을 포함한 딕셔너리
    """
    # n기간 이전 가격
    prev_prices = prices.shift(period)
    
    # ROC 계산
    roc_value = ((prices - prev_prices) / prev_prices) * 100
    
    # NaN 및 무한대 값 처리
    roc_value = roc_value.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return {
        'ROC': roc_value
    }