from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.ensemble import RandomForestClassifier
from train import read_data
import pandas as pd

class CustomTransformer(BaseEstimator, TransformerMixin):

    def __init__(self):
        print("CustomTransformer:")

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        print("Drop columns: 'age', 'chol', 'oldpeak', 'cp_0', 'cp_3', 'ca_0', 'ca_2', 'slope_1'")
        X_cut = X[['age', 'chol', 'oldpeak', 'cp_0', 'cp_3', 'ca_0', 'ca_2', 'slope_1']]
        print(f"New data shape = {X_cut.shape}")
        return X_cut

def main():
    TRAIN_DATA_PATH = 'data/data_train.csv'
    TEST_DATA_PATH = 'data/data_test.csv'
    TARGET_NAME = 'condition'
    X_train, y_train = read_data(TRAIN_DATA_PATH, TARGET_NAME)
    X_test = pd.read_csv(TEST_DATA_PATH, header=0, index_col=0)

    pipe = make_pipeline(CustomTransformer(), RandomForestClassifier(n_estimators=50, max_depth=7, random_state=0))
    pipe.fit(X_train, y_train)

    print("Make prediction on test data")
    preds = pipe.predict(X_test)
    print(f"Number of predictions {len(preds)}")


if __name__ == '__main__':
    main()