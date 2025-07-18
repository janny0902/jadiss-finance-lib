# EPS(Earnings Per Share, 주당순이익)는 기업의 순이익을 발행주식수로 나눈 값으로, 주주가 보유한 주식 1주당 얼마의 이익을 창출했는지를 나타내는 핵심 재무지표입니다.
# EPS의 구성 요소:
# 순이익(Net Income):
# 기업이 일정 기간 동안 벌어들인 최종 이익으로, 모든 비용과 세금을 차감한 후의 이익입니다.
# 발행주식수(Outstanding Shares):
# 현재 시장에서 거래되고 있는 주식의 총 개수입니다.
# EPS의 특징:
# 수익성 측정:
# 기업의 주당 수익성을 직접적으로 보여주는 지표입니다.
# 투자 판단 기준:
# 주식 투자 시 기업의 수익성을 평가하는 핵심 지표 중 하나입니다.
# 시계열 분석:
# 과거 EPS와 비교하여 기업의 성장성을 판단할 수 있습니다.
# 업종 비교:
# 동일 업종 내 다른 기업들과의 수익성 비교가 가능합니다.
# EPS 활용:
# PER 계산: 주가 ÷ EPS = PER(주가수익비율)
# 성장률 분석: (현재 EPS - 과거 EPS) ÷ 과거 EPS × 100
# 배당 정책: EPS가 높을수록 배당 여력이 증가합니다.
# 주의사항:
# 일회성 요인: 특별손익 등 일회성 요인이 포함될 수 있습니다.
# 회계 정책: 회계 정책 변경이 EPS에 영향을 줄 수 있습니다.

import pandas as pd

def eps(net_income, outstanding_shares):
    """
    EPS(주당순이익) 계산
    
    입력 타입:
    net_income (pd.Series): 순이익 데이터 시리즈
    outstanding_shares (pd.Series): 발행주식수 데이터 시리즈
    
    출력 타입:
    dict: {'EPS': pd.Series} - 주당순이익 값을 포함한 딕셔너리
    """
    eps_value = net_income / outstanding_shares
    
    return {
        'EPS': eps_value
    }