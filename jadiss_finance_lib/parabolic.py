# 패러볼릭(Parabolic)은 웰스 와일더가 개발한 기술적 분석 지표로, 추세의 방향과 전환점을 파악하는 데 사용됩니다. 가격이 추세를 따라 움직일 때 가속도를 적용하여 계산하는 지표입니다.
# 패러볼릭의 특징:
# 추세 추종:
# 상승 추세에서는 지지선 역할, 하락 추세에서는 저항선 역할을 합니다.
# 가속도 개념:
# 추세가 지속될수록 가속도 인수(AF)가 증가하여 더 빠르게 가격을 추적합니다.
# 단순한 신호:
# 가격이 패러볼릭 선을 돌파하면 추세 전환 신호로 해석됩니다.
# 패러볼릭 계산:
# 초기값: 첫 번째 극값(최고가 또는 최저가)
# SAR = 이전 SAR + AF × (EP - 이전 SAR)
# AF: 가속도 인수 (초기값 0.02, 최대값 0.20)
# EP: 극값 (상승 추세시 최고가, 하락 추세시 최저가)
# 매매 신호:
# 가격이 패러볼릭 선을 상향 돌파하면 매수 신호
# 가격이 패러볼릭 선을 하향 돌파하면 매도 신호
# 추세가 강할수록 패러볼릭 선이 가격에 더 가까워집니다.

import pandas as pd
import numpy as np

def parabolic(high, low, close, af_start=0.02, af_increment=0.02, af_max=0.20):
    """
    패러볼릭 지표 계산
    
    입력 타입:
    high (pd.Series): 고가 데이터 시리즈
    low (pd.Series): 저가 데이터 시리즈
    close (pd.Series): 종가 데이터 시리즈
    af_start (float): 초기 가속도 인수 (기본값: 0.02)
    af_increment (float): 가속도 증가량 (기본값: 0.02)
    af_max (float): 최대 가속도 인수 (기본값: 0.20)
    
    출력 타입:
    dict: {'Parabolic': pd.Series, 'Trend': pd.Series} - 패러볼릭 값과 추세 방향을 포함한 딕셔너리
    """
    length = len(high)
    parabolic_values = np.zeros(length)
    trend = np.zeros(length)
    
    # 초기값 설정
    af = af_start
    ep = high.iloc[0]
    parabolic_values[0] = low.iloc[0]
    trend[0] = 1  # 1: 상승, -1: 하락
    
    for i in range(1, length):
        # 이전 패러볼릭 값 계산
        parabolic_values[i] = parabolic_values[i-1] + af * (ep - parabolic_values[i-1])
        
        # 추세 판단
        if trend[i-1] == 1:  # 상승 추세
            if low.iloc[i] <= parabolic_values[i]:
                # 추세 전환
                trend[i] = -1
                parabolic_values[i] = ep
                af = af_start
                ep = low.iloc[i]
            else:
                trend[i] = 1
                if high.iloc[i] > ep:
                    ep = high.iloc[i]
                    af = min(af + af_increment, af_max)
        else:  # 하락 추세
            if high.iloc[i] >= parabolic_values[i]:
                # 추세 전환
                trend[i] = 1
                parabolic_values[i] = ep
                af = af_start
                ep = high.iloc[i]
            else:
                trend[i] = -1
                if low.iloc[i] < ep:
                    ep = low.iloc[i]
                    af = min(af + af_increment, af_max)
    
    return {
        'Parabolic': pd.Series(parabolic_values, index=high.index),
        'Trend': pd.Series(trend, index=high.index)
    }