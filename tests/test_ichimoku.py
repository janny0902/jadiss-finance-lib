# 일목균형표 테스트 파일
# 입력 타입: high (pd.Series), low (pd.Series), close (pd.Series) - 고가, 저가, 종가 데이터 시리즈
# 출력 타입: dict - {'Tenkan': pd.Series, 'Kijun': pd.Series, 'Senkou_A': pd.Series, 'Senkou_B': pd.Series, 'Chikou': pd.Series}

import pandas as pd
from jadiss_finance_lib.ichimoku import ichimoku

def test_ichimoku():
    # 테스트 데이터: 고가, 저가, 종가 시리즈 (충분한 데이터 포인트)
    high = pd.Series([105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120] * 4)
    low = pd.Series([95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110] * 4)
    close = pd.Series([100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115] * 4)
    
    result = ichimoku(high, low, close, tenkan_period=9, kijun_period=26, senkou_b_period=52, displacement=26)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'Tenkan' in result
    assert 'Kijun' in result
    assert 'Senkou_A' in result
    assert 'Senkou_B' in result
    assert 'Chikou' in result
    assert isinstance(result['Tenkan'], pd.Series)
    assert isinstance(result['Kijun'], pd.Series)
    assert isinstance(result['Senkou_A'], pd.Series)
    assert isinstance(result['Senkou_B'], pd.Series)
    assert isinstance(result['Chikou'], pd.Series)