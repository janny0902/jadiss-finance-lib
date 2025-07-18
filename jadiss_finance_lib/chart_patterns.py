# 차트 패턴(Chart Patterns)은 가격 차트에서 반복적으로 나타나는 특정 형태의 패턴으로, 향후 가격 움직임을 예측하는 데 사용됩니다.
# 차트 패턴은 추세 반전 패턴과 추세 지속 패턴으로 나눌 수 있으며, 각각의 패턴은 특정한 시장 상황을 나타냅니다.
# 주요 차트 패턴:
# 1. 추세 반전 패턴:
#    - 헤드 앤 숄더(Head and Shoulders): 상승 추세의 끝을 나타내는 패턴, 세 개의 고점 중 가운데가 가장 높음
#    - 역 헤드 앤 숄더(Inverse Head and Shoulders): 하락 추세의 끝을 나타내는 패턴, 세 개의 저점 중 가운데가 가장 낮음
#    - 이중 천장(Double Top): 두 개의 비슷한 고점으로 구성된 상승 추세 반전 패턴
#    - 이중 바닥(Double Bottom): 두 개의 비슷한 저점으로 구성된 하락 추세 반전 패턴
#    - 삼중 천장/바닥(Triple Top/Bottom): 세 개의 비슷한 고점/저점으로 구성된 반전 패턴
# 2. 추세 지속 패턴:
#    - 삼각형(Triangle): 수렴하는 추세선으로 구성된 패턴, 상승/하락/대칭 삼각형으로 구분
#    - 깃발형(Flag): 짧은 통합 기간을 나타내는 평행사변형 패턴
#    - 페넌트(Pennant): 깃발형과 유사하지만 삼각형 모양의 패턴
#    - 쐐기형(Wedge): 수렴하는 두 추세선으로 구성된 패턴, 상승/하락 쐐기로 구분
# 차트 패턴의 활용:
# 추세 예측: 패턴 완성 후 가격의 움직임 방향을 예측합니다.
# 목표가 설정: 패턴의 높이를 기준으로 가격 목표를 설정합니다.
# 진입/퇴출 포인트: 패턴의 돌파를 매매 신호로 활용합니다.
# 리스크 관리: 패턴의 주요 지지/저항선을 스톱로스 포인트로 활용합니다.

import pandas as pd
import numpy as np
from scipy.signal import find_peaks

