# ROE 테스트 파일
# 입력 타입: net_income (pd.Series), shareholders_equity (pd.Series) - 순이익, 자기자본 데이터 시리즈
# 출력 타입: dict - {'ROE': pd.Series}

import pandas as pd
from jadiss_finance_lib.roe import roe

def test_roe():
    # 테스트 데이터: 순이익과 자기자본
    net_income = pd.Series([1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900])
    shareholders_equity = pd.Series([5000, 5200, 5400, 5600, 5800, 6000, 6200, 6400, 6600, 6800])
    
    result = roe(net_income, shareholders_equity)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'ROE' in result
    assert isinstance(result['ROE'], pd.Series)
    assert len(result['ROE']) == len(net_income)
    
    # ROE 값이 백분율로 계산되었는지 확인 (첫 번째 값: 1000/5000*100 = 20%)
    assert abs(result['ROE'].iloc[0] - 20.0) < 0.01