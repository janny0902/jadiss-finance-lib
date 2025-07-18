# 다이버전스 검출 테스트 파일
# 입력 타입: prices (pd.Series), indicator_name (str) - 가격 데이터 시리즈, 지표 이름
# 출력 타입: dict - {'bullish': bool, 'bearish': bool, 'price_points': list, 'indicator_points': list, 'indicator_name': str}

import pandas as pd
import numpy as np
from jadiss_finance_lib.divergence import divergence

def test_divergence():
    print("\n===== 다이버전스 테스트 =====")
    
    # 상승 다이버전스 테스트 데이터 (가격은 하락하는데 RSI는 상승)
    bullish_prices = pd.Series([
        3000, 2950, 2900, 2850, 2800, 2750, 2700, 2650, 2600, 2550, 2500,  # 처음 저점까지 하락
        2520, 2500, 2480, 2460, 2440, 2420, 2400, 2380, 2360, 2340, 2320,  # 두 번째 저점까지 하락 (더 낮은 저점)
        2330, 2350, 2370, 2390, 2410, 2430, 2450, 2470, 2500              # 반드시 상승 (상승 반전 신호)
    ])
    print(f"\n상승 다이버전스 테스트 입력값: \n{bullish_prices}")
    
    # 하락 다이버전스 테스트 데이터 (가격은 상승하는데 RSI는 하락)
    bearish_prices = pd.Series([
        2000, 2020, 2040, 2060, 2080, 2100, 2120, 2140, 2160, 2180, 2200,  # 처음 고점까지 상승
        2190, 2200, 2210, 2220, 2230, 2240, 2250, 2260, 2270, 2280, 2290,  # 두 번째 고점까지 상승 (더 높은 고점)
        2280, 2260, 2240, 2220, 2200, 2180, 2160, 2140, 2120              # 하락 시작 (하락 반전 신호)
    ])
    print(f"\n하락 다이버전스 테스트 입력값: \n{bearish_prices}")
    
    # RSI로 다이버전스 테스트
    bullish_result = divergence(bullish_prices, 'rsi', window=3, peak_threshold=0.01, trough_threshold=0.01, period=5)
    bearish_result = divergence(bearish_prices, 'rsi', window=3, peak_threshold=0.01, trough_threshold=0.01, period=5)
    
    print(f"\n상승 다이버전스 테스트 결과 (RSI): ")
    print(f"상승 반전 신호: {bullish_result['bullish']}")
    print(f"하락 반전 신호: {bullish_result['bearish']}")
    print(f"가격 포인트: {bullish_result['price_points']}")
    print(f"지표 포인트: {bullish_result['indicator_points']}")
    print(f"사용된 지표: {bullish_result['indicator_name']}")
    
    print(f"\n하락 다이버전스 테스트 결과 (RSI): ")
    print(f"상승 반전 신호: {bearish_result['bullish']}")
    print(f"하락 반전 신호: {bearish_result['bearish']}")
    print(f"가격 포인트: {bearish_result['price_points']}")
    print(f"지표 포인트: {bearish_result['indicator_points']}")
    print(f"사용된 지표: {bearish_result['indicator_name']}")
    
    # 다른 지표로도 테스트
    macd_result = divergence(bearish_prices, 'macd', window=3, peak_threshold=0.01, trough_threshold=0.01)
    stoch_result = divergence(bullish_prices, 'stochastic_slow', window=3, peak_threshold=0.01, trough_threshold=0.01)
    
    print(f"\nMACD 다이버전스 테스트 결과: ")
    print(f"상승 반전 신호: {macd_result['bullish']}")
    print(f"하락 반전 신호: {macd_result['bearish']}")
    
    print(f"\n스토캐스틱 다이버전스 테스트 결과: ")
    print(f"상승 반전 신호: {stoch_result['bullish']}")
    print(f"하락 반전 신호: {stoch_result['bearish']}")
    print("\n===========================")
    
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
    
    assert isinstance(macd_result, dict)
    assert isinstance(stoch_result, dict)