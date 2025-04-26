# 📊 노트북 최적화 시각화 프로페셔널 버전

import io

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


def save_current_plot(filename='plot.png'):
    """현재 플롯 저장하기."""
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf


def plot_numeric_columns(df):
    numeric_cols = df.select_dtypes(include='number').columns
    if numeric_cols.empty:
        print("⚠️ No numeric columns to plot.")
        return None
    df[numeric_cols].hist(bins=20, figsize=(15, 10), color='skyblue', edgecolor='black')
    plt.suptitle('Numeric Columns Distribution', fontsize=20)
    plt.tight_layout()
    return save_current_plot()


def plot_correlation_heatmap(df):
    numeric_cols = df.select_dtypes(include='number')
    if numeric_cols.empty:
        print("⚠️ No numeric columns for correlation heatmap.")
        return None
    corr = numeric_cols.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Heatmap', fontsize=18)
    return save_current_plot()


def plot_top_categories(df, column, top_n=10):
    if column not in df.columns:
        print(f"⚠️ Column '{column}' not found.")
        return None
    counts = df[column].value_counts().head(top_n)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=counts.values, y=counts.index, palette='muted')
    plt.title(f'Top {top_n} Categories in {column}', fontsize=18)
    plt.xlabel('Count')
    plt.ylabel(column)
    return save_current_plot()


def plot_pairplot(df, hue=None):
    numeric_cols = df.select_dtypes(include='number')
    if numeric_cols.empty:
        print("⚠️ No numeric columns for pairplot.")
        return None
    pair = sns.pairplot(df, hue=hue, palette='pastel')
    plt.suptitle('Pairplot of Numeric Columns', fontsize=20, y=1.02)
    return save_current_plot()


def plot_with_download(plot_func, **kwargs):
    """그래프 그리고, 다운로드 버튼 만들기."""
    output = widgets.Output()
    download_button = widgets.Button(
        description="Download Plot",
        icon='download',
        button_style='success',
        layout=widgets.Layout(width='150px')
    )

    img_data = None

    def on_button_click(b):
        if img_data is not None:
            with output:
                clear_output(wait=True)
                print("✅ Download ready!")
                display(widgets.Image(value=img_data.getvalue()))

    with output:
        clear_output(wait=True)
        img_data = plot_func(**kwargs)

    download_button.on_click(on_button_click)
    display(widgets.VBox([download_button, output]))


def plot_all_tabs(df, category_col=None, hue=None, top_n=10):
    """
    프로페셔널: 각 그래프별 다운로드 버튼 + 필터링 기능
    """

    tab_titles = ['Numeric Columns', 'Correlation Heatmap', 'Top Categories', 'Pairplot']
    tab_contents = []

    category_options = [None] + list(df[category_col].dropna().unique()) if category_col else [None]

    # 범주 필터 드롭다운
    category_filter = widgets.Dropdown(
        options=category_options,
        description='Filter:',
        value=None,
        layout=widgets.Layout(width='300px')
    )

    def filter_df(selected_value):
        if selected_value and category_col:
            return df[df[category_col] == selected_value]
        return df

    # 탭별로 그래프 그리기
    for tab_title in tab_titles:
        output = widgets.Output()

        with output:
            clear_output(wait=True)
            filtered_df = filter_df(category_filter.value)
            if tab_title == 'Numeric Columns':
                plot_with_download(plot_numeric_columns, df=filtered_df)
            elif tab_title == 'Correlation Heatmap':
                plot_with_download(plot_correlation_heatmap, df=filtered_df)
            elif tab_title == 'Top Categories':
                if category_col:
                    plot_with_download(plot_top_categories, df=filtered_df, column=category_col, top_n=top_n)
                else:
                    print("⚠️ No category column specified.")
            elif tab_title == 'Pairplot':
                plot_with_download(plot_pairplot, df=filtered_df, hue=hue)

        tab_contents.append(output)

    tabs = widgets.Tab(children=tab_contents)
    for i, title in enumerate(tab_titles):
        tabs.set_title(i, title)

    display(category_filter)
    display(tabs)

    print("\n✅ [Professional Visualization] All plots ready in Tabs with Download and Filters!")