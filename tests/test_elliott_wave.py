# 엘리어트 파동 검색기 테스트 파일
# 입력 타입: prices (pd.Series) - 가격 데이터 시리즈
# 출력 타입: dict - {'wave_1_2': bool, 'wave_3_4': bool, 'wave_b_c': bool, 'wave_points': list}

import pandas as pd
import numpy as np
from jadiss_finance_lib.elliott_wave import elliott_wave_detector

def test_elliott_wave_detector():
    # 테스트 데이터: 엘리어트 파동 패턴을 시뮬레이션한 가격 시리즈
    print("\n===== 엘리어트 파동 테스트 =====")
    
    # 1-2파 패턴 테스트 (상승 후 부분 조정)
    wave_1_2_prices = pd.Series([
        2000, 2020, 2040, 2060, 2080, 2100, 2120, 2140, 2160, 2180, 2200,  # 1파: 초기 상승
        2160, 2120, 2100, 2080, 2070                                      # 2파: 1파의 약 61.8% 되돌림
    ])
    print(f"\n1-2파 테스트 입력값: \n{wave_1_2_prices}")
    
    result_1_2 = elliott_wave_detector(wave_1_2_prices, window_size=3, peak_threshold=0.01, trough_threshold=0.01,
                                    wave2_min_retracement=0.3, wave2_max_retracement=0.7)
    
    print(f"\n1-2파 테스트 결과: ")
    print(f"1,2파 진행 중: {result_1_2['wave_1_2']}")
    print(f"3,4파 진행 중: {result_1_2['wave_3_4']}")
    print(f"b,c파 진행 중: {result_1_2['wave_b_c']}")
    print(f"파동 포인트: {result_1_2['wave_points']}")
    
    # 3-4파 패턴 테스트 (강한 상승 후 부분 조정)
    wave_3_4_prices = pd.Series([
        2000, 2050, 2100, 2080, 2050,                                      # 1-2파 완료
        2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000,        # 3파: 강한 상승 (가장 긴 파동)
        2900, 2800, 2750, 2700, 2650                                      # 4파: 3파의 정확히 38.2% 되돌림
    ])
    print(f"\n3-4파 테스트 입력값: \n{wave_3_4_prices}")
    
    result_3_4 = elliott_wave_detector(wave_3_4_prices, window_size=3, peak_threshold=0.01, trough_threshold=0.01,
                                    wave4_min_retracement=0.3, wave4_max_retracement=0.6)
    
    print(f"\n3-4파 테스트 결과: ")
    print(f"1,2파 진행 중: {result_3_4['wave_1_2']}")
    print(f"3,4파 진행 중: {result_3_4['wave_3_4']}")
    print(f"b,c파 진행 중: {result_3_4['wave_b_c']}")
    print(f"파동 포인트: {result_3_4['wave_points']}")
    
    # b-c파 패턴 테스트 (A파 하락 후 B파 반등, C파 하락)
    wave_b_c_prices = pd.Series([
        3000, 2900, 2800, 2700, 2600, 2500, 2400, 2300, 2200, 2100, 2000,  # A파: 하락
        2100, 2200, 2300, 2400, 2500,                                      # B파: A파의 정확히 50% 반등
        2400, 2300, 2200, 2100, 2000, 1900, 1800, 1700, 1600, 1500         # C파: A파와 정확히 동일한 하락
    ])
    print(f"\nb-c파 테스트 입력값: \n{wave_b_c_prices}")
    
    result_b_c = elliott_wave_detector(wave_b_c_prices, window_size=3, peak_threshold=0.01, trough_threshold=0.01,
                                    waveb_min_retracement=0.4, waveb_max_retracement=0.8,
                                    wavec_min_ratio=0.8, wavec_max_ratio=1.2)
    
    print(f"\nb-c파 테스트 결과: ")
    print(f"1,2파 진행 중: {result_b_c['wave_1_2']}")
    print(f"3,4파 진행 중: {result_b_c['wave_3_4']}")
    print(f"b,c파 진행 중: {result_b_c['wave_b_c']}")
    print(f"파동 포인트: {result_b_c['wave_points']}")
    print("\n===========================")
    
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