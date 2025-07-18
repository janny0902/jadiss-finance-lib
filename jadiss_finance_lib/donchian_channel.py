# 돈치안 채널(Donchian Channel)은 리처드 돈치안이 개발한 기술적 지표로, 일정 기간 동안의 최고가와 최저가를 기준으로 상하 밴드를 형성합니다.
# 돈치안 채널은 가격의 변동 범위를 시각적으로 표현하고, 추세 돌파를 식별하는 데 사용됩니다.
# 돈치안 채널의 구성 요소:
# 상단선(Upper Band): n기간 동안의 최고가
# 하단선(Lower Band): n기간 동안의 최저가
# 중심선(Middle Band): 상단선과 하단선의 중간값
# 돈치안 채널의 특징:
# 추세 식별: 채널의 방향은 시장의 추세를 나타냅니다.
# 돌파 신호: 가격이 채널을 돌파하면 추세 전환 신호로 해석됩니다.
# 변동성 측정: 채널의 폭은 시장의 변동성을 나타냅니다.
# 단순성: 계산이 단순하고 이해하기 쉬운 지표입니다.
# 돈치안 채널 해석:
# 가격이 상단선 돌파: 상승 추세 신호
# 가격이 하단선 돌파: 하락 추세 신호
# 가격이 채널 내에서 움직임: 횡보 시장 또는 추세 지속
# 채널 폭 확대: 변동성 증가
# 채널 폭 축소: 변동성 감소, 추세 전환 가능성
# 매매 신호:
# 가격이 상단선 돌파: 매수 신호 (돈치안 브레이크아웃 시스템)
# 가격이 하단선 돌파: 매도 신호 (돈치안 브레이크아웃 시스템)
# 가격이 중심선 돌파: 추세 방향 확인 신호

import pandas as pd
import numpy as np

def donchian_channel(high, low, period=20):
    """
    돈치안 채널 계산
    
    입력 타입:
    high (pd.Series): 고가 데이터 시리즈
    low (pd.Series): 저가 데이터 시리즈
    period (int): 계산 기간 (기본값: 20)
    
    출력 타입:
    dict: {'Upper': pd.Series, 'Middle': pd.Series, 'Lower': pd.Series, 'Width': pd.Series} - 돈치안 채널 값을 포함한 딕셔너리
    """
    # 상단선 계산 (n기간 최고가)
    upper = high.rolling(window=period).max()
    
    # 하단선 계산 (n기간 최저가)
    lower = low.rolling(window=period).min()
    
    # 중심선 계산 (상단선과 하단선의 중간값)
    middle = (upper + lower) / 2
    
    # 채널 폭 계산
    width = ((upper - lower) / middle) * 100
    
    # NaN 및 무한대 값 처리
    upper = upper.replace([np.inf, -np.inf], np.nan).fillna(0)
    middle = middle.replace([np.inf, -np.inf], np.nan).fillna(0)
    lower = lower.replace([np.inf, -np.inf], np.nan).fillna(0)
    width = width.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return {
        'Upper': upper,
        'Middle': middle,
        'Lower': lower,
        'Width': width
    }