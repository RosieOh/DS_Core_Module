from datetime import datetime

import matplotlib.pyplot as plt
import missingno as msno
import numpy as np
import pandas as pd
import seaborn as sns


class EDA:
    def __init__(self, df):
        self.df = df
    
    def summary(self):
        """기본적인 데이터프레임 요약"""
        return self.df.describe(include='all')
    
    def missing_values(self):
        """결측치 확인"""
        return self.df.isnull().sum()
    
    def data_types(self):
        """데이터 타입 확인"""
        return self.df.dtypes
    
    def correlation_matrix(self):
        """상관 행렬 출력 (수치형 열에 대해서만)"""
        numeric_df = self.df.select_dtypes(include=['float64', 'int64'])
        if numeric_df.empty:
            print("No numeric columns available for correlation.")
            return
        corr = numeric_df.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title('Correlation Matrix')
        plt.show()
    
    def plot_histograms(self, sample_size=None):
        """히스토그램 출력 (수치형 데이터만, 선택적 샘플링)"""
        df = self.df if sample_size is None else self.df.sample(n=sample_size, random_state=42)
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        if numeric_df.empty:
            print("No numeric columns available for histograms.")
            return
        numeric_df.hist(bins=30, figsize=(15, 10))
        plt.suptitle('Histograms for Numeric Features')
        plt.show()
    
    def boxplot(self, column):
        """박스플롯 출력 (이상치 확인용)"""
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
        plt.figure(figsize=(6, 4))
        sns.boxplot(x=self.df[column])
        plt.title(f'Boxplot for {column}')
        plt.show()
        
    def plot_categorical(self, column):
        """범주형 데이터 카운트 플롯"""
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
        plt.figure(figsize=(8, 6))
        sns.countplot(x=self.df[column])
        plt.title(f'Count Plot for {column}')
        plt.show()
        
    def missing_values_visual(self):
        """결측치 패턴 시각화"""
        if self.df.isnull().sum().sum() == 0:
            print("No missing values in the DataFrame.")
            return
        plt.figure(figsize=(10, 6))
        msno.matrix(self.df)
        plt.title('Missing Values Matrix')
        plt.show()
        
    def categorical_summary(self, top_n=5):
        """범주형 변수의 빈도 분석 (상위 N개 범주)"""
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns
        if categorical_cols.empty:
            print("No categorical columns available.")
            return
        
        for col in categorical_cols:
            print(f"\nFrequency counts for {col}:")
            print(self.df[col].value_counts().head(top_n))
            
            plt.figure(figsize=(8, 6))
            sns.countplot(x=self.df[col], order=self.df[col].value_counts().index[:top_n])
            plt.title(f'Top {top_n} Categories in {col}')
            plt.xticks(rotation=45)
            plt.show()
            
    def outlier_summary(self, threshold=1.5):
        """수치형 열의 이상치 요약 (IQR 기준)"""
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        if numeric_cols.empty:
            print("No numeric columns available.")
            return
        
        outliers_info = {}
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)][col]
            outliers_info[col] = {
                'outlier_count': len(outliers),
                'outlier_values': outliers.tolist()
            }
        
        for col, info in outliers_info.items():
            print(f"\nColumn: {col}")
            print(f"Number of outliers: {info['outlier_count']}")
            if info['outlier_count'] > 0:
                print(f"Outlier values: {info['outlier_values']}")
        
        return outliers_info
    
    def plot_kde(self):
        """수치형 열의 KDE 플롯"""
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        if numeric_cols.empty:
            print("No numeric columns available for KDE plot.")
            return
        
        for col in numeric_cols:
            plt.figure(figsize=(8, 6))
            sns.kdeplot(data=self.df, x=col, fill=True)
            plt.title(f'KDE Plot for {col}')
            plt.show()
            
    def pair_plot(self, hue=None):
        """수치형 변수 간 쌍 플롯 (선택적으로 범주형 hue 사용)"""
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_cols) < 2:
            print("At least two numeric columns are required for pair plot.")
            return
        
        plt.figure(figsize=(10, 10))
        sns.pairplot(self.df, vars=numeric_cols, hue=hue, diag_kind='kde')
        plt.suptitle('Pair Plot of Numeric Features', y=1.02)
        plt.show()
        
    def distribution_stats(self):
        """수치형 변수의 왜도와 첨도 계산"""
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        if numeric_cols.empty:
            print("No numeric columns available.")
            return
        
        stats = pd.DataFrame({
            'Skewness': self.df[numeric_cols].skew(),
            'Kurtosis': self.df[numeric_cols].kurtosis()
        })
        print("\nDistribution Statistics:")
        print(stats)
        return stats
    
    def plot_timeseries(self, time_col, value_col):
        """시계열 데이터 플롯"""
        if time_col not in self.df.columns or value_col not in self.df.columns:
            raise ValueError("Specified columns do not exist in the DataFrame.")
        
        plt.figure(figsize=(12, 6))
        plt.plot(self.df[time_col], self.df[value_col])
        plt.title(f'Time Series Plot: {value_col} over {time_col}')
        plt.xlabel(time_col)
        plt.ylabel(value_col)
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()
        
    def generate_report(self, output_file='eda_report.txt'):
        """EDA 요약 보고서 생성"""
        with open(output_file, 'w') as f:
            f.write("=== EDA Report ===\n\n")
            f.write("1. Data Summary:\n")
            f.write(str(self.summary()) + "\n\n")
            f.write("2. Missing Values:\n")
            f.write(str(self.missing_values()) + "\n\n")
            f.write("3. Data Types:\n")
            f.write(str(self.data_types()) + "\n\n")
            f.write("4. Distribution Statistics:\n")
            f.write(str(self.distribution_stats()) + "\n\n")
            f.write("5. Outlier Summary:\n")
            f.write(str(self.outlier_summary()) + "\n\n")
        
        print(f"Report generated: {output_file}")