# 다이버전스(Divergence)는 가격과 기술적 지표 간의 불일치를 나타내는 현상으로, 시장의 반전 신호를 감지하는 데 사용됩니다.
# 다이버전스의 종류:
# 1. 정배열 다이버전스(Regular Divergence):
#    - 상승 다이버전스: 가격은 하락하는데 지표는 상승하는 경우 (상승 반전 신호)
#    - 하락 다이버전스: 가격은 상승하는데 지표는 하락하는 경우 (하락 반전 신호)
# 2. 역배열 다이버전스(Hidden Divergence):
#    - 상승 다이버전스: 가격은 상승하는데 지표는 더 약한 상승을 보이는 경우 (추세 지속 신호)
#    - 하락 다이버전스: 가격은 하락하는데 지표는 더 약한 하락을 보이는 경우 (추세 지속 신호)
# 다이버전스 식별 방법:
# - 가격과 지표의 고점/저점을 비교
# - 가격과 지표의 추세선 기울기를 비교
# - 가격과 지표의 변곡점 간 관계 분석
# 다이버전스 활용:
# - 추세 반전 신호로 활용
# - 과매수/과매도 구간에서 더 효과적
# - 다른 기술적 지표와 함께 사용하여 신뢰도 향상

import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import importlib

def divergence(prices, indicator_name, window=20, peak_threshold=0.02, trough_threshold=0.02, lookback=5, **indicator_params):
    """
    가격과 기술적 지표 간의 다이버전스 검출
    
    입력 타입:
    prices (pd.Series): 가격 데이터 시리즈
    indicator_name (str): 사용할 기술적 지표 이름 (예: 'rsi', 'macd', 'stochastic_slow')
    window (int): 피크와 트로프 탐지를 위한 윈도우 크기 (기본값: 20)
    peak_threshold (float): 피크 탐지 임계값 (기본값: 0.02 = 2%)
    trough_threshold (float): 트로프 탐지 임계값 (기본값: 0.02 = 2%)
    lookback (int): 검사할 최근 변곡점 수 (기본값: 5)
    **indicator_params: 지표 계산에 필요한 추가 매개변수
    
    출력 타입:
    dict: {
        'bullish': bool - 상승 반전 신호 여부,
        'bearish': bool - 하락 반전 신호 여부,
        'price_points': list - 다이버전스 가격 포인트,
        'indicator_points': list - 다이버전스 지표 포인트,
        'indicator_name': str - 사용된 지표 이름
    }
    """
    # 결과 초기화
    result = {
        'bullish': False,
        'bearish': False,
        'price_points': [],
        'indicator_points': [],
        'indicator_name': indicator_name
    }
    
    if len(prices) < window * 2:
        return result  # 데이터가 충분하지 않음
    
    # 지표 계산
    try:
        # 동적으로 지표 모듈 가져오기
        indicator_module = importlib.import_module(f"jadiss_finance_lib.{indicator_name}")
        indicator_func = getattr(indicator_module, indicator_name)
        
        # 지표 계산
        if indicator_name == 'rsi':
            indicator_result = indicator_func(prices, **indicator_params)
            indicator_values = indicator_result['RSI']
        elif indicator_name == 'macd':
            indicator_result = indicator_func(prices, **indicator_params)
            indicator_values = indicator_result['MACD']
        elif indicator_name == 'macd_oci':
            indicator_result = indicator_func(prices, **indicator_params)
            indicator_values = indicator_result['OCI']
        elif indicator_name == 'stochastic_slow' or indicator_name == 'stochastic_fast':
            high = prices  # 간단한 예시로 동일한 값 사용
            low = prices
            indicator_result = indicator_func(high, low, prices, **indicator_params)
            indicator_values = indicator_result['%K']
        elif indicator_name == 'bollinger_bands':
            indicator_result = indicator_func(prices, **indicator_params)
            indicator_values = indicator_result['Percent_B']
        elif indicator_name == 'standard_deviation':
            indicator_result = indicator_func(prices, **indicator_params)
            indicator_values = indicator_result['Z_Score']
        else:
            # 기본적으로 첫 번째 반환 값 사용
            indicator_result = indicator_func(prices, **indicator_params)
            indicator_values = list(indicator_result.values())[0]
    except (ImportError, AttributeError) as e:
        print(f"지표 로드 오류: {e}")
        return result
    
    # 가격 피크와 트로프 찾기
    price_peaks, _ = find_peaks(prices, prominence=prices.mean() * peak_threshold)
    price_troughs, _ = find_peaks(-prices, prominence=prices.mean() * trough_threshold)
    
    # 지표 피크와 트로프 찾기
    indicator_peaks, _ = find_peaks(indicator_values, prominence=indicator_values.mean() * peak_threshold)
    indicator_troughs, _ = find_peaks(-indicator_values, prominence=indicator_values.mean() * trough_threshold)
    
    # 최근 변곡점만 고려
    if len(price_peaks) > lookback:
        price_peaks = price_peaks[-lookback:]
    if len(price_troughs) > lookback:
        price_troughs = price_troughs[-lookback:]
    if len(indicator_peaks) > lookback:
        indicator_peaks = indicator_peaks[-lookback:]
    if len(indicator_troughs) > lookback:
        indicator_troughs = indicator_troughs[-lookback:]
    
    # 상승 다이버전스 검출 (가격 저점은 하락, 지표 저점은 상승)
    if len(price_troughs) >= 2 and len(indicator_troughs) >= 2:
        # 최근 두 개의 저점 비교
        price_trough1, price_trough2 = price_troughs[-2], price_troughs[-1]
        indicator_trough1, indicator_trough2 = indicator_troughs[-2], indicator_troughs[-1]
        
        # 가격은 하락하는데 지표는 상승하는 경우
        if (prices.iloc[price_trough2] < prices.iloc[price_trough1] and 
            indicator_values.iloc[indicator_trough2] > indicator_values.iloc[indicator_trough1]):
            result['bullish'] = True
            result['price_points'] = [prices.iloc[price_trough1], prices.iloc[price_trough2]]
            result['indicator_points'] = [indicator_values.iloc[indicator_trough1], indicator_values.iloc[indicator_trough2]]
    
    # 하락 다이버전스 검출 (가격 고점은 상승, 지표 고점은 하락)
    if len(price_peaks) >= 2 and len(indicator_peaks) >= 2:
        # 최근 두 개의 고점 비교
        price_peak1, price_peak2 = price_peaks[-2], price_peaks[-1]
        indicator_peak1, indicator_peak2 = indicator_peaks[-2], indicator_peaks[-1]
        
        # 가격은 상승하는데 지표는 하락하는 경우
        if (prices.iloc[price_peak2] > prices.iloc[price_peak1] and 
            indicator_values.iloc[indicator_peak2] < indicator_values.iloc[indicator_peak1]):
            result['bearish'] = True
            result['price_points'] = [prices.iloc[price_peak1], prices.iloc[price_peak2]]
            result['indicator_points'] = [indicator_values.iloc[indicator_peak1], indicator_values.iloc[indicator_peak2]]
    
    return result