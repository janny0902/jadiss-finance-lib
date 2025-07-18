# 표준편차(Standard Deviation) 기반 표준화 점수는 데이터가 평균으로부터 얼마나 떨어져 있는지를 표준편차 단위로 나타내는 지표입니다. Z-score라고도 불리며, 데이터의 상대적 위치를 파악하는 데 사용됩니다.
# 표준화 점수의 구성 요소:
# 평균(Mean):
# 데이터의 중심값으로, 모든 데이터의 합을 데이터 개수로 나눈 값입니다.
# 표준편차(Standard Deviation):
# 데이터가 평균으로부터 얼마나 퍼져있는지를 나타내는 척도입니다.
# Z-score:
# (개별값 - 평균) ÷ 표준편차로 계산되며, 평균으로부터의 거리를 표준편차 단위로 표현합니다.
# 표준화 점수의 특징:
# 정규화:
# 서로 다른 단위나 규모의 데이터를 동일한 기준으로 비교할 수 있습니다.
# 상대적 위치:
# 데이터가 전체 분포에서 어느 위치에 있는지를 명확히 보여줍니다.
# 이상치 탐지:
# ±2 또는 ±3을 벗어나는 값들을 이상치로 판단할 수 있습니다.
# 확률적 해석:
# 정규분포에서 약 68%는 ±1, 95%는 ±2, 99.7%는 ±3 범위 내에 위치합니다.
# 표준화 점수 해석:
# 0: 평균과 동일한 값
# +1: 평균보다 1 표준편차 위
# -1: 평균보다 1 표준편차 아래
# +2: 평균보다 2 표준편차 위 (상위 약 2.5%)
# -2: 평균보다 2 표준편차 아래 (하위 약 2.5%)
# 활용 분야:
# 주가 분석: 현재 주가가 과거 평균 대비 어느 위치인지 판단
# 리스크 관리: 수익률의 변동성과 극값 분석
# 포트폴리오 관리: 자산 간 상대적 성과 비교
# 이상치 탐지: 비정상적인 가격 움직임 식별

import pandas as pd

def standard_deviation(prices, period=20):
    """
    표준편차 기반 표준화 점수 계산
    
    입력 타입:
    prices (pd.Series): 가격 데이터 시리즈
    period (int): 계산 기간 (기본값: 20)
    
    출력 타입:
    dict: {'Z_Score': pd.Series, 'Mean': pd.Series, 'Std': pd.Series, 'Upper_2': pd.Series, 'Upper_1': pd.Series, 'Lower_1': pd.Series, 'Lower_2': pd.Series} - 표준화 점수와 관련 지표들을 포함한 딕셔너리
    """
    # 이동평균 계산
    rolling_mean = prices.rolling(window=period).mean()
    
    # 이동 표준편차 계산
    rolling_std = prices.rolling(window=period).std()
    
    # Z-score 계산 (표준화 점수)
    z_score = (prices - rolling_mean) / rolling_std
    
    # 표준편차 밴드 계산
    upper_2 = rolling_mean + (rolling_std * 2)  # +2σ
    upper_1 = rolling_mean + (rolling_std * 1)  # +1σ
    lower_1 = rolling_mean - (rolling_std * 1)  # -1σ
    lower_2 = rolling_mean - (rolling_std * 2)  # -2σ
    
    return {
        'Z_Score': z_score,
        'Mean': rolling_mean,
        'Std': rolling_std,
        'Upper_2': upper_2,
        'Upper_1': upper_1,
        'Lower_1': lower_1,
        'Lower_2': lower_2
    }