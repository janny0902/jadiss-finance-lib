# 지표 신호 생성기(Indicator Signals)는 각 기술적 지표에 대해 가격 데이터와 일자 정보를 입력받아
# 매수/매도 신호를 생성하는 유틸리티입니다.
# 지원하는 시간 프레임:
# - 일봉(Daily): 'D'로 표시
# - 분봉(Minutes): 1, 3, 5, 10, 15, 30, 60, 180 등 정수로 표시
# 입력 형식:
# - 일자: 'YYYY-MM-DD HH:MM:SS' 형식의 문자열
# 출력 형식:
# - 매수/매도 신호: 'YYYY-MM-DD HH:MM:SS' 형식의 문자열 리스트

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def process_data(prices, dates, timeframe='D'):
    """
    가격 데이터와 일자 데이터를 처리하여 DataFrame으로 변환
    
    Parameters:
    prices (list or pd.Series): 가격 데이터
    dates (list or pd.Series): 일자 데이터 ('YYYY-MM-DD HH:MM:SS' 형식)
    timeframe (str or int): 시간 프레임 ('D' 또는 분 단위 정수)
    
    Returns:
    pd.DataFrame: 처리된 OHLCV 데이터
    """
    # 데이터 프레임 생성
    df = pd.DataFrame({
        'date': pd.to_datetime(dates),
        'price': prices
    })
    
    # 날짜를 인덱스로 설정
    df.set_index('date', inplace=True)
    
    # 시간 프레임에 따라 리샘플링
    if timeframe == 'D':
        # 일봉 데이터
        resampled = df.resample('D').agg({
            'price': ['first', 'max', 'min', 'last']
        })
    else:
        # 분봉 데이터
        try:
            minutes = int(timeframe)
            resampled = df.resample(f'{minutes}min').agg({
                'price': ['first', 'max', 'min', 'last']
            })
        except ValueError:
            raise ValueError(f"지원하지 않는 시간 프레임입니다: {timeframe}")
    
    # 컬럼명 변경
    resampled.columns = ['open', 'high', 'low', 'close']
    
    # NaN 값 제거
    resampled.dropna(inplace=True)
    
    return resampled

def rsi_signals(prices, dates, timeframe='D', period=14, overbought=70, oversold=30):
    """
    RSI 기반 매수/매도 신호 생성
    
    Parameters:
    prices (list or pd.Series): 가격 데이터
    dates (list or pd.Series): 일자 데이터 ('YYYY-MM-DD HH:MM:SS' 형식)
    timeframe (str or int): 시간 프레임 ('D' 또는 분 단위 정수)
    period (int): RSI 계산 기간
    overbought (int): 과매수 기준값
    oversold (int): 과매도 기준값
    
    Returns:
    dict: {
        'buy_signals': 매수 신호 일자 리스트,
        'sell_signals': 매도 신호 일자 리스트
    }
    """
    from jadiss_finance_lib.rsi import rsi
    
    # 데이터 처리
    data = process_data(prices, dates, timeframe)
    
    # RSI 계산
    result = rsi(data['close'], period=period)
    rsi_values = result['RSI']
    
    # 신호 생성
    buy_signals = []
    sell_signals = []
    
    for i in range(1, len(rsi_values)):
        # 매수 신호: RSI가 과매도 구간에서 상승 반전
        if rsi_values.iloc[i-1] <= oversold and rsi_values.iloc[i] > oversold:
            buy_signals.append(rsi_values.index[i].strftime('%Y-%m-%d %H:%M:%S'))
        
        # 매도 신호: RSI가 과매수 구간에서 하락 반전
        if rsi_values.iloc[i-1] >= overbought and rsi_values.iloc[i] < overbought:
            sell_signals.append(rsi_values.index[i].strftime('%Y-%m-%d %H:%M:%S'))
    
    return {
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    }

