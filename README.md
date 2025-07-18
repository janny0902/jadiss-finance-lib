# Jadiss Finance Library

금융 기술적 분석 및 밸류에이션 지표를 제공하는 Python 라이브러리입니다.

## 설치 및 테스트 가이드

### 1. 가상환경 생성 및 활성화
```bash
# 가상환경 생성
python -m venv env

# 가상환경 활성화 (Windows)
env\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source env/bin/activate
```

### 2. 필요한 패키지 설치
```bash
# 기본 패키지 설치
pip install pandas numpy

# 테스트 패키지 설치
pip install pytest
```

### 3. 라이브러리 설치
```bash
# 개발 모드로 설치
pip install -e .
```

### 4. 전체 테스트 실행
```bash
# 모든 테스트 실행
pytest tests/

# 상세한 출력과 함께 테스트 실행
pytest tests/ -v

# 특정 테스트 파일만 실행
pytest tests/test_rsi.py -v
```

### 5. 개별 지표 테스트
```bash
# 기술적 지표 테스트
pytest tests/test_rsi.py tests/test_macd.py tests/test_bollinger_bands.py -v

# 스토캐스틱 지표 테스트
pytest tests/test_stochastic_slow.py tests/test_stochastic_fast.py -v

# 패러볼릭 지표 테스트
pytest tests/test_parabolic.py tests/test_parabolic_sar.py -v

# 일목균형표 테스트
pytest tests/test_ichimoku.py -v

# 밸류에이션 지표 테스트
pytest tests/test_eps.py tests/test_bps.py tests/test_sps.py -v

# 비율 지표 테스트
pytest tests/test_per.py tests/test_pbr.py tests/test_psr.py -v

# ROE 및 표준편차 테스트
pytest tests/test_roe.py tests/test_standard_deviation.py -v

# 기술적 분석 기법 테스트
pytest tests/test_elliott_wave.py tests/test_divergence.py -v
```

### 6. 사용 예시
```python
import pandas as pd
from jadiss_finance_lib.rsi import rsi
from jadiss_finance_lib.macd import macd
from jadiss_finance_lib.eps import eps

# 샘플 데이터
prices = pd.Series([100, 101, 102, 101, 100, 98, 99, 100, 101, 102])

# RSI 계산
rsi_result = rsi(prices, period=7)
print(rsi_result['RSI'])

# MACD 계산
macd_result = macd(prices, fast=5, slow=10, signal=3)
print(macd_result['MACD'])

# EPS 계산
net_income = pd.Series([1000, 1100, 1200])
shares = pd.Series([100, 100, 110])
eps_result = eps(net_income, shares)
print(eps_result['EPS'])

# 엘리어트 파동 감지
from jadiss_finance_lib.elliott_wave import elliott_wave_detector
wave_result = elliott_wave_detector(prices, window_size=10)
if wave_result['wave_1_2']:
    print("1,2파 진행 중")

# 다이버전스 감지
from jadiss_finance_lib.divergence import divergence
div_result = divergence(prices, 'rsi', period=14)
if div_result['bullish']:
    print("상승 반전 신호 감지!")
```

### 6-1. 지표 신호 생성 예시 (가격과 일자 입력)
```python
import pandas as pd
from jadiss_finance_lib.indicator_signals import rsi_signals, macd_signals, bollinger_signals

# 가격과 일자 데이터 준비
prices = [100, 101, 102, 103, 104, 105, 106, 105, 104, 103]
dates = [
    '2025-07-18 10:00:00', '2025-07-18 11:00:00', '2025-07-18 12:00:00',
    '2025-07-18 13:00:00', '2025-07-18 14:00:00', '2025-07-18 15:00:00',
    '2025-07-19 10:00:00', '2025-07-19 11:00:00', '2025-07-19 12:00:00',
    '2025-07-19 13:00:00'
]

# 일봉 데이터로 RSI 신호 생성
rsi_result = rsi_signals(prices, dates, timeframe='D', period=14, overbought=70, oversold=30)
print(f"일봉 RSI 매수 신호: {rsi_result['buy_signals']}")
print(f"일봉 RSI 매도 신호: {rsi_result['sell_signals']}")

# 60분봉 데이터로 MACD 신호 생성
macd_result = macd_signals(prices, dates, timeframe=60, fast=12, slow=26, signal=9)
print(f"60분봉 MACD 매수 신호: {macd_result['buy_signals']}")
print(f"60분봉 MACD 매도 신호: {macd_result['sell_signals']}")

# 볼린저 밴드 신호 생성
bb_result = bollinger_signals(prices, dates, timeframe=60, period=5, std_dev=2)
print(f"볼린저 밴드 매수 신호: {bb_result['buy_signals']}")
print(f"볼린저 밴드 매도 신호: {bb_result['sell_signals']}")
```

