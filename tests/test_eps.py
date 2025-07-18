# EPS 테스트 파일
# 입력 타입: net_income (pd.Series), outstanding_shares (pd.Series) - 순이익, 발행주식수 데이터 시리즈
# 출력 타입: dict - {'EPS': pd.Series}

import pandas as pd
from jadiss_finance_lib.eps import eps

def test_eps():
    # 테스트 데이터: 순이익과 발행주식수
    net_income = pd.Series([1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900])
    outstanding_shares = pd.Series([100, 100, 110, 110, 120, 120, 130, 130, 140, 140])
    
    result = eps(net_income, outstanding_shares)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'EPS' in result
    assert isinstance(result['EPS'], pd.Series)
    assert len(result['EPS']) == len(net_income)