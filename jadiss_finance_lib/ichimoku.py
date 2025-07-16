# 일목균형표(Ichimoku Kinko Hyo)는 일본에서 개발된 종합적인 기술적 분석 지표로, 한 눈에 균형을 파악할 수 있도록 설계되었습니다. 5개의 선으로 구성되어 추세, 지지/저항, 모멘텀을 동시에 분석할 수 있습니다.
# 일목균형표의 구성 요소:
# 전환선(Tenkan-sen):
# (9일 최고가 + 9일 최저가) / 2로 계산되며, 단기 추세를 나타냅니다.
# 기준선(Kijun-sen):
# (26일 최고가 + 26일 최저가) / 2로 계산되며, 중기 추세를 나타냅니다.
# 선행스팬A(Senkou Span A):
# (전환선 + 기준선) / 2를 26일 앞으로 이동시킨 선입니다.
# 선행스팬B(Senkou Span B):
# (52일 최고가 + 52일 최저가) / 2를 26일 앞으로 이동시킨 선입니다.
# 후행스팬(Chikou Span):
# 현재 종가를 26일 뒤로 이동시킨 선입니다.
# 구름(Kumo):
# 선행스팬A와 선행스팬B 사이의 영역으로, 지지/저항 역할을 합니다.
# 일목균형표의 특징:
# 종합적 분석:
# 추세, 지지/저항, 모멘텀을 한 번에 분석할 수 있습니다.
# 미래 예측:
# 선행스팬을 통해 미래의 지지/저항 수준을 예측할 수 있습니다.
# 시간 개념:
# 과거, 현재, 미래를 모두 고려한 분석이 가능합니다.
# 매매 신호:
# 전환선이 기준선을 상향 돌파하면 골든크로스(매수 신호)
# 전환선이 기준선을 하향 돌파하면 데드크로스(매도 신호)
# 가격이 구름 위에 있으면 상승 추세, 아래에 있으면 하락 추세
# 후행스팬이 과거 가격을 상향 돌파하면 매수 신호

import pandas as pd

def ichimoku(high, low, close, tenkan_period=9, kijun_period=26, senkou_b_period=52, displacement=26):
    """
    일목균형표 지표 계산
    
    입력 타입:
    high (pd.Series): 고가 데이터 시리즈
    low (pd.Series): 저가 데이터 시리즈
    close (pd.Series): 종가 데이터 시리즈
    tenkan_period (int): 전환선 계산 기간 (기본값: 9)
    kijun_period (int): 기준선 계산 기간 (기본값: 26)
    senkou_b_period (int): 선행스팬B 계산 기간 (기본값: 52)
    displacement (int): 선행스팬 이동 기간 (기본값: 26)
    
    출력 타입:
    dict: {'Tenkan': pd.Series, 'Kijun': pd.Series, 'Senkou_A': pd.Series, 'Senkou_B': pd.Series, 'Chikou': pd.Series} - 일목균형표 지표들을 포함한 딕셔너리
    """
    # 전환선 (Tenkan-sen): 단기 추세선
    tenkan = (high.rolling(window=tenkan_period).max() + low.rolling(window=tenkan_period).min()) / 2
    
    # 기준선 (Kijun-sen): 중기 추세선
    kijun = (high.rolling(window=kijun_period).max() + low.rolling(window=kijun_period).min()) / 2
    
    # 선행스팬A (Senkou Span A): 전환선과 기준선의 평균을 미래로 이동
    senkou_a = ((tenkan + kijun) / 2).shift(displacement)
    
    # 선행스팬B (Senkou Span B): 장기 추세선을 미래로 이동
    senkou_b = ((high.rolling(window=senkou_b_period).max() + low.rolling(window=senkou_b_period).min()) / 2).shift(displacement)
    
    # 후행스팬 (Chikou Span): 현재 종가를 과거로 이동
    chikou = close.shift(-displacement)
    
    return {
        'Tenkan': tenkan,
        'Kijun': kijun,
        'Senkou_A': senkou_a,
        'Senkou_B': senkou_b,
        'Chikou': chikou
    }