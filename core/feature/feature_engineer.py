import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


class FeatureEngineer:
    def __init__(self, df):
        self.df = df
    
    def encode_labels(self, column):
        """레이블 인코딩 (문자형 컬럼에 대해서만)"""
        le = LabelEncoder()
        self.df[column] = le.fit_transform(self.df[column])
        return self.df
    
    def one_hot_encode(self, column):
        """원-핫 인코딩"""
        ohe = OneHotEncoder(drop='first', sparse=False)
        encoded = ohe.fit_transform(self.df[[column]])
        encoded_df = pd.DataFrame(encoded, columns=ohe.get_feature_names_out([column]))
        self.df = pd.concat([self.df, encoded_df], axis=1).drop(column, axis=1)
        return self.df
