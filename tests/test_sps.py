# SPS 테스트 파일
# 입력 타입: total_sales (pd.Series), outstanding_shares (pd.Series) - 총매출액, 발행주식수 데이터 시리즈
# 출력 타입: dict - {'SPS': pd.Series}

import pandas as pd
from jadiss_finance_lib.sps import sps

def test_sps():
    # 테스트 데이터: 총매출액과 발행주식수
    total_sales = pd.Series([10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000])
    outstanding_shares = pd.Series([100, 100, 110, 110, 120, 120, 130, 130, 140, 140])
    
    result = sps(total_sales, outstanding_shares)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'SPS' in result
    assert isinstance(result['SPS'], pd.Series)
    assert len(result['SPS']) == len(total_sales)