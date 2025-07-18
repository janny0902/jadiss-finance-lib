# 지표 신호 생성 예제
# 이 예제는 가격 데이터와 일자 데이터를 입력받아 매수/매도 신호를 생성하는 방법을 보여줍니다.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# 라이브러리 경로 추가
sys.path.append(os.path.abspath('..'))

from jadiss_finance_lib.indicator_signals import (
    rsi_signals, macd_signals, bollinger_signals, stochastic_signals,
    parabolic_sar_signals, adx_signals, ichimoku_signals,
    divergence_signals, elliott_wave_signals
)

def generate_sample_data(start_date='2023-01-01', periods=100, freq='D'):
    """샘플 가격 데이터와 일자 데이터 생성"""
    # 날짜 범위 생성
    date_range = pd.date_range(start=start_date, periods=periods, freq=freq)
    dates = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in date_range]
    
    # 기본 가격 생성 (랜덤워크)
    np.random.seed(42)
    price = 100
    prices = [price]
    
    for _ in range(1, periods):
        change = np.random.normal(0, 1)
        price += change
        prices.append(price)
    
    return prices, dates

def main():
    print("===== 지표 신호 생성 예제 =====")
    
    # 1. 일봉 데이터 생성
    print("\n1. 일봉 데이터 생성")
    daily_prices, daily_dates = generate_sample_data(start_date='2023-01-01', periods=100, freq='D')
    print(f"데이터 기간: {daily_dates[0]} ~ {daily_dates[-1]}")
    print(f"데이터 개수: {len(daily_prices)}")
    
    # 2. 분봉 데이터 생성
    print("\n2. 15분봉 데이터 생성")
    minute_prices, minute_dates = generate_sample_data(start_date='2023-07-01', periods=100, freq='15min')
    print(f"데이터 기간: {minute_dates[0]} ~ {minute_dates[-1]}")
    print(f"데이터 개수: {len(minute_prices)}")
    
    # 3. RSI 신호 생성 (일봉)
    print("\n3. RSI 신호 생성 (일봉)")
    rsi_result = rsi_signals(daily_prices, daily_dates, timeframe='D', period=14, overbought=70, oversold=30)
    print(f"매수 신호: {len(rsi_result['buy_signals'])} 개")
    for date in rsi_result['buy_signals'][:3]:
        print(f"  - {date}")
    print(f"매도 신호: {len(rsi_result['sell_signals'])} 개")
    for date in rsi_result['sell_signals'][:3]:
        print(f"  - {date}")
    
    # 4. MACD 신호 생성 (15분봉)
    print("\n4. MACD 신호 생성 (15분봉)")
    macd_result = macd_signals(minute_prices, minute_dates, timeframe=15, fast=12, slow=26, signal=9)
    print(f"매수 신호: {len(macd_result['buy_signals'])} 개")
    for date in macd_result['buy_signals'][:3]:
        print(f"  - {date}")
    print(f"매도 신호: {len(macd_result['sell_signals'])} 개")
    for date in macd_result['sell_signals'][:3]:
        print(f"  - {date}")
    
    # 5. 볼린저 밴드 신호 생성 (일봉)
    print("\n5. 볼린저 밴드 신호 생성 (일봉)")
    bb_result = bollinger_signals(daily_prices, daily_dates, timeframe='D', period=20, std_dev=2)
    print(f"매수 신호: {len(bb_result['buy_signals'])} 개")
    for date in bb_result['buy_signals'][:3]:
        print(f"  - {date}")
    print(f"매도 신호: {len(bb_result['sell_signals'])} 개")
    for date in bb_result['sell_signals'][:3]:
        print(f"  - {date}")
    
    # 6. 패러볼릭 SAR 신호 생성 (일봉)
    print("\n6. 패러볼릭 SAR 신호 생성 (일봉)")
    sar_result = parabolic_sar_signals(daily_prices, daily_dates, timeframe='D')
    print(f"매수 신호: {len(sar_result['buy_signals'])} 개")
    for date in sar_result['buy_signals'][:3]:
        print(f"  - {date}")
    print(f"매도 신호: {len(sar_result['sell_signals'])} 개")
    for date in sar_result['sell_signals'][:3]:
        print(f"  - {date}")
    
    # 7. 특정 일자 입력 예시 (2025-07-18 10:00:00)
    print("\n7. 특정 일자 입력 예시 (2025-07-18 10:00:00)")
    specific_date = '2025-07-18 10:00:00'
    print(f"입력 일자: {specific_date}")
    print("이 일자를 포함한 데이터로 신호를 생성하려면 해당 일자를 포함하는 가격 데이터와 일자 데이터를 입력하세요.")
    
    # 예시: 2025-07-18 전후 데이터 생성
    future_prices, future_dates = generate_sample_data(start_date='2025-07-01', periods=30, freq='D')
    print(f"생성된 데이터 기간: {future_dates[0]} ~ {future_dates[-1]}")
    
    # 8. 다양한 분봉 단위 예시
    print("\n8. 다양한 분봉 단위 예시")
    for minute in [1, 5, 15, 30, 60, 180]:
        print(f"\n{minute}분봉 데이터 처리:")
        minute_data_prices, minute_data_dates = generate_sample_data(
            start_date='2023-07-01', periods=100, freq=f'{minute}min'
        )
        result = rsi_signals(minute_data_prices, minute_data_dates, timeframe=minute)
        print(f"매수 신호: {len(result['buy_signals'])} 개")
        print(f"매도 신호: {len(result['sell_signals'])} 개")

if __name__ == "__main__":
    main()