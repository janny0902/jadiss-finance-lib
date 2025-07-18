# SPS(Sales Per Share, 주당매출액)는 기업의 총매출액을 발행주식수로 나눈 값으로, 주식 1주당 매출액을 나타내는 재무지표입니다.
# SPS의 구성 요소:
# 총매출액(Total Sales/Revenue):
# 기업이 일정 기간 동안 상품이나 서비스 판매로 얻은 총수익입니다.
# 발행주식수(Outstanding Shares):
# 현재 시장에서 거래되고 있는 주식의 총 개수입니다.
# SPS의 특징:
# 매출 효율성:
# 주당 얼마의 매출을 창출하는지를 보여주는 효율성 지표입니다.
# 성장성 지표:
# 시계열 분석을 통해 기업의 매출 성장성을 평가할 수 있습니다.
# 규모 정규화:
# 기업 규모에 관계없이 주당 기준으로 매출을 비교할 수 있습니다.
# 업종 비교:
# 동일 업종 내 기업들의 매출 효율성을 비교하는 데 유용합니다.
# SPS 활용:
# PSR 계산: 주가 ÷ SPS = PSR(주가매출액비율)
# 성장률 분석: (현재 SPS - 과거 SPS) ÷ 과거 SPS × 100
# 매출 효율성: SPS 증가는 주당 매출 증가를 의미
# 밸류에이션: 매출 기준 기업 가치 평가에 활용
# 주의사항:
# 수익성 무관: 매출액만 반영하므로 수익성은 별도 확인 필요
# 일회성 매출: 특별한 일회성 매출이 포함될 수 있습니다.
# 업종별 차이: 업종에 따라 SPS의 의미와 중요도가 다릅니다.

import pandas as pd

def sps(total_sales, outstanding_shares):
    """
    SPS(주당매출액) 계산
    
    입력 타입:
    total_sales (pd.Series): 총매출액 데이터 시리즈
    outstanding_shares (pd.Series): 발행주식수 데이터 시리즈
    
    출력 타입:
    dict: {'SPS': pd.Series} - 주당매출액 값을 포함한 딕셔너리
    """
    sps_value = total_sales / outstanding_shares
    
    return {
        'SPS': sps_value
    }