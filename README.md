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
```

### 7. 포함된 지표들

#### 기술적 지표
- **RSI**: 상대강도지수
- **MACD**: 이동평균수렴확산
- **MACD OCI**: MACD 옵션체인지표
- **Stochastic Slow**: 스토캐스틱 슬로우
- **Stochastic Fast**: 스토캐스틱 패스트
- **Bollinger Bands**: 볼린저 밴드
- **Parabolic**: 패러볼릭
- **Parabolic SAR**: 패러볼릭 SAR
- **Ichimoku**: 일목균형표
- **Standard Deviation**: 표준편차 기반 표준화 점수

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

# 특정 테스트 디버깅
pytest tests/test_rsi.py::test_rsi -v -s
```