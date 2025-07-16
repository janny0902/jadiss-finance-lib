# 패러볼릭 테스트 파일
# 입력 타입: high (pd.Series), low (pd.Series), close (pd.Series) - 고가, 저가, 종가 데이터 시리즈
# 출력 타입: dict - {'Parabolic': pd.Series, 'Trend': pd.Series}

import pandas as pd
from jadiss_finance_lib.parabolic import parabolic

def test_parabolic():
    # 테스트 데이터: 고가, 저가, 종가 시리즈
    high = pd.Series([105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120,
                     119, 118, 117, 116, 115, 114, 113, 112, 111, 110, 109, 108, 107, 106])
    low = pd.Series([95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
                    109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 99, 98, 97, 96])
    close = pd.Series([100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115,
                      114, 113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101])
    
    result = parabolic(high, low, close, af_start=0.02, af_increment=0.02, af_max=0.20)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'Parabolic' in result
    assert 'Trend' in result
    assert isinstance(result['Parabolic'], pd.Series)
    assert isinstance(result['Trend'], pd.Series)
    assert len(result['Parabolic']) == len(high)
    assert len(result['Trend']) == len(high)