def chart_patterns(high, low, close, window_size=20):
    """
    차트 패턴 감지
    
    입력 타입:
    high (pd.Series): 고가 데이터 시리즈
    low (pd.Series): 저가 데이터 시리즈
    close (pd.Series): 종가 데이터 시리즈
    window_size (int): 패턴 탐색 윈도우 크기 (기본값: 20)
    
    출력 타입:
    dict: 다양한 차트 패턴의 감지 결과를 포함한 딕셔너리
    """
    # 결과 초기화
    patterns = pd.DataFrame(index=close.index)
    patterns = patterns.fillna(False)
    
    # 피크와 트로프 찾기
    high_peaks, _ = find_peaks(high, distance=5)
    low_troughs, _ = find_peaks(-low, distance=5)
    
    # 1. 이중 천장(Double Top) 패턴
    double_top = pd.Series(False, index=close.index)
    for i in range(1, len(high_peaks)):
        if i >= len(high_peaks):
            break
        peak1_idx = high_peaks[i-1]
        peak2_idx = high_peaks[i]
        
        # 두 고점의 높이가 비슷한지 확인
        if abs(high.iloc[peak1_idx] - high.iloc[peak2_idx]) < 0.03 * high.iloc[peak1_idx]:
            # 두 고점 사이에 저점이 있는지 확인
            trough_between = [t for t in low_troughs if peak1_idx < t < peak2_idx]
            if trough_between:
                # 두 번째 고점 이후 가격이 저점 아래로 떨어지는지 확인
                if peak2_idx + 1 < len(close) and close.iloc[peak2_idx + 1] < low.iloc[trough_between[0]]:
                    double_top.iloc[peak2_idx] = True
    
    # 2. 이중 바닥(Double Bottom) 패턴
    double_bottom = pd.Series(False, index=close.index)
    for i in range(1, len(low_troughs)):
        if i >= len(low_troughs):
            break
        trough1_idx = low_troughs[i-1]
        trough2_idx = low_troughs[i]
        
        # 두 저점의 높이가 비슷한지 확인
        if abs(low.iloc[trough1_idx] - low.iloc[trough2_idx]) < 0.03 * low.iloc[trough1_idx]:
            # 두 저점 사이에 고점이 있는지 확인
            peak_between = [p for p in high_peaks if trough1_idx < p < trough2_idx]
            if peak_between:
                # 두 번째 저점 이후 가격이 고점 위로 올라가는지 확인
                if trough2_idx + 1 < len(close) and close.iloc[trough2_idx + 1] > high.iloc[peak_between[0]]:
                    double_bottom.iloc[trough2_idx] = True
    
    # 3. 헤드 앤 숄더(Head and Shoulders) 패턴
    head_and_shoulders = pd.Series(False, index=close.index)
    for i in range(2, len(high_peaks)):
        if i >= len(high_peaks):
            break
        shoulder1_idx = high_peaks[i-2]
        head_idx = high_peaks[i-1]
        shoulder2_idx = high_peaks[i]
        
        # 헤드가 양쪽 어깨보다 높은지 확인
        if (high.iloc[head_idx] > high.iloc[shoulder1_idx] and 
            high.iloc[head_idx] > high.iloc[shoulder2_idx] and
            abs(high.iloc[shoulder1_idx] - high.iloc[shoulder2_idx]) < 0.05 * high.iloc[shoulder1_idx]):
            
            # 목선(neckline) 확인
            trough1 = min(low.iloc[shoulder1_idx:head_idx])
            trough2 = min(low.iloc[head_idx:shoulder2_idx])
            
            # 두 번째 어깨 이후 가격이 목선 아래로 떨어지는지 확인
            if shoulder2_idx + 1 < len(close) and close.iloc[shoulder2_idx + 1] < min(trough1, trough2):
                head_and_shoulders.iloc[shoulder2_idx] = True
    
    # 4. 역 헤드 앤 숄더(Inverse Head and Shoulders) 패턴
    inv_head_and_shoulders = pd.Series(False, index=close.index)
    for i in range(2, len(low_troughs)):
        if i >= len(low_troughs):
            break
        shoulder1_idx = low_troughs[i-2]
        head_idx = low_troughs[i-1]
        shoulder2_idx = low_troughs[i]
        
        # 헤드가 양쪽 어깨보다 낮은지 확인
        if (low.iloc[head_idx] < low.iloc[shoulder1_idx] and 
            low.iloc[head_idx] < low.iloc[shoulder2_idx] and
            abs(low.iloc[shoulder1_idx] - low.iloc[shoulder2_idx]) < 0.05 * low.iloc[shoulder1_idx]):
            
            # 목선(neckline) 확인
            peak1 = max(high.iloc[shoulder1_idx:head_idx])
            peak2 = max(high.iloc[head_idx:shoulder2_idx])
            
            # 두 번째 어깨 이후 가격이 목선 위로 올라가는지 확인
            if shoulder2_idx + 1 < len(close) and close.iloc[shoulder2_idx + 1] > max(peak1, peak2):
                inv_head_and_shoulders.iloc[shoulder2_idx] = True
    
    # 결과 저장
    patterns['Double_Top'] = double_top
    patterns['Double_Bottom'] = double_bottom
    patterns['Head_And_Shoulders'] = head_and_shoulders
    patterns['Inverse_Head_And_Shoulders'] = inv_head_and_shoulders
    
    # 결과를 딕셔너리로 변환
    result = {col: patterns[col] for col in patterns.columns}
    
    return result