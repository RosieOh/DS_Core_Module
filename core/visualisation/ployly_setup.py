import pandas as pd
import plotly.express as px


def animated_plot(df, x_col, y_col, time_col):
    """Plotly 애니메이션 그래프"""
    # x_col과 y_col을 기준으로 그래프를 그리고 시간(time_col)을 애니메이션으로
    fig = px.scatter(df, x=x_col, y=y_col, animation_frame=time_col, 
                     animation_group='순위', # 예시로 '순위'로 그룹화
                     color='성별', # 성별로 색깔 구분
                     size_max=60, title=f'{y_col} vs {x_col} Over Time')
    
    fig.update_layout(
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(label='Play',
                         method='animate', args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)])]
        )]
    )

    fig.show()

def interactive_plot(df, category_col):
    """Plotly 인터랙티브 그래프"""
    fig = px.bar(df, x=category_col, y="순위", color="성별",
                 labels={category_col: 'Category', '순위': 'Ranking'},
                 title=f'{category_col} vs Ranking Interactive')
    
    # Interactive features: hover, click on legend to hide/show, zoom, etc.
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')), opacity=0.8)
    fig.update_layout(title=f'Interactive Plot of {category_col} vs Ranking')

    fig.show()

# # 사용 예시
# data = pd.read_csv('http://bit.ly/ld-sample-idol')

# # 애니메이션 예시
# animated_plot(data, x_col='나이', y_col='순위', time_col='연도')

# # 인터랙티브 예시
# interactive_plot(data, category_col='그룹')
