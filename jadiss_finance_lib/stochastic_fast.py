# 스토캐스틱 패스트(Stochastic Fast)는 기술적 분석에서 사용되는 모멘텀 지표로, 현재 가격이 특정 기간의 최고가-최저가 범위에서 어느 위치에 있는지를 나타냅니다. 스토캐스틱 슬로우보다 민감하게 반응하여 빠른 신호를 제공합니다.
# 스토캐스틱 패스트의 구성 요소:
# %K:
# 현재 가격이 특정 기간 최고가와 최저가 범위 내에서 어느 위치에 있는지를 백분율로 나타냅니다.
# %D:
# %K의 이동 평균으로, %K보다 부드러운 신호를 제공합니다.
# 스토캐스틱 패스트의 특징:
# 민감성:
# 가격 변화에 빠르게 반응하여 조기 신호를 제공합니다.
# 변동성:
# 스토캐스틱 슬로우에 비해 변동성이 크고 가짜 신호가 많을 수 있습니다.
# 과매수/과매도:
# 0~100% 범위에서 움직이며, 80 이상은 과매수, 20 이하는 과매도로 간주합니다.
# 매매 신호:
# %K 선이 %D 선을 상향 돌파하면 매수 신호, 하향 돌파하면 매도 신호로 해석됩니다.

import pandas as pd

def stochastic_fast(high, low, close, k_period=14, d_period=3):
    """
    스토캐스틱 패스트 지표 계산
    
    입력 타입:
    high (pd.Series): 고가 데이터 시리즈
    low (pd.Series): 저가 데이터 시리즈
    close (pd.Series): 종가 데이터 시리즈
    k_period (int): %K 계산 기간 (기본값: 14)
    d_period (int): %D 계산 기간 (기본값: 3)
    
    출력 타입:
    dict: {'%K': pd.Series, '%D': pd.Series} - 스토캐스틱 패스트 지표들을 포함한 딕셔너리
    """
    # 최고가와 최저가 계산
    highest_high = high.rolling(window=k_period).max()
    lowest_low = low.rolling(window=k_period).min()
    
    # %K 계산 (Raw Stochastic)
    k_percent = ((close - lowest_low) / (highest_high - lowest_low)) * 100
    
    # %D 계산 (%K의 이동평균)
    d_percent = k_percent.rolling(window=d_period).mean()
    
    return {
        '%K': k_percent,
        '%D': d_percent
    }