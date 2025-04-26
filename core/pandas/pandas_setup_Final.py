import warnings

import numpy as np
import pandas as pd


def setup_pandas_display():
    """Pandas 출력 기본 세팅."""
    pd.set_option('display.float_format', lambda x: f'{x:,.1f}')
    pd.set_option('display.integer_format', lambda x: f'{x:,}')
    pd.set_option('display.precision', 1)
    pd.set_option('display.max_columns', 100)
    pd.set_option('display.max_rows', 100)
    pd.set_option('display.max_colwidth', 200)
    warnings.filterwarnings('ignore')
    pd.options.display.html.table_schema = True
    pd.options.display.html.table_border = 1
    print("✅ [Pandas Setup] Display settings applied!")


def reset_pandas_display():
    """Pandas 출력 및 경고 설정 리셋."""
    pd.reset_option('all')
    warnings.resetwarnings()
    print("🔄 [Pandas Setup] Display settings reset to default.")


def highlight_top_votes(s, threshold=5_000_000):
    """총득표수가 특정 임계값(threshold) 이상이면 금색 배경."""
    is_high = s > threshold
    return ['background-color: gold; font-weight: bold;' if v else '' for v in is_high]


def bold_names(s):
    """이름 컬럼은 항상 볼드체로."""
    return ['font-weight: bold;' for _ in s]


def style_columns(df: pd.DataFrame) -> pd.io.formats.style.Styler:
    """
    컬럼별 맞춤형 스타일 적용:
    - 이름 컬럼: 볼드체
    - 총득표수: 상위는 금색 강조
    - 숫자 컬럼: 블루 그라데이션
    - 결측치: 코랄색 표시
    """
    styler = df.style

    # 기본 스타일
    styler = styler.set_properties(**{'text-align': 'center'})
    styler = styler.set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center')]},
        {'selector': 'td', 'props': [('border', '1px solid #ddd')]}
    ])

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # 🎯 숫자 컬럼 포맷
    styler = styler.format(na_rep='-', formatter={col: "{:,.1f}".format for col in numeric_cols})

    # 🎨 컬럼별 스타일 매핑
    if '총득표수' in df.columns:
        styler = styler.apply(highlight_top_votes, subset=['총득표수'])

    if '이름' in df.columns:
        styler = styler.apply(bold_names, subset=['이름'])

    # 📈 숫자 컬럼: 그라데이션
    styler = styler.background_gradient(subset=numeric_cols, cmap='Blues')

    # 🚨 결측치 하이라이트
    styler = styler.highlight_null(null_color='lightcoral')

    return styler


# import pandas as pd
# from pandas_super_star_styler import setup_pandas_display, reset_pandas_display, style_columns

# # 1. 기본 세팅 적용
# setup_pandas_display()

# # 2. 데이터 불러오기
# data = pd.read_csv('http://bit.ly/ld-sample-idol', index_col='순위')

# # 3. 슈퍼스타일링 적용
# styled_data = style_columns(data)
# styled_data

# # 4. 필요시 초기화
# reset_pandas_display()
