# RSI 테스트 파일
# 입력 타입: prices (pd.Series) - 가격 데이터 시리즈
# 출력 타입: dict - {'RSI': pd.Series}

import pandas as pd
from jadiss_finance_lib.rsi import rsi

def test_rsi():
    # 테스트 데이터: 가격 시리즈
    print("\n===== RSI 테스트 =====")
    
    # 과매수/과매도 구간을 보여주는 가격 데이터
    prices = pd.Series([
        2000, 2020, 2040, 2060, 2080, 2100, 2120, 2140, 2160, 2180,  # 지속적 상승 (과매수 구간)
        2160, 2140, 2120, 2100, 2080, 2060, 2040, 2020, 2000, 1980,  # 지속적 하락 (과매도 구간)
        1990, 2000, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080   # 재상승 (중립에서 회복)
    ])
    
    print(f"\n입력값 (가격 패턴): 상승(과매수) -> 하락(과매도) -> 재상승")
    print(f"\n가격: \n{prices}")
    
    result = rsi(prices, period=14)
    
    print(f"\n리턴값: \n{result['RSI']}")
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'RSI' in result
    assert isinstance(result['RSI'], pd.Series)
    assert not result['RSI'].empty
