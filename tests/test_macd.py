# MACD 테스트 파일
# 입력 타입: prices (pd.Series) - 가격 데이터 시리즈
# 출력 타입: dict - {'MACD': pd.Series, 'Signal': pd.Series, 'Histogram': pd.Series}

import pandas as pd
from jadiss_finance_lib.macd import macd

def test_macd():
    # 테스트 데이터: 가격 시리즈
    prices = pd.Series([100, 101, 102, 101, 100, 98, 99, 100, 101, 102])
    result = macd(prices, fast=5, slow=10, signal=3)
    
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
