# CCI(Commodity Channel Index, 상품채널지수)는 도널드 램버트가 개발한 기술적 지표로, 가격이 평균 가격에서 얼마나 벗어났는지를 측정합니다.
# CCI는 원래 상품 시장을 위해 개발되었지만, 현재는 모든 금융 시장에서 널리 사용됩니다.
# CCI의 계산 방법:
# 1. 일반 가격(Typical Price) = (고가 + 저가 + 종가) / 3
# 2. 일반 가격의 이동평균(MA) 계산
# 3. 평균편차(Mean Deviation) 계산
# 4. CCI = (일반 가격 - MA) / (0.015 * 평균편차)
# CCI의 특징:
# 과매수/과매도: +100 이상은 과매수, -100 이하는 과매도 구간으로 간주됩니다.
# 추세 강도: CCI 값이 클수록 추세가 강하다고 해석됩니다.
# 발산/수렴: 가격과 CCI 간의 다이버전스는 추세 반전 신호로 해석됩니다.
# CCI 해석:
# +100 이상: 강한 상승 추세, 과매수 가능성
# -100 이하: 강한 하락 추세, 과매도 가능성
# +100과 -100 사이: 중립적인 시장 상태
# 0선 돌파: 추세 전환 신호로 해석 가능
# 매매 신호:
# CCI가 -100 아래에서 -100 위로 상승: 매수 신호
# CCI가 +100 위에서 +100 아래로 하락: 매도 신호
# 가격과 CCI 간의 다이버전스: 추세 반전 신호

import pandas as pd
import numpy as np

def cci(high, low, close, period=20):
    """
    CCI(상품채널지수) 계산
    
    입력 타입:
    high (pd.Series): 고가 데이터 시리즈
    low (pd.Series): 저가 데이터 시리즈
    close (pd.Series): 종가 데이터 시리즈
    period (int): 계산 기간 (기본값: 20)
    
    출력 타입:
    dict: {'CCI': pd.Series} - CCI 값을 포함한 딕셔너리
    """
    # 일반 가격(Typical Price) 계산
    tp = (high + low + close) / 3
    
    # 일반 가격의 이동평균 계산
    tp_ma = tp.rolling(window=period).mean()
    
    # 평균편차 계산
    mean_deviation = pd.Series(index=tp.index)
    for i in range(period-1, len(tp)):
        mean_deviation.iloc[i] = abs(tp.iloc[i-period+1:i+1] - tp_ma.iloc[i]).mean()
    
    # CCI 계산
    cci_value = (tp - tp_ma) / (0.015 * mean_deviation)
    
    # NaN 및 무한대 값 처리
    cci_value = cci_value.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return {
        'CCI': cci_value
    }