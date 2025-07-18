# 볼린저 밴드 테스트 파일
# 입력 타입: prices (pd.Series) - 가격 데이터 시리즈
# 출력 타입: dict - {'Middle': pd.Series, 'Upper': pd.Series, 'Lower': pd.Series, 'Width': pd.Series, 'Percent_B': pd.Series}

import pandas as pd
from jadiss_finance_lib.bollinger_bands import bollinger_bands

def test_bollinger_bands():
    # 테스트 데이터: 가격 시리즈
    print("\n===== 볼린저 밴드 테스트 =====")
    
    # 변동성 수축 후 확장을 보여주는 가격 데이터
    prices = pd.Series([
        2000, 2010, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090,  # 완만한 상승 (일정한 변동성)
        2090, 2100, 2090, 2100, 2090, 2100, 2090, 2100, 2090, 2100,  # 박스권 형성 (낮은 변동성)
        2080, 2120, 2070, 2140, 2050, 2160, 2030, 2180, 2000, 2200,  # 변동성 확대 (상하폭 확대)
        2220, 2180, 2250, 2150, 2280, 2120, 2300, 2100, 2320, 2080   # 가파른 상승과 하락 (고변동성)
    ])
    
    print(f"\n입력값 (가격 패턴): 일정 상승 -> 박스권 -> 변동성 확대 -> 고변동성")
    print(f"\n가격: \n{prices}")
    
    
    result = bollinger_bands(prices, period=10, std_dev=2)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'Middle' in result
    assert 'Upper' in result
    assert 'Lower' in result
    assert 'Width' in result
    assert 'Percent_B' in result
    assert isinstance(result['Middle'], pd.Series)
    assert isinstance(result['Upper'], pd.Series)
    assert isinstance(result['Lower'], pd.Series)
    assert isinstance(result['Width'], pd.Series)
    assert isinstance(result['Percent_B'], pd.Series)