# BPR 테스트 파일
# 입력 타입: bps (pd.Series), stock_price (pd.Series) - 주당순자산가치, 주가 데이터 시리즈
# 출력 타입: dict - {'BPR': pd.Series}

import pandas as pd
from jadiss_finance_lib.bpr import bpr

def test_bpr():
    # 테스트 데이터: BPS와 주가
    bps_data = pd.Series([50, 52, 54, 56, 58, 60, 62, 64, 66, 68])
    stock_price = pd.Series([100, 110, 120, 130, 140, 150, 160, 170, 180, 190])
    
    result = bpr(bps_data, stock_price)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'BPR' in result
    assert isinstance(result['BPR'], pd.Series)
    assert len(result['BPR']) == len(bps_data)