def macd_signals(prices, dates, timeframe='D', fast=12, slow=26, signal=9):
    """
    MACD 기반 매수/매도 신호 생성
    
    Parameters:
    prices (list or pd.Series): 가격 데이터
    dates (list or pd.Series): 일자 데이터 ('YYYY-MM-DD HH:MM:SS' 형식)
    timeframe (str or int): 시간 프레임 ('D' 또는 분 단위 정수)
    fast (int): 단기 EMA 기간
    slow (int): 장기 EMA 기간
    signal (int): 시그널 라인 기간
    
    Returns:
    dict: {
        'buy_signals': 매수 신호 일자 리스트,
        'sell_signals': 매도 신호 일자 리스트
    }
    """
    from jadiss_finance_lib.macd import macd
    
    # 데이터 처리
    data = process_data(prices, dates, timeframe)
    
    # MACD 계산
    result = macd(data['close'], fast=fast, slow=slow, signal=signal)
    macd_line = result['MACD']
    signal_line = result['Signal']
    
    # 신호 생성
    buy_signals = []
    sell_signals = []
    
    for i in range(1, len(macd_line)):
        # 매수 신호: MACD가 시그널 라인을 상향 돌파
        if macd_line.iloc[i-1] <= signal_line.iloc[i-1] and macd_line.iloc[i] > signal_line.iloc[i]:
            buy_signals.append(macd_line.index[i].strftime('%Y-%m-%d %H:%M:%S'))
        
        # 매도 신호: MACD가 시그널 라인을 하향 돌파
        if macd_line.iloc[i-1] >= signal_line.iloc[i-1] and macd_line.iloc[i] < signal_line.iloc[i]:
            sell_signals.append(macd_line.index[i].strftime('%Y-%m-%d %H:%M:%S'))
    
    return {
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    }

def bollinger_signals(prices, dates, timeframe='D', period=20, std_dev=2):
    """
    볼린저 밴드 기반 매수/매도 신호 생성
    
    Parameters:
    prices (list or pd.Series): 가격 데이터
    dates (list or pd.Series): 일자 데이터 ('YYYY-MM-DD HH:MM:SS' 형식)
    timeframe (str or int): 시간 프레임 ('D' 또는 분 단위 정수)
    period (int): 이동평균 기간
    std_dev (float): 표준편차 배수
    
    Returns:
    dict: {
        'buy_signals': 매수 신호 일자 리스트,
        'sell_signals': 매도 신호 일자 리스트
    }
    """
    from jadiss_finance_lib.bollinger_bands import bollinger_bands
    
    # 데이터 처리
    data = process_data(prices, dates, timeframe)
    
    # 볼린저 밴드 계산
    result = bollinger_bands(data['close'], period=period, std_dev=std_dev)
    upper = result['Upper']
    lower = result['Lower']
    
    # 신호 생성
    buy_signals = []
    sell_signals = []
    
    for i in range(1, len(data['close'])):
        # 매수 신호: 가격이 하단 밴드 아래로 갔다가 다시 위로
        if data['close'].iloc[i-1] <= lower.iloc[i-1] and data['close'].iloc[i] > lower.iloc[i]:
            buy_signals.append(data.index[i].strftime('%Y-%m-%d %H:%M:%S'))
        
        # 매도 신호: 가격이 상단 밴드 위로 갔다가 다시 아래로
        if data['close'].iloc[i-1] >= upper.iloc[i-1] and data['close'].iloc[i] < upper.iloc[i]:
            sell_signals.append(data.index[i].strftime('%Y-%m-%d %H:%M:%S'))
    
    return {
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    }

def stochastic_signals(prices, dates, timeframe='D', k_period=14, d_period=3, overbought=80, oversold=20):
    """
    스토캐스틱 기반 매수/매도 신호 생성
    
    Parameters:
    prices (list or pd.Series): 가격 데이터
    dates (list or pd.Series): 일자 데이터 ('YYYY-MM-DD HH:MM:SS' 형식)
    timeframe (str or int): 시간 프레임 ('D' 또는 분 단위 정수)
    k_period (int): %K 계산 기간
    d_period (int): %D 계산 기간
    overbought (int): 과매수 기준값
    oversold (int): 과매도 기준값
    
    Returns:
    dict: {
        'buy_signals': 매수 신호 일자 리스트,
        'sell_signals': 매도 신호 일자 리스트
    }
    """
    from jadiss_finance_lib.stochastic_slow import stochastic_slow
    
    # 데이터 처리
    data = process_data(prices, dates, timeframe)
    
    # 스토캐스틱 계산
    result = stochastic_slow(data['high'], data['low'], data['close'], k_period=k_period, d_period=d_period)
    k = result['%K']
    d = result['%D']
    
    # 신호 생성
    buy_signals = []
    sell_signals = []
    
    for i in range(1, len(k)):
        # 매수 신호: %K가 %D를 상향 돌파하고 둘 다 과매도 구간에 있을 때
        if k.iloc[i-1] <= d.iloc[i-1] and k.iloc[i] > d.iloc[i] and k.iloc[i] < oversold:
            buy_signals.append(k.index[i].strftime('%Y-%m-%d %H:%M:%S'))
        
        # 매도 신호: %K가 %D를 하향 돌파하고 둘 다 과매수 구간에 있을 때
        if k.iloc[i-1] >= d.iloc[i-1] and k.iloc[i] < d.iloc[i] and k.iloc[i] > overbought:
            sell_signals.append(k.index[i].strftime('%Y-%m-%d %H:%M:%S'))
    
    return {
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    }

