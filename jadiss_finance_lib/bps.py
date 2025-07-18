# BPS(Book Value Per Share, 주당순자산가치)는 기업의 순자산을 발행주식수로 나눈 값으로, 주식 1주당 순자산 가치를 나타내는 재무지표입니다.
# BPS의 구성 요소:
# 순자산(Shareholders' Equity):
# 총자산에서 총부채를 차감한 값으로, 주주에게 귀속되는 자산의 순가치입니다.
# 발행주식수(Outstanding Shares):
# 현재 시장에서 거래되고 있는 주식의 총 개수입니다.
# BPS의 특징:
# 청산 가치:
# 기업이 청산될 경우 주주가 받을 수 있는 이론적 가치를 나타냅니다.
# 안정성 지표:
# 기업의 재무 안정성과 자본 구조를 평가하는 데 사용됩니다.
# 장부 가치:
# 회계상 기록된 자산의 장부 가치를 기준으로 계산됩니다.
# 보수적 평가:
# 시장 가치보다 보수적인 기업 가치 평가 방법입니다.
# BPS 활용:
# PBR 계산: 주가 ÷ BPS = PBR(주가순자산비율)
# 저평가 판단: 주가가 BPS보다 낮으면 저평가 가능성
# 재무 안정성: BPS 증가 추세는 재무 안정성 개선을 의미
# 배당 능력: 높은 BPS는 배당 지급 능력을 뒷받침
# 주의사항:
# 장부 가치 한계: 실제 시장 가치와 차이가 클 수 있습니다.
# 업종별 차이: 자산 집약적 업종과 서비스업 간 BPS 의미가 다릅니다.

import pandas as pd

def bps(shareholders_equity, outstanding_shares):
    """
    BPS(주당순자산가치) 계산
    
    입력 타입:
    shareholders_equity (pd.Series): 순자산(자기자본) 데이터 시리즈
    outstanding_shares (pd.Series): 발행주식수 데이터 시리즈
    
    출력 타입:
    dict: {'BPS': pd.Series} - 주당순자산가치 값을 포함한 딕셔너리
    """
    bps_value = shareholders_equity / outstanding_shares
    
    return {
        'BPS': bps_value
    }