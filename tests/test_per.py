# PER 테스트 파일
# 입력 타입: eps (pd.Series), stock_price (pd.Series) - 주당순이익, 주가 데이터 시리즈
# 출력 타입: dict - {'PER': pd.Series}

import pandas as pd
from jadiss_finance_lib.per import per

def test_per():
    # 테스트 데이터: EPS와 주가
    eps_data = pd.Series([10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
    stock_price = pd.Series([100, 110, 120, 130, 140, 150, 160, 170, 180, 190])
    
    result = per(eps_data, stock_price)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'PER' in result
    assert isinstance(result['PER'], pd.Series)
    assert len(result['PER']) == len(eps_data)
    
    # PER 값이 올바르게 계산되었는지 확인 (첫 번째 값: 100/10 = 10.0)
    assert abs(result['PER'].iloc[0] - 10.0) < 0.01