# 표준편차 테스트 파일
# 입력 타입: prices (pd.Series) - 가격 데이터 시리즈
# 출력 타입: dict - {'Z_Score': pd.Series, 'Mean': pd.Series, 'Std': pd.Series, 'Upper_2': pd.Series, 'Upper_1': pd.Series, 'Lower_1': pd.Series, 'Lower_2': pd.Series}

import pandas as pd
import numpy as np
from jadiss_finance_lib.standard_deviation import standard_deviation

def test_standard_deviation():
    # 테스트 데이터: 가격 시리즈 (충분한 데이터 포인트)
    np.random.seed(42)  # 재현 가능한 결과를 위한 시드 설정
    prices = pd.Series([100 + i + np.random.normal(0, 5) for i in range(30)])
    
    result = standard_deviation(prices, period=10)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result, dict)
    assert 'Z_Score' in result
    assert 'Mean' in result
    assert 'Std' in result
    assert 'Upper_2' in result
    assert 'Upper_1' in result
    assert 'Lower_1' in result
    assert 'Lower_2' in result
    
    # 모든 시리즈가 pandas Series인지 확인
    for key in result:
        assert isinstance(result[key], pd.Series)
        assert len(result[key]) == len(prices)
    
    # Z-score가 대략 -3 ~ +3 범위 내에 있는지 확인 (이상치 제외)
    z_scores = result['Z_Score'].dropna()
    assert z_scores.min() >= -4  # 극단적인 경우 고려
    assert z_scores.max() <= 4