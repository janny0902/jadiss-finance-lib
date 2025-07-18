# PSR 테스트 파일
# 입력 타입: sps (pd.Series), stock_price (pd.Series) - 주당매출액, 주가 데이터 시리즈
# 출력 타입: dict - {'PSR': pd.Series}

import pandas as pd
from jadiss_finance_lib.psr import psr

def test_psr():
    # 테스트 데이터: SPS와 주가
    sps_data = pd.Series([100, 110, 120, 130, 140, 150, 160, 170, 180, 190])
    stock_price = pd.Series([100, 110, 120, 130, 140, 150, 160, 170, 180, 190])
    
    result = psr(sps_data, stock_price)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'PSR' in result
    assert isinstance(result['PSR'], pd.Series)
    assert len(result['PSR']) == len(sps_data)
    
    # PSR 값이 올바르게 계산되었는지 확인 (첫 번째 값: 100/100 = 1.0)
    assert abs(result['PSR'].iloc[0] - 1.0) < 0.01