def parabolic_sar_signals(prices, dates, timeframe='D', af_start=0.02, af_increment=0.02, af_max=0.2):
    """
    패러볼릭 SAR 기반 매수/매도 신호 생성
    
    Parameters:
    prices (list or pd.Series): 가격 데이터
    dates (list or pd.Series): 일자 데이터 ('YYYY-MM-DD HH:MM:SS' 형식)
    timeframe (str or int): 시간 프레임 ('D' 또는 분 단위 정수)
    af_start (float): 초기 가속도 인수
    af_increment (float): 가속도 증가량
    af_max (float): 최대 가속도 인수
    
    Returns:
    dict: {
        'buy_signals': 매수 신호 일자 리스트,
        'sell_signals': 매도 신호 일자 리스트
    }
    """
    from jadiss_finance_lib.parabolic_sar import parabolic_sar
    
    # 데이터 처리
    data = process_data(prices, dates, timeframe)
    
    # 패러볼릭 SAR 계산
    result = parabolic_sar(data['high'], data['low'], af_start=af_start, af_increment=af_increment, af_max=af_max)
    trend = result['Trend']
    
    # 신호 생성
    buy_signals = []
    sell_signals = []
    
    for i in range(1, len(trend)):
        # 매수 신호: 추세가 하락에서 상승으로 전환
        if trend.iloc[i-1] == -1 and trend.iloc[i] == 1:
            buy_signals.append(trend.index[i].strftime('%Y-%m-%d %H:%M:%S'))
        
        # 매도 신호: 추세가 상승에서 하락으로 전환
        if trend.iloc[i-1] == 1 and trend.iloc[i] == -1:
            sell_signals.append(trend.index[i].strftime('%Y-%m-%d %H:%M:%S'))
    
    return {
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    }

def adx_signals(prices, dates, timeframe='D', period=14, threshold=25):
    """
    ADX 기반 매수/매도 신호 생성
    
    Parameters:
    prices (list or pd.Series): 가격 데이터
    dates (list or pd.Series): 일자 데이터 ('YYYY-MM-DD HH:MM:SS' 형식)
    timeframe (str or int): 시간 프레임 ('D' 또는 분 단위 정수)
    period (int): ADX 계산 기간
    threshold (int): ADX 임계값
    
    Returns:
    dict: {
        'buy_signals': 매수 신호 일자 리스트,
        'sell_signals': 매도 신호 일자 리스트
    }
    """
    from jadiss_finance_lib.adx import adx
    
    # 데이터 처리
    data = process_data(prices, dates, timeframe)
    
    # ADX 계산
    result = adx(data['high'], data['low'], data['close'], period=period)
    adx_values = result['ADX']
    plus_di = result['+DI']
    minus_di = result['-DI']
    
    # 신호 생성
    buy_signals = []
    sell_signals = []
    
    for i in range(1, len(adx_values)):
        # 매수 신호: ADX > 임계값이고 +DI가 -DI를 상향 돌파
        if (adx_values.iloc[i] > threshold and 
            plus_di.iloc[i-1] <= minus_di.iloc[i-1] and 
            plus_di.iloc[i] > minus_di.iloc[i]):
            buy_signals.append(adx_values.index[i].strftime('%Y-%m-%d %H:%M:%S'))
        
        # 매도 신호: ADX > 임계값이고 -DI가 +DI를 상향 돌파
        if (adx_values.iloc[i] > threshold and 
            minus_di.iloc[i-1] <= plus_di.iloc[i-1] and 
            minus_di.iloc[i] > plus_di.iloc[i]):
            sell_signals.append(adx_values.index[i].strftime('%Y-%m-%d %H:%M:%S'))
    
    return {
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    }

