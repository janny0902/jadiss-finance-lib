# 패러볼릭 테스트 파일
# 입력 타입: high (pd.Series), low (pd.Series), close (pd.Series) - 고가, 저가, 종가 데이터 시리즈
# 출력 타입: dict - {'Parabolic': pd.Series, 'Trend': pd.Series}

import pandas as pd
from jadiss_finance_lib.parabolic import parabolic

def test_parabolic():
    # 테스트 데이터: 상승 후 하락 후 상승하는 가격 패턴
    print("\n===== 패러볼릭 테스트 =====")
    
    # 상승 추세 -> 하락 추세 -> 상승 추세로 전환되는 가격 데이터
    high = pd.Series([2500, 2520, 2560, 2580, 2620, 2650, 2680, 2720, 2750, 2780,  # 상승 구간
                     2760, 2720, 2680, 2640, 2600, 2580, 2550, 2520, 2480, 2450,  # 하락 구간
                     2470, 2500, 2530, 2560, 2600, 2640, 2680, 2720, 2760, 2800])  # 상승 구간
    
    low = pd.Series([2450, 2480, 2500, 2530, 2560, 2600, 2630, 2660, 2700, 2720,   # 상승 구간
                    2700, 2660, 2620, 2580, 2550, 2520, 2480, 2450, 2420, 2400,   # 하락 구간
                    2420, 2450, 2480, 2500, 2540, 2580, 2620, 2660, 2700, 2740])   # 상승 구간
    
    close = pd.Series([2480, 2500, 2540, 2560, 2600, 2630, 2660, 2700, 2730, 2750,  # 상승 구간
                      2720, 2680, 2640, 2600, 2570, 2540, 2500, 2470, 2440, 2420,  # 하락 구간
                      2450, 2480, 2510, 2540, 2580, 2620, 2660, 2700, 2740, 2780])  # 상승 구간
    
    print(f"\n입력값 (가격 패턴): 상승 -> 하락 -> 상승")
    print(f"\n고가: \n{high}")
    print(f"\n저가: \n{low}")
    print(f"\n종가: \n{close}")
    
    result = parabolic(high, low, close, af_start=0.02, af_increment=0.02, af_max=0.20)
    
    print(f"\n결과:")
    print(f"\n패러볼릭 값: \n{result['Parabolic'].head(10)}...")
    print(f"\n추세 방향 (1=상승, -1=하락): \n{result['Trend'].head(10)}...")
    print("\n===========================")
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'Parabolic' in result
    assert 'Trend' in result
    assert isinstance(result['Parabolic'], pd.Series)
    assert isinstance(result['Trend'], pd.Series)
    assert len(result['Parabolic']) == len(high)
    assert len(result['Trend']) == len(high)