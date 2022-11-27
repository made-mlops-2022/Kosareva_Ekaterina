import json
import logging
import click
import numpy as np
import pandas as pd
import requests


@click.command()
@click.option("--host", default="localhost")
@click.option("--port", default=8000)
@click.option("--data_path", default="./data/data.csv")
def predict(host, port, data_path):
    data = pd.read_csv(data_path)
    if 'condition' in data.columns.values:
        data.drop(['condition'], axis=1, inplace=True)
    features = data.columns.tolist()

    for i in range(data.shape[0]):
        request_data = [
            x.item() if isinstance(x, np.generic) else x for x in data.iloc[i].tolist()
        ]
        logging.info(f"Request_data: {request_data}")
        response = requests.post(
            f"http://{host}:{port}/predict/",
            data=json.dumps({"data": [request_data], "features": features}),
        )
        logging.info(f"Response status code: {response.status_code}, body json: {response.json()}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    predict()