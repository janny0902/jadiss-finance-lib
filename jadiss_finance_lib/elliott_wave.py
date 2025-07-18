# 엘리어트 파동(Elliott Wave)은 금융 시장에서 가격 움직임의 패턴을 분석하는 기술적 분석 방법입니다.
# 엘리어트 파동 이론에 따르면, 시장은 5개의 추진파(1,2,3,4,5)와 3개의 조정파(a,b,c)로 구성된 사이클을 반복합니다.
# 엘리어트 파동의 구성:
# 추진파(Impulse Wave):
# 1파: 초기 상승/하락 움직임
# 2파: 1파의 조정(일반적으로 1파 움직임의 38.2~61.8% 되돌림)
# 3파: 가장 강력하고 긴 움직임(종종 1파의 1.618배)
# 4파: 3파의 조정(일반적으로 3파 움직임의 38.2~50% 되돌림)
# 5파: 최종 상승/하락 움직임(종종 1파와 비슷한 크기)
# 조정파(Corrective Wave):
# A파: 추진파 이후 첫 번째 조정 움직임
# B파: A파에 대한 반발 움직임
# C파: 최종 조정 움직임
# 엘리어트 파동 식별 방법:
# 피보나치 되돌림: 파동 간 되돌림 수준이 피보나치 비율(38.2%, 50%, 61.8%)과 일치하는지 확인
# 파동 비율: 3파는 1파보다 길고, 5파는 1파와 비슷한 길이인지 확인
# 볼륨 패턴: 3파에서 볼륨이 증가하고 5파에서 감소하는지 확인
# 시간 비율: 파동 간 시간 관계도 피보나치 비율을 따르는 경향이 있음

import pandas as pd
import numpy as np
from scipy.signal import find_peaks

