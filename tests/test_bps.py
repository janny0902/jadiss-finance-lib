# BPS 테스트 파일
# 입력 타입: shareholders_equity (pd.Series), outstanding_shares (pd.Series) - 순자산, 발행주식수 데이터 시리즈
# 출력 타입: dict - {'BPS': pd.Series}

import pandas as pd
from jadiss_finance_lib.bps import bps

def test_bps():
    # 테스트 데이터: 순자산과 발행주식수
    shareholders_equity = pd.Series([5000, 5200, 5400, 5600, 5800, 6000, 6200, 6400, 6600, 6800])
    outstanding_shares = pd.Series([100, 100, 110, 110, 120, 120, 130, 130, 140, 140])
    
    result = bps(shareholders_equity, outstanding_shares)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'BPS' in result
    assert isinstance(result['BPS'], pd.Series)
    assert len(result['BPS']) == len(shareholders_equity)