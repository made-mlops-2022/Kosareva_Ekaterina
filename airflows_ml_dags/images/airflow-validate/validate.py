import json
import os

import click
import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, roc_auc_score

@click.command("validate")
@click.option("--input-dir")
@click.option("--model-dir")
def validate(input_dir: str, model_dir: str):

    data = pd.read_csv(os.path.join(input_dir, "valid.csv"), header=0)
    y = data["target"]
    X = data.drop(["target"], axis=1)

    with open(os.path.join(model_dir, "model.pkl"), "rb") as f:
        model = pickle.load(f)

    y_pred = model.predict(X)

    metrics = {
        "accuracy_score": accuracy_score(y_pred, y),
        "roc_auc_score": roc_auc_score(y_pred, y)
    }

    with open(os.path.join(model_dir, "metrics.json"), "w") as f:
        json.dump(metrics, f)


if __name__ == "__main__":
    validate()

