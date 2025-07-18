# OBV(On-Balance Volume, 온밸런스 볼륨)는 조셉 그랜빌이 개발한 기술적 지표로, 거래량과 가격 변화의 관계를 분석합니다.
# OBV는 가격 변화의 방향에 따라 거래량을 누적하여 계산하며, 가격 움직임에 앞서 거래량의 변화를 감지하는 데 사용됩니다.
# OBV의 계산 방법:
# - 종가가 전일 종가보다 상승: OBV = 이전 OBV + 현재 거래량
# - 종가가 전일 종가보다 하락: OBV = 이전 OBV - 현재 거래량
# - 종가가 전일 종가와 동일: OBV = 이전 OBV
# OBV의 특징:
# 선행 지표: 종종 가격 변화에 앞서 움직이는 선행 지표로 작용합니다.
# 추세 확인: 가격 추세의 강도를 확인하는 데 사용됩니다.
# 다이버전스: 가격과 OBV 간의 다이버전스는 추세 반전 신호로 해석됩니다.
# OBV 해석:
# OBV 상승: 매수 압력 증가, 상승 추세 지속 가능성
# OBV 하락: 매도 압력 증가, 하락 추세 지속 가능성
# 가격 상승 + OBV 하락: 약세 다이버전스, 상승 추세 약화 신호
# 가격 하락 + OBV 상승: 강세 다이버전스, 하락 추세 약화 신호

import pandas as pd
import numpy as np

def obv(close, volume):
    """
    OBV(온밸런스 볼륨) 계산
    
    입력 타입:
    close (pd.Series): 종가 데이터 시리즈
    volume (pd.Series): 거래량 데이터 시리즈
    
    출력 타입:
    dict: {'OBV': pd.Series} - OBV 값을 포함한 딕셔너리
    """
    obv_value = pd.Series(0, index=close.index)
    
    for i in range(1, len(close)):
        if close.iloc[i] > close.iloc[i-1]:
            obv_value.iloc[i] = obv_value.iloc[i-1] + volume.iloc[i]
        elif close.iloc[i] < close.iloc[i-1]:
            obv_value.iloc[i] = obv_value.iloc[i-1] - volume.iloc[i]
        else:
            obv_value.iloc[i] = obv_value.iloc[i-1]
    
    return {
        'OBV': obv_value
    }