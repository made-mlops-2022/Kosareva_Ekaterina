import os
import pickle

import click
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


@click.command("airflow-train")
@click.option("--input-dir")
@click.option("--model-dir")
def train(input_dir: str, model_dir: str):

    data = pd.read_csv(os.path.join(input_dir, "train.csv"), header=0)

    y = data['target']
    X = data.drop(['target'], axis=1)

    model = RandomForestClassifier()
    model.fit(X, y)

    os.makedirs(model_dir, exist_ok=True)
    with open(os.path.join(model_dir, "model.pkl"), 'wb') as f:
        pickle.dump(model, f)


if __name__ == '__main__':
    train()
