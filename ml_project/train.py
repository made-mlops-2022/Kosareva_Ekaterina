"""Model training script for heart disease cleavlend classification"""

import click
from configparser import ConfigParser
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import logging


def read_data(train_data, target):
    dataset = pd.read_csv(train_data, header=0, index_col=0)
    y = dataset[target]
    X = dataset.drop([target], axis=1)
    return X, y

def model_fit(X, y, max_depth, n_estimators, random_state):
    model = RandomForestClassifier(
        max_depth=max_depth,
        n_estimators=n_estimators,
        random_state=random_state
    )
    model.fit(X, y)  # fit model
    return model

def save_model(model, save_path):
    pickle.dump(model, open(save_path, 'wb'))  # save model


DEFAULT_CFG = "/config/config2.yaml"

def configure(ctx, params, filename):
    cfg = ConfigParser()
    cfg.read(filename)

    try:
        options = dict(cfg['options'])
    except KeyError:
        options = {}
    ctx.default_map = options

@click.command()
@click.option(
    '-c', '--config',
    type         = click.Path(dir_okay=False),
    default      = DEFAULT_CFG,
    callback     = configure,
    is_eager     = True,
    expose_value = False,
    help         = 'Read option defaults from the specified INI file',
    show_default = True,
)
@click.option("--train-data", type=str, default='data/data_train.csv')
@click.option("--n-estimators", type=int, default=100)
@click.option("--max-depth", type=int, default=4)
@click.option("--random-state", type=int, default=0)
@click.option("--target", type=str, default='condition')
@click.option("--save-path", type=str, default='models/rfc_model.sav')
def main(
    train_data,
    n_estimators,
    max_depth,
    random_state,
    target,
    save_path
):
    logging.basicConfig(level=logging.DEBUG, filename="logs/train_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")

    logging.debug("Training is starting...")

    X, y = read_data(train_data, target)
    logging.info("Data loaded...")
    logging.info(f'The number of training samples = {X.shape[0]}')

    logging.info("Model initialization ...")

    print(
        f'Model RandomForest params: data = {train_data}, n_estimators = {n_estimators}, max_depth = {max_depth}, random_state = {random_state}')

    logging.debug("Model training is started....")
    logging.info(f'Model RandomForest params: data = {train_data}, n_estimators = {n_estimators}, max_depth = {max_depth}, random_state = {random_state}')
    model = model_fit(X, y, max_depth, n_estimators, random_state) # fit model

    logging.debug(f"Model trained successfuly with accuracy {model.score(X, y)}")

    save_model(model, save_path)
    logging.info("Model was saved")


if __name__ == '__main__':
    main()