# VR(Volume Ratio, 거래량 비율)은 상승 거래량과 하락 거래량의 비율을 측정하는 기술적 지표입니다.
# VR은 일정 기간 동안 상승일의 거래량과 하락일의 거래량을 비교하여 시장의 강도를 평가합니다.
# VR의 계산 방법:
# VR = (AV + 1/2 × SV) / (DV + 1/2 × SV) × 100
# 여기서:
# AV(Advancing Volume): 상승일의 거래량 합계
# DV(Declining Volume): 하락일의 거래량 합계
# SV(Stable Volume): 보합일의 거래량 합계
# VR의 특징:
# 거래량 분석: 가격 변화에 따른 거래량의 분포를 분석합니다.
# 모멘텀 측정: 상승 또는 하락 추세의 강도를 측정합니다.
# 과매수/과매도: 극단적인 VR 값은 과매수 또는 과매도 상태를 나타낼 수 있습니다.
# VR 해석:
# VR > 100: 상승 거래량이 하락 거래량보다 많음, 상승 추세 강도
# VR < 100: 하락 거래량이 상승 거래량보다 많음, 하락 추세 강도
# VR 증가: 상승 모멘텀 강화
# VR 감소: 하락 모멘텀 강화
# 매매 신호:
# 낮은 VR에서 상승 전환: 매수 신호
# 높은 VR에서 하락 전환: 매도 신호
# 극단적인 VR 값: 추세 전환 가능성

import pandas as pd
import numpy as np

def vr(close, volume, period=26):
    """
    VR(거래량 비율) 계산
    
    입력 타입:
    close (pd.Series): 종가 데이터 시리즈
    volume (pd.Series): 거래량 데이터 시리즈
    period (int): 계산 기간 (기본값: 26)
    
    출력 타입:
    dict: {'VR': pd.Series} - VR 값을 포함한 딕셔너리
    """
    # 가격 변화 계산
    price_change = close.diff()
    
    # 상승일, 하락일, 보합일 거래량 분류
    av = pd.Series(0, index=close.index)  # 상승일 거래량
    dv = pd.Series(0, index=close.index)  # 하락일 거래량
    sv = pd.Series(0, index=close.index)  # 보합일 거래량
    
    for i in range(1, len(close)):
        if price_change.iloc[i] > 0:
            av.iloc[i] = volume.iloc[i]
        elif price_change.iloc[i] < 0:
            dv.iloc[i] = volume.iloc[i]
        else:
            sv.iloc[i] = volume.iloc[i]
    
    # n기간 동안의 상승일, 하락일, 보합일 거래량 합계
    av_sum = av.rolling(window=period).sum()
    dv_sum = dv.rolling(window=period).sum()
    sv_sum = sv.rolling(window=period).sum()
    
    # VR 계산
    vr_value = (av_sum + 0.5 * sv_sum) / (dv_sum + 0.5 * sv_sum) * 100
    
    # NaN 및 무한대 값 처리
    vr_value = vr_value.replace([np.inf, -np.inf], np.nan).fillna(100)  # 기본값 100으로 설정
    
    return {
        'VR': vr_value
    }