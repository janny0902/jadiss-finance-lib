# 엘리어트 파동 검색기 테스트 파일
# 입력 타입: prices (pd.Series) - 가격 데이터 시리즈
# 출력 타입: dict - {'wave_1_2': bool, 'wave_3_4': bool, 'wave_b_c': bool, 'wave_points': list}

import pandas as pd
import numpy as np
from jadiss_finance_lib.elliott_wave import elliott_wave_detector

def test_elliott_wave_detector():
    # 테스트 데이터: 엘리어트 파동 패턴을 시뮬레이션한 가격 시리즈
    
    # 1-2파 패턴 테스트 (상승 후 부분 조정)
    wave_1_2_prices = pd.Series([100, 102, 105, 110, 115, 120, 125, 130, 125, 120, 118])
    result_1_2 = elliott_wave_detector(wave_1_2_prices, window_size=3, peak_threshold=0.01, trough_threshold=0.01,
                                    wave2_min_retracement=0.3, wave2_max_retracement=0.7)
    
    # 3-4파 패턴 테스트 (강한 상승 후 부분 조정)
    wave_3_4_prices = pd.Series([100, 110, 105, 115, 125, 140, 160, 150, 145, 155])
    result_3_4 = elliott_wave_detector(wave_3_4_prices, window_size=3, peak_threshold=0.01, trough_threshold=0.01,
                                    wave4_min_retracement=0.3, wave4_max_retracement=0.6)
    
    # b-c파 패턴 테스트 (A파 하락 후 B파 반등, C파 하락)
    wave_b_c_prices = pd.Series([100, 95, 90, 85, 80, 85, 90, 85, 80, 75])
    result_b_c = elliott_wave_detector(wave_b_c_prices, window_size=3, peak_threshold=0.01, trough_threshold=0.01,
                                    waveb_min_retracement=0.4, waveb_max_retracement=0.8,
                                    wavec_min_ratio=0.8, wavec_max_ratio=1.2)
    
    # 반환값이 딕셔너리인지 확인
    assert isinstance(result_1_2, dict)
    assert isinstance(result_3_4, dict)
    assert isinstance(result_b_c, dict)
    
    # 필요한 키가 모두 있는지 확인
    for result in [result_1_2, result_3_4, result_b_c]:
        assert 'wave_1_2' in result
        assert 'wave_3_4' in result
        assert 'wave_b_c' in result
        assert 'wave_points' in result
        
        assert isinstance(result['wave_1_2'], bool)
        assert isinstance(result['wave_3_4'], bool)
        assert isinstance(result['wave_b_c'], bool)
        assert isinstance(result['wave_points'], list)