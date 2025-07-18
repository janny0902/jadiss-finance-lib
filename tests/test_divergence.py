# 다이버전스 검출 테스트 파일
# 입력 타입: prices (pd.Series), indicator_name (str) - 가격 데이터 시리즈, 지표 이름
# 출력 타입: dict - {'bullish': bool, 'bearish': bool, 'price_points': list, 'indicator_points': list, 'indicator_name': str}

import pandas as pd
import numpy as np
from jadiss_finance_lib.divergence import divergence

def test_divergence():
    # 상승 다이버전스 테스트 데이터 (가격은 하락하는데 RSI는 상승)
    bullish_prices = pd.Series([100, 95, 90, 85, 80, 82, 78, 75, 73, 70, 68, 65, 67, 70])
    
    # 하락 다이버전스 테스트 데이터 (가격은 상승하는데 RSI는 하락)
    bearish_prices = pd.Series([100, 105, 110, 115, 120, 118, 122, 125, 127, 130, 132, 135, 133, 130])
    
    # RSI로 다이버전스 테스트
    bullish_result = divergence(bullish_prices, 'rsi', window=3, peak_threshold=0.01, trough_threshold=0.01, period=5)
    bearish_result = divergence(bearish_prices, 'rsi', window=3, peak_threshold=0.01, trough_threshold=0.01, period=5)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(bullish_result, dict)
    assert isinstance(bearish_result, dict)
    
    # 필요한 키가 모두 있는지 확인
    for result in [bullish_result, bearish_result]:
        assert 'bullish' in result
        assert 'bearish' in result
        assert 'price_points' in result
        assert 'indicator_points' in result
        assert 'indicator_name' in result
        
        assert isinstance(result['bullish'], bool)
        assert isinstance(result['bearish'], bool)
        assert isinstance(result['price_points'], list)
        assert isinstance(result['indicator_points'], list)
        assert isinstance(result['indicator_name'], str)
        
    # 다른 지표로도 테스트
    macd_result = divergence(bearish_prices, 'macd', window=3, peak_threshold=0.01, trough_threshold=0.01)
    stoch_result = divergence(bullish_prices, 'stochastic_slow', window=3, peak_threshold=0.01, trough_threshold=0.01)
    
    assert isinstance(macd_result, dict)
    assert isinstance(stoch_result, dict)