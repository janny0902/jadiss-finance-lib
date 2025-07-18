# CMF(Chaikin Money Flow, 차이킨 자금 흐름)는 마크 차이킨이 개발한 기술적 지표로, 거래량과 가격 변화를 결합하여 자금의 유입과 유출을 측정합니다.
# CMF는 일정 기간 동안의 누적 자금 흐름을 거래량으로 나누어 계산하며, 가격 움직임에 대한 거래량의 확인을 제공합니다.
# CMF의 계산 방법:
# 1. 자금 흐름 승수(Money Flow Multiplier, MFM) 계산:
#    MFM = ((종가 - 저가) - (고가 - 종가)) / (고가 - 저가)
# 2. 자금 흐름 볼륨(Money Flow Volume, MFV) 계산:
#    MFV = MFM × 거래량
# 3. n기간 CMF 계산:
#    CMF = n기간 동안의 MFV 합계 / n기간 동안의 거래량 합계
# CMF의 특징:
# 자금 흐름 측정: 시장에 자금이 유입되는지 유출되는지를 나타냅니다.
# 거래량 확인: 가격 움직임에 대한 거래량의 확인을 제공합니다.
# 다이버전스: 가격과 CMF 간의 다이버전스는 추세 반전 신호로 해석됩니다.
# CMF 해석:
# 양수 CMF: 매수 압력, 자금 유입 (종가가 고가와 저가의 중간보다 위에서 마감)
# 음수 CMF: 매도 압력, 자금 유출 (종가가 고가와 저가의 중간보다 아래에서 마감)
# 0선 돌파: 자금 흐름 방향 전환 신호
# 매매 신호:
# CMF가 음수에서 양수로 전환: 매수 신호
# CMF가 양수에서 음수로 전환: 매도 신호
# 가격과 CMF 간의 다이버전스: 추세 반전 신호

import pandas as pd
import numpy as np

def cmf(high, low, close, volume, period=20):
    """
    CMF(차이킨 자금 흐름) 계산
    
    입력 타입:
    high (pd.Series): 고가 데이터 시리즈
    low (pd.Series): 저가 데이터 시리즈
    close (pd.Series): 종가 데이터 시리즈
    volume (pd.Series): 거래량 데이터 시리즈
    period (int): 계산 기간 (기본값: 20)
    
    출력 타입:
    dict: {'CMF': pd.Series} - CMF 값을 포함한 딕셔너리
    """
    # 자금 흐름 승수(Money Flow Multiplier) 계산
    mfm = ((close - low) - (high - close)) / (high - low)
    mfm = mfm.replace([np.inf, -np.inf], 0)  # 0으로 나누기 방지
    
    # 자금 흐름 볼륨(Money Flow Volume) 계산
    mfv = mfm * volume
    
    # n기간 CMF 계산
    cmf_value = mfv.rolling(window=period).sum() / volume.rolling(window=period).sum()
    
    # NaN 및 무한대 값 처리
    cmf_value = cmf_value.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return {
        'CMF': cmf_value
    }