### 6-2. 다양한 분봉 단위 사용 예시
```python
from jadiss_finance_lib.indicator_signals import stochastic_signals

# 가격과 일자 데이터
prices = [100, 101, 102, 103, 104, 105, 106, 105, 104, 103]
dates = [
    '2025-07-18 10:00:00', '2025-07-18 10:01:00', '2025-07-18 10:02:00',
    '2025-07-18 10:03:00', '2025-07-18 10:04:00', '2025-07-18 10:05:00',
    '2025-07-18 10:06:00', '2025-07-18 10:07:00', '2025-07-18 10:08:00',
    '2025-07-18 10:09:00'
]

# 다양한 분봉 단위로 신호 생성
for minute in [1, 3, 5]:
    result = stochastic_signals(prices, dates, timeframe=minute)
    print(f"{minute}분봉 스토캐스틱 매수 신호: {result['buy_signals']}")
    print(f"{minute}분봉 스토캐스틱 매도 신호: {result['sell_signals']}")
```

### 7. 포함된 지표들

#### 추세 분석 지표
- **RSI**: 상대강도지수
- **MACD**: 이동평균수렴확산
- **MACD OCI**: MACD 옵션체인지표
- **Parabolic**: 패러볼릭
- **Parabolic SAR**: 패러볼릭 SAR
- **ADX**: 평균 방향성 지수

#### 모멘텀 및 오실레이터 지표
- **RSI**: 상대강도지수
- **Stochastic Slow**: 스토캐스틱 슬로우
- **Stochastic Fast**: 스토캐스틱 패스트
- **ROC**: 변화율
- **CCI**: 상품채널지수

#### 변동성 분석 지표
- **Bollinger Bands**: 볼린저 밴드
- **ATR**: 평균 실제 범위
- **Keltner Channel**: 켈트너 채널
- **Donchian Channel**: 돌치안 채널
- **Standard Deviation**: 표준편차 기반 표준화 점수

#### 거래량 기반 지표
- **OBV**: 온밸런스 볼륨
- **CMF**: 차이킨 자금 흐름
- **VR**: 거래량 비율

#### 지지/저항 분석 지표
- **Fibonacci Retracement**: 피보나치 되돌림
- **Pivot Points**: 피봇 포인트

#### 종합 분석 지표
- **Ichimoku**: 일목균형표

#### 기술적 분석 기법
- **Elliott Wave**: 엘리어트 파동 분석 - 가격 시리즈에서 1,2파, 3,4파, b,c파 패턴 감지
- **Divergence**: 다이버전스 분석 - 가격과 지표 간의 불일치를 통한 반전 신호 감지
- **Chart Patterns**: 차트 패턴 분석 - 헤드 앤 슈더, 이중 천장/바닥 등 패턴 감지
- **Candle Patterns**: 캥들 패턴 분석 - 해머형, 유성형, 장악형 등 패턴 감지

#### 밸류에이션 지표
- **EPS**: 주당순이익
- **BPS**: 주당순자산가치
- **SPS**: 주당매출액
- **PER**: 주가수익비율
- **PBR**: 주가순자산비율
- **PSR**: 주가매출비율
- **ROE**: 자기자본이익률

### 8. 문제 해결
```bash
# 패키지 재설치
pip uninstall jadiss-finance-lib
pip install -e .

# 캐시 클리어 후 테스트
pytest --cache-clear tests/

# 특정 테스트 디버깅 (상세 출력 포함)
pytest tests/test_rsi.py::test_rsi -v -s

# 모든 테스트 상세 출력 포함 실행 (입력값과 결과값 확인)
pytest tests/ -v -s
```