def ichimoku_signals(prices, dates, timeframe='D', tenkan_period=9, kijun_period=26, senkou_b_period=52, displacement=26):
    """
    일목균형표 기반 매수/매도 신호 생성
    
    Parameters:
    prices (list or pd.Series): 가격 데이터
    dates (list or pd.Series): 일자 데이터 ('YYYY-MM-DD HH:MM:SS' 형식)
    timeframe (str or int): 시간 프레임 ('D' 또는 분 단위 정수)
    tenkan_period (int): 전환선 기간
    kijun_period (int): 기준선 기간
    senkou_b_period (int): 선행스팬B 기간
    displacement (int): 이동 기간
    
    Returns:
    dict: {
        'buy_signals': 매수 신호 일자 리스트,
        'sell_signals': 매도 신호 일자 리스트
    }
    """
    from jadiss_finance_lib.ichimoku import ichimoku
    
    # 데이터 처리
    data = process_data(prices, dates, timeframe)
    
    # 일목균형표 계산
    result = ichimoku(data['high'], data['low'], data['close'], 
                     tenkan_period=tenkan_period, 
                     kijun_period=kijun_period, 
                     senkou_b_period=senkou_b_period, 
                     displacement=displacement)
    
    tenkan = result['Tenkan']
    kijun = result['Kijun']
    
    # 신호 생성
    buy_signals = []
    sell_signals = []
    
    for i in range(1, len(tenkan)):
        # 매수 신호: 전환선이 기준선을 상향 돌파 (골든크로스)
        if tenkan.iloc[i-1] <= kijun.iloc[i-1] and tenkan.iloc[i] > kijun.iloc[i]:
            buy_signals.append(tenkan.index[i].strftime('%Y-%m-%d %H:%M:%S'))
        
        # 매도 신호: 전환선이 기준선을 하향 돌파 (데드크로스)
        if tenkan.iloc[i-1] >= kijun.iloc[i-1] and tenkan.iloc[i] < kijun.iloc[i]:
            sell_signals.append(tenkan.index[i].strftime('%Y-%m-%d %H:%M:%S'))
    
    return {
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    }

def divergence_signals(prices, dates, timeframe='D', indicator_name='rsi', **indicator_params):
    """
    다이버전스 기반 매수/매도 신호 생성
    
    Parameters:
    prices (list or pd.Series): 가격 데이터
    dates (list or pd.Series): 일자 데이터 ('YYYY-MM-DD HH:MM:SS' 형식)
    timeframe (str or int): 시간 프레임 ('D' 또는 분 단위 정수)
    indicator_name (str): 사용할 지표 이름
    **indicator_params: 지표별 추가 매개변수
    
    Returns:
    dict: {
        'buy_signals': 매수 신호 일자 리스트,
        'sell_signals': 매도 신호 일자 리스트
    }
    """
    from jadiss_finance_lib.divergence import divergence
    
    # 데이터 처리
    data = process_data(prices, dates, timeframe)
    
    # 다이버전스 계산
    result = divergence(data['close'], indicator_name, **indicator_params)
    
    # 신호 생성
    buy_signals = []
    sell_signals = []
    
    # 상승 다이버전스 (매수 신호)
    bullish = result['bullish']
    for i in range(len(bullish)):
        if bullish.iloc[i]:
            buy_signals.append(bullish.index[i].strftime('%Y-%m-%d %H:%M:%S'))
    
    # 하락 다이버전스 (매도 신호)
    bearish = result['bearish']
    for i in range(len(bearish)):
        if bearish.iloc[i]:
            sell_signals.append(bearish.index[i].strftime('%Y-%m-%d %H:%M:%S'))
    
    return {
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    }

def elliott_wave_signals(prices, dates, timeframe='D', **params):
    """
    엘리어트 파동 기반 매수/매도 신호 생성
    
    Parameters:
    prices (list or pd.Series): 가격 데이터
    dates (list or pd.Series): 일자 데이터 ('YYYY-MM-DD HH:MM:SS' 형식)
    timeframe (str or int): 시간 프레임 ('D' 또는 분 단위 정수)
    **params: 엘리어트 파동 검출 매개변수
    
    Returns:
    dict: {
        'buy_signals': 매수 신호 일자 리스트,
        'sell_signals': 매도 신호 일자 리스트
    }
    """
    from jadiss_finance_lib.elliott_wave import elliott_wave_detector
    
    # 데이터 처리
    data = process_data(prices, dates, timeframe)
    
    # 엘리어트 파동 계산
    result = elliott_wave_detector(data['close'], **params)
    
    # 신호 생성
    buy_signals = []
    sell_signals = []
    
    # 1,2파 완료 후 3파 시작 지점 (매수 신호)
    wave_1_2 = result['wave_1_2']
    for i in range(len(wave_1_2)):
        if wave_1_2[i]:
            buy_signals.append(data.index[i].strftime('%Y-%m-%d %H:%M:%S'))
    
    # 5파 완료 후 a,b,c 시작 지점 (매도 신호)
    wave_b_c = result['wave_b_c']
    for i in range(len(wave_b_c)):
        if wave_b_c[i]:
            sell_signals.append(data.index[i].strftime('%Y-%m-%d %H:%M:%S'))
    
    return {
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    }