import os
import pickle

import click
import pandas as pd


@click.command("predict")
@click.option("--input-dir", required=True)
@click.option("--output-dir", required=True)
@click.option("--model-dir", required=True)
def predict(input_dir: str, output_dir: str, model_dir: str):

    with open(os.path.join(model_dir, "model.pkl"), "rb") as f:
        model = pickle.load(f)

    data = pd.read_csv(os.path.join(input_dir, "data.csv"), header=0)
    X = data.drop(['target'], axis=1)

    predicts = model.predict(X)

    predictions = pd.DataFrame(predicts, columns=["target"])
    os.makedirs(output_dir, exist_ok=True)
    predictions.to_csv(os.path.join(output_dir, "predictions.csv"), index=False)


if __name__ == '__main__':
    predict()
