# SPR 테스트 파일
# 입력 타입: sps (pd.Series), stock_price (pd.Series) - 주당매출액, 주가 데이터 시리즈
# 출력 타입: dict - {'SPR': pd.Series}

import pandas as pd
from jadiss_finance_lib.psr import spr

def test_spr():
    # 테스트 데이터: SPS와 주가
    sps_data = pd.Series([100, 110, 120, 130, 140, 150, 160, 170, 180, 190])
    stock_price = pd.Series([100, 110, 120, 130, 140, 150, 160, 170, 180, 190])
    
    result = spr(sps_data, stock_price)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'SPR' in result
    assert isinstance(result['SPR'], pd.Series)
    assert len(result['SPR']) == len(sps_data)