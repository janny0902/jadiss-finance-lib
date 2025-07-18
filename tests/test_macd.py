# MACD 테스트 파일
# 입력 타입: prices (pd.Series) - 가격 데이터 시리즈
# 출력 타입: dict - {'MACD': pd.Series, 'Signal': pd.Series, 'Histogram': pd.Series}

import pandas as pd
from jadiss_finance_lib.macd import macd

def test_macd():
    # 테스트 데이터: 가격 시리즈
    print("\n===== MACD 테스트 =====")
    
    # 추세 전환을 보여주는 가격 데이터
    prices = pd.Series([
        2000, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090,  # 완만한 상승
        2100, 2120, 2140, 2160, 2180, 2200, 2220, 2240, 2260, 2280,  # 가파르게 상승
        2260, 2240, 2220, 2200, 2180, 2160, 2140, 2120, 2100, 2080,  # 하락 시작
        2060, 2040, 2020, 2000, 1980, 1960, 1940, 1920, 1900, 1880   # 지속적 하락
    ])
    
    print(f"\n입력값 (가격 패턴): 완만한 상승 -> 가파른 상승 -> 하락 시작 -> 지속적 하락")
    print(f"\n가격: \n{prices}")
    
    result = macd(prices, fast=12, slow=26, signal=9)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'MACD' in result
    assert 'Signal' in result
    assert 'Histogram' in result
    assert isinstance(result['MACD'], pd.Series)
    assert isinstance(result['Signal'], pd.Series)
    assert isinstance(result['Histogram'], pd.Series)
    assert not result['MACD'].empty
    assert not result['Signal'].empty
    assert not result['Histogram'].empty
