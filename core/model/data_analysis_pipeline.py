from data_preprocessor import DataPreprocessor
from eda import EDA
from model_trainer import ModelTrainer


class DataAnalysisPipeline:
    def __init__(self, df):
        self.df = df
        self.eda = EDA(df)
        self.preprocessor = DataPreprocessor(df)
    
    def run_pipeline(self, missing_strategy='mean', scale_type='standard', drop_columns=None, remove_outliers_cols=None):
        # EDA
        print(self.eda.summary())
        
        # 데이터 전처리
        self.df = self.preprocessor.preprocess(
            missing_strategy=missing_strategy, 
            scale_type=scale_type, 
            drop_columns=drop_columns, 
            remove_outliers_cols=remove_outliers_cols
        )
        
        # 추가 작업 (모델링 등)
        # 모델 학습, 평가 등의 작업을 진행
        
        return self.df
