# 볼린저 밴드 테스트 파일
# 입력 타입: prices (pd.Series) - 가격 데이터 시리즈
# 출력 타입: dict - {'Middle': pd.Series, 'Upper': pd.Series, 'Lower': pd.Series, 'Width': pd.Series, 'Percent_B': pd.Series}

import pandas as pd
from jadiss_finance_lib.bollinger_bands import bollinger_bands

def test_bollinger_bands():
    # 테스트 데이터: 가격 시리즈 (충분한 데이터 포인트)
    prices = pd.Series([100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 
                       116, 117, 118, 119, 120, 119, 118, 117, 116, 115, 114, 113, 112, 111])
    
    result = bollinger_bands(prices, period=10, std_dev=2)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'Middle' in result
    assert 'Upper' in result
    assert 'Lower' in result
    assert 'Width' in result
    assert 'Percent_B' in result
    assert isinstance(result['Middle'], pd.Series)
    assert isinstance(result['Upper'], pd.Series)
    assert isinstance(result['Lower'], pd.Series)
    assert isinstance(result['Width'], pd.Series)
    assert isinstance(result['Percent_B'], pd.Series)