def elliott_wave_detector(prices, window_size=20, peak_threshold=0.02, trough_threshold=0.02, 
                      wave2_min_retracement=0.382, wave2_max_retracement=0.618,
                      wave4_min_retracement=0.382, wave4_max_retracement=0.5,
                      waveb_min_retracement=0.5, waveb_max_retracement=0.75,
                      wavec_min_ratio=0.9, wavec_max_ratio=1.1):
    """
    엘리어트 파동 패턴 검색기
    
    입력 타입:
    prices (pd.Series): 가격 데이터 시리즈
    window_size (int): 피크와 트로프 탐지를 위한 윈도우 크기 (기본값: 20)
    peak_threshold (float): 피크 탐지 임계값 (기본값: 0.02 = 2%)
    trough_threshold (float): 트로프 탐지 임계값 (기본값: 0.02 = 2%)
    wave2_min_retracement (float): 2파 최소 되돌림 수준 (기본값: 0.382 = 38.2%)
    wave2_max_retracement (float): 2파 최대 되돌림 수준 (기본값: 0.618 = 61.8%)
    wave4_min_retracement (float): 4파 최소 되돌림 수준 (기본값: 0.382 = 38.2%)
    wave4_max_retracement (float): 4파 최대 되돌림 수준 (기본값: 0.5 = 50%)
    waveb_min_retracement (float): B파 최소 되돌림 수준 (기본값: 0.5 = 50%)
    waveb_max_retracement (float): B파 최대 되돌림 수준 (기본값: 0.75 = 75%)
    wavec_min_ratio (float): C파/A파 최소 비율 (기본값: 0.9 = 90%)
    wavec_max_ratio (float): C파/A파 최대 비율 (기본값: 1.1 = 110%)
    
    출력 타입:
    dict: {
        'wave_1_2': bool - 1,2파 진행 중 여부,
        'wave_3_4': bool - 3,4파 진행 중 여부,
        'wave_b_c': bool - b,c파 진행 중 여부,
        'wave_points': list - 식별된 파동 지점들의 가격 리스트
    }
    """
    # 결과 초기화
    result = {
        'wave_1_2': False,
        'wave_3_4': False,
        'wave_b_c': False,
        'wave_points': []
    }
    
    if len(prices) < window_size * 2:
        return result  # 데이터가 충분하지 않음
    
    # 피크와 트로프 찾기
    # 상대적 변화율 계산
    price_changes = prices.pct_change().abs()
    
    # 피크 찾기 (고점)
    peaks, _ = find_peaks(prices, prominence=prices.mean() * peak_threshold)
    
    # 트로프 찾기 (저점)
    troughs, _ = find_peaks(-prices, prominence=prices.mean() * trough_threshold)
    
    # 모든 변곡점을 시간순으로 정렬
    all_points = np.sort(np.concatenate([peaks, troughs]))
    
    if len(all_points) < 5:
        return result  # 변곡점이 충분하지 않음
    
    # 변곡점 유형 식별 (피크=1, 트로프=-1)
    point_types = np.zeros(len(all_points))
    for i, point in enumerate(all_points):
        if point in peaks:
            point_types[i] = 1
        else:
            point_types[i] = -1
    
    # 엘리어트 파동 패턴 식별
    wave_points = []
    
    # 최근 5개 변곡점 분석
    recent_points = all_points[-5:] if len(all_points) >= 5 else all_points
    recent_types = point_types[-5:] if len(point_types) >= 5 else point_types
    
    # 파동 포인트 수집
    for point in recent_points:
        wave_points.append(prices.iloc[point])
    
    # 1,2파 패턴 확인 (상승 후 부분 조정)
    if len(recent_points) >= 2:
        if recent_types[-2] == 1 and recent_types[-1] == -1:
            # 2파 되돌림 수준 확인 (38.2~61.8%)
            p0 = prices.iloc[0]  # 시작점
            p1 = prices.iloc[recent_points[-2]]  # 1파 끝
            p2 = prices.iloc[recent_points[-1]]  # 2파 끝
            
            retracement = (p1 - p2) / (p1 - p0) if p1 != p0 else 0
            if wave2_min_retracement <= retracement <= wave2_max_retracement:
                result['wave_1_2'] = True
    
    # 3,4파 패턴 확인 (강한 상승 후 부분 조정)
    if len(recent_points) >= 4:
        if (recent_types[-4] == -1 and recent_types[-3] == 1 and 
            recent_types[-2] == -1 and recent_types[-1] == 1):
            # 3파 길이와 4파 되돌림 확인
            p1 = prices.iloc[recent_points[-4]]  # 1파 끝 (2파 시작)
            p2 = prices.iloc[recent_points[-3]]  # 2파 끝 (3파 시작)
            p3 = prices.iloc[recent_points[-2]]  # 3파 끝 (4파 시작)
            p4 = prices.iloc[recent_points[-1]]  # 4파 끝
            
            wave1_length = abs(p2 - p1)
            wave3_length = abs(p3 - p2)
            retracement = (p3 - p4) / (p3 - p2) if p3 != p2 else 0
            
            # 3파는 1파보다 길고, 4파는 3파의 지정된 되돌림 수준
            if wave3_length > wave1_length and wave4_min_retracement <= retracement <= wave4_max_retracement:
                result['wave_3_4'] = True
    
    # b,c파 패턴 확인 (A파 하락 후 B파 반등, C파 하락)
    if len(recent_points) >= 3:
        if (recent_types[-3] == -1 and recent_types[-2] == 1 and recent_types[-1] == -1):
            # A, B, C파 길이 확인
            pa = prices.iloc[recent_points[-3]]  # A파 끝
            pb = prices.iloc[recent_points[-2]]  # B파 끝
            pc = prices.iloc[recent_points[-1]]  # C파 끝 (현재)
            
            # B파는 A파의 지정된 되돌림 수준, C파는 A파와 지정된 비율
            b_retracement = (pb - pa) / (prices.iloc[0] - pa) if prices.iloc[0] != pa else 0
            c_to_a_ratio = (pc - pb) / (pa - prices.iloc[0]) if pa != prices.iloc[0] else 0
            
            if waveb_min_retracement <= b_retracement <= waveb_max_retracement and wavec_min_ratio <= c_to_a_ratio <= wavec_max_ratio:
                result['wave_b_c'] = True
    
    # 파동 포인트 저장
    result['wave_points'] = wave_points
    
    return result