import warnings

import numpy as np
import pandas as pd


def setup_pandas_display():
    """
    Pandas 출력 설정을 고급 버전으로 세팅합니다.
    """
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
    """
    Pandas 출력 및 경고 설정을 기본으로 리셋합니다.
    """
    pd.reset_option('all')
    warnings.resetwarnings()
    print("🔄 [Pandas Setup] Display settings reset to default.")


def apply_super_styling(df: pd.DataFrame) -> pd.io.formats.style.Styler:
    """
    데이터프레임에 고급 스타일 적용:
    - 중앙 정렬
    - 컬럼별 자동 스타일링
    - 음수값 빨간색 표시
    - 결측치 하이라이트
    - 숫자는 색상 그라데이션
    """
    # 숫자 컬럼 식별
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # 스타일링 시작
    styler = df.style

    # 📋 중앙 정렬
    styler = styler.set_properties(**{'text-align': 'center'})
    styler = styler.set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center')]},
        {'selector': 'td', 'props': [('border', '1px solid #ddd')]}
    ])

    # 📈 숫자 컬럼: 음수는 빨간색 표시
    styler = styler.format(na_rep='-', formatter={col: "{:,.1f}".format for col in numeric_cols})
    styler = styler.applymap(lambda v: 'color: red;' if isinstance(v, (int, float)) and v < 0 else '', subset=numeric_cols)

    # 🎨 숫자 컬럼: 그라데이션(컬러맵)
    styler = styler.background_gradient(subset=numeric_cols, cmap='Blues')

    # 🚨 결측치 하이라이트
    styler = styler.highlight_null(null_color='lightcoral')

    return styler
