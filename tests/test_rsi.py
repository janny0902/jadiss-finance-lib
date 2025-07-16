# RSI 테스트 파일
# 입력 타입: prices (pd.Series) - 가격 데이터 시리즈
# 출력 타입: dict - {'RSI': pd.Series}

import pandas as pd
from jadiss_finance_lib.rsi import rsi

def test_rsi():
    # 테스트 데이터: 가격 시리즈
    prices = pd.Series([100, 101, 102, 101, 100, 98, 99, 100, 101, 102])
    result = rsi(prices, period=7)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'RSI' in result
    assert isinstance(result['RSI'], pd.Series)
    assert not result['RSI'].empty
