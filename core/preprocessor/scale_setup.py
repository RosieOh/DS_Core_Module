import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


class DataPreprocessor:
    def __init__(self, df):
        self.df = df
    
    def clean_column_names(self):
        """컬럼명을 소문자화하고 공백을 언더스코어로 바꿈"""
        self.df.columns = self.df.columns.str.lower().str.replace(' ', '_')
    
    def handle_missing_values(self, strategy='mean'):
        """결측치 처리: 숫자형 데이터는 'mean' 또는 'median', 문자형 데이터는 'most_frequent' 처리"""
        # 숫자형 데이터만 mean/median 처리
        num_cols = self.df.select_dtypes(include='number').columns
        cat_cols = self.df.select_dtypes(exclude='number').columns
        
        # 숫자형 컬럼에 대해 결측치 처리
        num_imputer = SimpleImputer(strategy=strategy)
        self.df[num_cols] = num_imputer.fit_transform(self.df[num_cols])
        
        # 문자형 컬럼에 대해 결측치 처리
        cat_imputer = SimpleImputer(strategy='most_frequent')
        self.df[cat_cols] = cat_imputer.fit_transform(self.df[cat_cols])
    
    def remove_outliers(self, col):
        """이상치 제거: IQR 방식을 이용"""
        Q1 = self.df[col].quantile(0.25)
        Q3 = self.df[col].quantile(0.75)
        IQR = Q3 - Q1
        self.df = self.df[(self.df[col] >= (Q1 - 1.5 * IQR)) & (self.df[col] <= (Q3 + 1.5 * IQR))]
    
    def scale_data(self, scaler_type='standard'):
        """데이터 스케일링: 'standard' 또는 'minmax'"""
        if scaler_type == 'standard':
            scaler = StandardScaler()
        else:
            raise ValueError("Invalid scaler type. Choose 'standard'.")
        
        self.df[self.df.select_dtypes(include='number').columns] = scaler.fit_transform(self.df.select_dtypes(include='number'))
    
    def drop_columns(self, columns):
        """불필요한 컬럼 제거 (컬럼이 있을 때만 제거)"""
        # 존재하는 컬럼만 제거하도록 체크
        self.df = self.df.drop([col for col in columns if col in self.df.columns], axis=1)
    
    def preprocess(self, missing_strategy='mean', remove_outliers_cols=None, scale_type='standard', drop_columns=None):
        """전처리 전체 파이프라인"""
        self.clean_column_names()
        self.handle_missing_values(strategy=missing_strategy)
        
        if remove_outliers_cols:
            for col in remove_outliers_cols:
                self.remove_outliers(col)
        
        if scale_type:
            self.scale_data(scaler_type=scale_type)
        
        if drop_columns:
            self.drop_columns(drop_columns)

        return self.df