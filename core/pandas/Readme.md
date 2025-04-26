# 🧩 사용법 예시

```python
import pandas as pd
from pandas_setup import setup_pandas_display, reset_pandas_display, apply_default_styling

# 1. 세팅 적용
setup_pandas_display()

# 2. 데이터 불러오기
data = pd.read_csv('http://bit.ly/ld-sample-idol', index_col='순위')

# 3. 스타일 적용해서 보기
styled_data = apply_default_styling(data)
styled_data

# 4. 세팅 리셋
reset_pandas_display()
```

# 📌 요약 기능

|기능|	설명|
|--|--|
|음수값 빨간색 표시|	숫자가 음수면 자동으로 빨간색 텍스트|
|숫자 컬럼 블루 그라데이션|	숫자 범위에 따라 파란색 단계적으로 채색|
|결측치(lightcoral) 하이라이트|	NaN, Null 값은 밝은 코랄색으로 표시|
|중앙 정렬 + 테두리|	깔끔한 테이블 모양|
|포맷팅 (천 단위 쉼표 + 소수점 1자리)|	숫자 가독성 극대화|
