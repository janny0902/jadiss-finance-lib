# 스토캐스틱 슬로우 테스트 파일
# 입력 타입: high (pd.Series), low (pd.Series), close (pd.Series) - 고가, 저가, 종가 데이터 시리즈
# 출력 타입: dict - {'%K': pd.Series, '%D': pd.Series}

import pandas as pd
from jadiss_finance_lib.stochastic_slow import stochastic_slow

def test_stochastic_slow():
    # 테스트 데이터: 고가, 저가, 종가 시리즈
    high = pd.Series([105, 106, 107, 106, 105, 103, 104, 105, 106, 107])
    low = pd.Series([95, 96, 97, 96, 95, 93, 94, 95, 96, 97])
    close = pd.Series([100, 101, 102, 101, 100, 98, 99, 100, 101, 102])
    
    result = stochastic_slow(high, low, close, k_period=5, d_period=3)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert '%K' in result
    assert '%D' in result
    assert isinstance(result['%K'], pd.Series)
    assert isinstance(result['%D'], pd.Series)
    assert not result['%K'].empty
    assert not result['%D'].empty