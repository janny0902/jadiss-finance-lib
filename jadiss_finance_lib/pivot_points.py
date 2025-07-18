# 피봇 포인트(Pivot Points)는 이전 거래 기간의 고가, 저가, 종가를 기반으로 계산되는 기술적 지표로, 다음 거래 기간의 지지선과 저항선을 예측하는 데 사용됩니다.
# 피봇 포인트는 단기 트레이더들이 매매 결정을 내리는 데 널리 사용되며, 특히 일중 거래자들에게 인기가 있습니다.
# 피봇 포인트의 종류:
# 1. 표준 피봇 포인트(Standard Pivot Points)
# 2. 피보나치 피봇 포인트(Fibonacci Pivot Points)
# 3. 우디 피봇 포인트(Woodie's Pivot Points)
# 4. 캐머릴라 피봇 포인트(Camarilla Pivot Points)
# 5. 드마크 피봇 포인트(DeMark's Pivot Points)
# 표준 피봇 포인트 계산 방법:
# 피봇 포인트(PP) = (고가 + 저가 + 종가) / 3
# 첫 번째 저항선(R1) = (2 × PP) - 저가
# 두 번째 저항선(R2) = PP + (고가 - 저가)
# 세 번째 저항선(R3) = 고가 + 2 × (PP - 저가)
# 첫 번째 지지선(S1) = (2 × PP) - 고가
# 두 번째 지지선(S2) = PP - (고가 - 저가)
# 세 번째 지지선(S3) = 저가 - 2 × (고가 - PP)
# 피봇 포인트의 활용:
# 지지/저항 레벨: 피봇 포인트와 지지/저항선은 잠재적인 반전점으로 작용합니다.
# 추세 방향: 가격이 피봇 포인트 위에 있으면 상승 편향, 아래에 있으면 하락 편향으로 해석됩니다.
# 돌파 확인: 지지/저항선 돌파는 추세의 강도를 확인하는 신호로 사용됩니다.
# 목표가 설정: 다음 지지/저항선을 목표가로 설정할 수 있습니다.

import pandas as pd
import numpy as np

def pivot_points(high, low, close, method='standard'):
    """
    피봇 포인트 계산
    
    입력 타입:
    high (float): 이전 기간 고가
    low (float): 이전 기간 저가
    close (float): 이전 기간 종가
    method (str): 계산 방법 ('standard', 'fibonacci', 'woodie', 'camarilla', 'demark', 기본값: 'standard')
    
    출력 타입:
    dict: 피봇 포인트와 지지/저항선을 포함한 딕셔너리
    """
    result = {}
    
    if method == 'standard':
        # 표준 피봇 포인트
        pp = (high + low + close) / 3
        r1 = (2 * pp) - low
        r2 = pp + (high - low)
        r3 = high + 2 * (pp - low)
        s1 = (2 * pp) - high
        s2 = pp - (high - low)
        s3 = low - 2 * (high - pp)
        
        result = {
            'PP': pp,
            'R1': r1,
            'R2': r2,
            'R3': r3,
            'S1': s1,
            'S2': s2,
            'S3': s3
        }
    
    elif method == 'fibonacci':
        # 피보나치 피봇 포인트
        pp = (high + low + close) / 3
        r1 = pp + 0.382 * (high - low)
        r2 = pp + 0.618 * (high - low)
        r3 = pp + 1.000 * (high - low)
        s1 = pp - 0.382 * (high - low)
        s2 = pp - 0.618 * (high - low)
        s3 = pp - 1.000 * (high - low)
        
        result = {
            'PP': pp,
            'R1': r1,
            'R2': r2,
            'R3': r3,
            'S1': s1,
            'S2': s2,
            'S3': s3
        }
    
    elif method == 'woodie':
        # 우디 피봇 포인트
        pp = (high + low + 2 * close) / 4
        r1 = (2 * pp) - low
        r2 = pp + (high - low)
        s1 = (2 * pp) - high
        s2 = pp - (high - low)
        
        result = {
            'PP': pp,
            'R1': r1,
            'R2': r2,
            'S1': s1,
            'S2': s2
        }
    
    elif method == 'camarilla':
        # 캐머릴라 피봇 포인트
        pp = (high + low + close) / 3
        r1 = close + (high - low) * 1.1 / 12
        r2 = close + (high - low) * 1.1 / 6
        r3 = close + (high - low) * 1.1 / 4
        r4 = close + (high - low) * 1.1 / 2
        s1 = close - (high - low) * 1.1 / 12
        s2 = close - (high - low) * 1.1 / 6
        s3 = close - (high - low) * 1.1 / 4
        s4 = close - (high - low) * 1.1 / 2
        
        result = {
            'PP': pp,
            'R1': r1,
            'R2': r2,
            'R3': r3,
            'R4': r4,
            'S1': s1,
            'S2': s2,
            'S3': s3,
            'S4': s4
        }
    
    elif method == 'demark':
        # 드마크 피봇 포인트
        if close < open:
            x = high + (low * 2) + close
        elif close > open:
            x = (high * 2) + low + close
        else:
            x = high + low + (close * 2)
        
        pp = x / 4
        r1 = x / 2 - low
        s1 = x / 2 - high
        
        result = {
            'PP': pp,
            'R1': r1,
            'S1': s1
        }
    
    return result