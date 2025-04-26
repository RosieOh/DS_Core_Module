# 📊 노트북 최적화 시각화 자동화 (with Tabs)

import ipywidgets as widgets
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from IPython.display import clear_output, display


def setup_plotting():
    """시각화 기본 스타일 세팅."""
    sns.set_theme(
        style='whitegrid',
        palette='pastel',
        font_scale=1.2,
        rc={
            'figure.figsize': (10, 6),
            'axes.titlesize': 18,
            'axes.labelsize': 14,
            'legend.fontsize': 12
        }
    )
    plt.rcParams['axes.unicode_minus'] = False
    print("✅ [Visualization Setup] Plotting style applied!")


def plot_numeric_columns(df):
    """숫자형 컬럼 히스토그램."""
    numeric_cols = df.select_dtypes(include='number').columns
    if numeric_cols.empty:
        print("⚠️ No numeric columns to plot.")
        return
    df[numeric_cols].hist(bins=20, figsize=(15, 10), color='skyblue', edgecolor='black')
    plt.suptitle('Numeric Columns Distribution', fontsize=20)
    plt.tight_layout()
    plt.show()


def plot_correlation_heatmap(df):
    """상관관계 히트맵."""
    numeric_cols = df.select_dtypes(include='number')
    if numeric_cols.empty:
        print("⚠️ No numeric columns for correlation heatmap.")
        return
    corr = numeric_cols.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Heatmap', fontsize=18)
    plt.show()


def plot_top_categories(df, column, top_n=10):
    """범주형 컬럼 Top N 시각화."""
    if column not in df.columns:
        print(f"⚠️ Column '{column}' not found.")
        return
    counts = df[column].value_counts().head(top_n)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=counts.values, y=counts.index, palette='muted')
    plt.title(f'Top {top_n} Categories in {column}', fontsize=18)
    plt.xlabel('Count')
    plt.ylabel(column)
    plt.show()


def plot_pairplot(df, hue=None):
    """숫자형 컬럼 쌍플롯(pairplot)."""
    numeric_cols = df.select_dtypes(include='number')
    if numeric_cols.empty:
        print("⚠️ No numeric columns for pairplot.")
        return
    sns.pairplot(df, hue=hue, palette='pastel')
    plt.suptitle('Pairplot of Numeric Columns', fontsize=20, y=1.02)
    plt.show()


def plot_all_tabs(
    df,
    category_col=None,
    hue=None,
    top_n=10
):
    """
    모든 기본 시각화를 Tab으로 구분해서 한 번에 보여줍니다.
    노트북 전용!

    Args:
        df (pd.DataFrame): 데이터프레임
        category_col (str, optional): 범주형 컬럼명
        hue (str, optional): 페어플롯 구분 기준 컬럼
        top_n (int, optional): 범주형 상위 몇 개까지만
    """

    tab_titles = ['Numeric Columns', 'Correlation Heatmap', 'Top Categories', 'Pairplot']
    tab_contents = []

    # 탭별로 그래프 그리기
    for tab_title in tab_titles:
        output = widgets.Output()

        with output:
            clear_output(wait=True)
            if tab_title == 'Numeric Columns':
                plot_numeric_columns(df)
            elif tab_title == 'Correlation Heatmap':
                plot_correlation_heatmap(df)
            elif tab_title == 'Top Categories':
                if category_col:
                    plot_top_categories(df, column=category_col, top_n=top_n)
                else:
                    print("⚠️ No category column specified.")
            elif tab_title == 'Pairplot':
                plot_pairplot(df, hue=hue)

        tab_contents.append(output)

    # Tab 위젯 만들기
    tabs = widgets.Tab(children=tab_contents)
    for i, title in enumerate(tab_titles):
        tabs.set_title(i, title)

    display(tabs)

    print("\n✅ [Visualization] All plots generated in Tabs!")
