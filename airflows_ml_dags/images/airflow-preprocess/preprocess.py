import os

import click
import pandas as pd


@click.command("preprocess")
@click.option("--input-dir")
@click.option("--output-dir")
def preprocess(input_dir: str, output_dir: str):

    data = pd.read_csv(os.path.join(input_dir, "data.csv"), header=0)
    for col in data.columns.values:
        if col != 'target':
            data[col] = (data[col] - data[col].mean()) / data[col].std()

    data_train = data.sample(frac=0.75)
    data_test = data.drop(data_train.index)
    os.makedirs(output_dir, exist_ok=True)
    data_train.to_csv(os.path.join(output_dir, "train.csv"), index=False)
    data_test.to_csv(os.path.join(output_dir, "valid.csv"), index=False)

if __name__ == '__main__':
    preprocess()
