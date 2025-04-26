# 🧩 사용법 예시
```python
import pandas as pd
from visualization_setup import setup_plotting, plot_numeric_columns, plot_correlation_heatmap, plot_top_categories, plot_pairplot

# 1. 스타일 세팅
setup_plotting()

# 2. 데이터 로드
data = pd.read_csv('http://bit.ly/ld-sample-idol')

# 3. 기본 그래프 뿌려보기
plot_numeric_columns(data)
plot_correlation_heatmap(data)
plot_top_categories(data, '그룹')
plot_pairplot(data, hue='그룹')

```


# 🎨 결과

✅ 숫자형 컬럼 히스토그램
✅ 상관관계 히트맵
✅ 범주형 컬럼 Top N 막대그래프
✅ 페어플롯(pairplot) (컬러별 구분까지)

