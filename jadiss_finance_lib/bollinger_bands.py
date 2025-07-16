# 볼린저 밴드(Bollinger Bands)는 존 볼린저가 개발한 기술적 분석 지표로, 이동평균선을 중심으로 표준편차를 이용해 상한선과 하한선을 그어 가격의 변동성과 과매수/과매도 상태를 판단하는 지표입니다.
# 볼린저 밴드의 구성 요소:
# 중심선(Middle Band):
# 일반적으로 20일 단순이동평균선으로, 가격의 중심 추세를 나타냅니다.
# 상한선(Upper Band):
# 중심선 + (표준편차 × 2)로 계산되며, 저항선 역할을 합니다.
# 하한선(Lower Band):
# 중심선 - (표준편차 × 2)로 계산되며, 지지선 역할을 합니다.
# 볼린저 밴드의 특징:
# 변동성 측정:
# 밴드의 폭이 넓어지면 변동성이 크고, 좁아지면 변동성이 작습니다.
# 상대적 가격 위치:
# 가격이 밴드 내에서 어느 위치에 있는지로 과매수/과매도를 판단합니다.
# 평균 회귀:
# 가격이 밴드를 벗어나면 다시 중심선으로 돌아오려는 성질이 있습니다.
# 동적 지지/저항:
# 상한선과 하한선이 동적으로 지지선과 저항선 역할을 합니다.
# 매매 신호:
# 가격이 상한선에 닿으면 과매수 상태로 매도 고려
# 가격이 하한선에 닿으면 과매도 상태로 매수 고려
# 밴드 수축 후 확장 시 추세 전환 신호
# %B 지표: (현재가 - 하한선) / (상한선 - 하한선) × 100으로 밴드 내 상대적 위치 표시
# 밴드폭: (상한선 - 하한선) / 중심선 × 100으로 변동성 크기 측정

import pandas as pd

def bollinger_bands(prices, period=20, std_dev=2):
    """
    볼린저 밴드 지표 계산
    
    입력 타입:
    prices (pd.Series): 가격 데이터 시리즈
    period (int): 이동평균 계산 기간 (기본값: 20)
    std_dev (float): 표준편차 배수 (기본값: 2)
    
    출력 타입:
    dict: {'Middle': pd.Series, 'Upper': pd.Series, 'Lower': pd.Series, 'Width': pd.Series, 'Percent_B': pd.Series} - 볼린저 밴드 지표들을 포함한 딕셔너리
    """
    # 중심선 (이동평균)
    middle_band = prices.rolling(window=period).mean()
    
    # 표준편차 계산
    std = prices.rolling(window=period).std()
    
    # 상한선과 하한선
    upper_band = middle_band + (std * std_dev)
    lower_band = middle_band - (std * std_dev)
    
    # 밴드폭 (변동성 측정)
    band_width = ((upper_band - lower_band) / middle_band) * 100
    
    # %B (밴드 내 상대적 위치)
    percent_b = ((prices - lower_band) / (upper_band - lower_band)) * 100
    
    return {
        'Middle': middle_band,
        'Upper': upper_band,
        'Lower': lower_band,
        'Width': band_width,
        'Percent_B': percent_b
    }