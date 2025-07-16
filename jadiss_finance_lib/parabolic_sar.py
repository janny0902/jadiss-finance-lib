# 패러볼릭 SAR(Stop And Reverse)은 웰스 와일더가 개발한 추세 추종 지표로, 추세의 방향과 잠재적 반전점을 식별하는 데 사용됩니다. SAR은 "Stop And Reverse"의 약자로, 포지션을 청산하고 반대 방향으로 진입하는 시점을 나타냅니다.
# 패러볼릭 SAR의 구성 요소:
# SAR 값:
# 현재 추세에서 스톱 로스 레벨을 나타내는 점들입니다.
# 가속도 인수(AF):
# 추세가 지속될 때마다 증가하는 값으로, SAR의 민감도를 조절합니다.
# 극값(EP):
# 현재 추세에서의 최고가(상승 추세) 또는 최저가(하락 추세)입니다.
# 패러볼릭 SAR의 특징:
# 추세 추종:
# 강한 추세에서 효과적이며, 추세가 지속되는 동안 수익을 보호합니다.
# 후행 지표:
# 가격 변화를 따라가는 후행 지표의 특성을 가집니다.
# 명확한 신호:
# 가격과 SAR의 위치 관계로 명확한 매매 신호를 제공합니다.
# 동적 스톱 로스:
# 추세가 지속되면서 스톱 로스 레벨이 동적으로 조정됩니다.
# 계산 방법:
# 상승 추세: SAR = 이전 SAR + AF × (EP - 이전 SAR)
# 하락 추세: SAR = 이전 SAR + AF × (EP - 이전 SAR)
# AF는 새로운 극값이 나타날 때마다 증가 (최대값 제한)
# 매매 신호:
# 가격이 SAR 위에 있으면 상승 추세 (매수 포지션 유지)
# 가격이 SAR 아래에 있으면 하락 추세 (매도 포지션 유지)
# 가격이 SAR를 돌파하면 추세 전환 및 포지션 반전 신호

import pandas as pd
import numpy as np

def parabolic_sar(high, low, af_start=0.02, af_increment=0.02, af_max=0.20):
    """
    패러볼릭 SAR 지표 계산
    
    입력 타입:
    high (pd.Series): 고가 데이터 시리즈
    low (pd.Series): 저가 데이터 시리즈
    af_start (float): 초기 가속도 인수 (기본값: 0.02)
    af_increment (float): 가속도 증가량 (기본값: 0.02)
    af_max (float): 최대 가속도 인수 (기본값: 0.20)
    
    출력 타입:
    dict: {'SAR': pd.Series, 'Trend': pd.Series, 'AF': pd.Series, 'EP': pd.Series} - SAR 값, 추세, 가속도 인수, 극값을 포함한 딕셔너리
    """
    length = len(high)
    sar = np.zeros(length)
    trend = np.zeros(length)
    af = np.zeros(length)
    ep = np.zeros(length)
    
    # 초기값 설정
    sar[0] = low.iloc[0]
    trend[0] = 1  # 1: 상승, -1: 하락
    af[0] = af_start
    ep[0] = high.iloc[0]
    
    for i in range(1, length):
        # 이전 값들
        prev_sar = sar[i-1]
        prev_trend = trend[i-1]
        prev_af = af[i-1]
        prev_ep = ep[i-1]
        
        # SAR 계산
        sar[i] = prev_sar + prev_af * (prev_ep - prev_sar)
        
        if prev_trend == 1:  # 상승 추세
            # SAR 조정 (상승 추세에서는 이전 2일의 최저가보다 높을 수 없음)
            if i >= 2:
                sar[i] = min(sar[i], low.iloc[i-1], low.iloc[i-2])
            else:
                sar[i] = min(sar[i], low.iloc[i-1])
            
            # 추세 전환 확인
            if low.iloc[i] <= sar[i]:
                # 하락 추세로 전환
                trend[i] = -1
                sar[i] = prev_ep
                af[i] = af_start
                ep[i] = low.iloc[i]
            else:
                # 상승 추세 지속
                trend[i] = 1
                if high.iloc[i] > prev_ep:
                    ep[i] = high.iloc[i]
                    af[i] = min(prev_af + af_increment, af_max)
                else:
                    ep[i] = prev_ep
                    af[i] = prev_af
        else:  # 하락 추세
            # SAR 조정 (하락 추세에서는 이전 2일의 최고가보다 낮을 수 없음)
            if i >= 2:
                sar[i] = max(sar[i], high.iloc[i-1], high.iloc[i-2])
            else:
                sar[i] = max(sar[i], high.iloc[i-1])
            
            # 추세 전환 확인
            if high.iloc[i] >= sar[i]:
                # 상승 추세로 전환
                trend[i] = 1
                sar[i] = prev_ep
                af[i] = af_start
                ep[i] = high.iloc[i]
            else:
                # 하락 추세 지속
                trend[i] = -1
                if low.iloc[i] < prev_ep:
                    ep[i] = low.iloc[i]
                    af[i] = min(prev_af + af_increment, af_max)
                else:
                    ep[i] = prev_ep
                    af[i] = prev_af
    
    return {
        'SAR': pd.Series(sar, index=high.index),
        'Trend': pd.Series(trend, index=high.index),
        'AF': pd.Series(af, index=high.index),
        'EP': pd.Series(ep, index=high.index)
    }