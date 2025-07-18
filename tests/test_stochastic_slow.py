# 스토캐스틱 슬로우 테스트 파일
# 입력 타입: high (pd.Series), low (pd.Series), close (pd.Series) - 고가, 저가, 종가 데이터 시리즈
# 출력 타입: dict - {'%K': pd.Series, '%D': pd.Series}

import pandas as pd
from jadiss_finance_lib.stochastic_slow import stochastic_slow

def test_stochastic_slow():
    # 테스트 데이터: 고가, 저가, 종가 시리즈
    print("\n===== 스토캐스틱 슬로우 테스트 =====")
    
    # 과매수/과매도 구간을 보여주는 가격 데이터
    high = pd.Series([
        2200, 2220, 2250, 2280, 2300, 2320, 2350, 2380, 2400, 2420,  # 상승 추세 (고가 상승)
        2400, 2380, 2350, 2320, 2300, 2280, 2250, 2220, 2200, 2180,  # 하락 추세 (고가 하락)
        2190, 2200, 2220, 2240, 2260, 2280, 2300, 2320, 2340, 2360   # 재상승 (고가 상승)
    ])
    
    low = pd.Series([
        2000, 2020, 2050, 2080, 2100, 2120, 2150, 2180, 2200, 2220,  # 상승 추세 (저가 상승)
        2200, 2180, 2150, 2120, 2100, 2080, 2050, 2020, 2000, 1980,  # 하락 추세 (저가 하락)
        1990, 2000, 2020, 2040, 2060, 2080, 2100, 2120, 2140, 2160   # 재상승 (저가 상승)
    ])
    
    close = pd.Series([
        2100, 2120, 2150, 2180, 2200, 2220, 2250, 2280, 2300, 2320,  # 상승 추세 (종가 상승)
        2300, 2280, 2250, 2220, 2200, 2180, 2150, 2120, 2100, 2080,  # 하락 추세 (종가 하락)
        2090, 2100, 2120, 2140, 2160, 2180, 2200, 2220, 2240, 2260   # 재상승 (종가 상승)
    ])
    
    print(f"\n입력값 (가격 패턴): 상승 추세 -> 하락 추세 -> 재상승")
    print(f"\n고가: \n{high}")
    print(f"\n저가: \n{low}")
    print(f"\n종가: \n{close}")
    
    
    result = stochastic_slow(high, low, close, k_period=5, d_period=3)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert '%K' in result
    assert '%D' in result
    assert isinstance(result['%K'], pd.Series)
    assert isinstance(result['%D'], pd.Series)
    assert not result['%K'].empty
    assert not result['%D'].empty