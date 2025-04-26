from sklearn.model_selection import cross_val_score


class ModelTrainer:
    def __init__(self, model, X_train, y_train):
        self.model = model
        self.X_train = X_train
        self.y_train = y_train
    
    def train(self):
        """모델 학습"""
        self.model.fit(self.X_train, self.y_train)
    
    def cross_validate(self, cv=5):
        """교차 검증 (KFold)"""
        scores = cross_val_score(self.model, self.X_train, self.y_train, cv=cv)
        print(f'Cross-Validation Scores: {scores}')
        print(f'Mean Score: {scores.mean():.4f}')
