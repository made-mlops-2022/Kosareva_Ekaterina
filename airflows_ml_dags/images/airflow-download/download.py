import os
import pandas as pd
import numpy as np

import click
from sklearn.datasets import make_classification


@click.command("download")
@click.option("--output-dir", required=True)
def download(output_dir: str):
    X, y = make_classification(n_samples=100, n_features=4, n_informative=3,
                                 n_redundant=1, n_classes=2)

    os.makedirs(output_dir, exist_ok=True)
    df = pd.DataFrame(np.c_[X, y], columns=['0', '1', '2', '3', 'target'])
    df.to_csv(os.path.join(output_dir, "data.csv"), index=False)


if __name__ == '__main__':
    download()

