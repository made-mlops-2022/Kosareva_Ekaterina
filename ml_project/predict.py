"""Model training script for heart disease cleavlend classification"""

import click
import pandas as pd
import pickle
import logging

def read_data(test_data):
    '''read dataset'''
    dataset = pd.read_csv(test_data, header=0, index_col=0)

    return dataset

def load_model(model_path):
    '''load model'''

    model = pickle.load(open(model_path, 'rb'))
    return model

def predict_class(X, model):
    '''make class prediction'''
    return  model.predict(X)

def save_predictions(X, y_pred, save_results):
    '''save predictions to file'''

    X['predictions'] = y_pred
    X.to_csv(save_results)


@click.command()
@click.option("--test-data", type=str, default="data/data_test.csv")
@click.option("--model-path", type=str, default="models/rfc_model.sav")
@click.option("--save-results", type=str, default="models/predictions.csv")
def main(
    test_data,
    model_path,
    save_results
):
    logging.basicConfig(level=logging.DEBUG, filename="logs/test_log.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")

    logging.debug("Load test data...")

    X = read_data(test_data)
    logging.info(f'The number of testing samples = {X.shape[0]}')
    logging.info("Test data loaded")

    logging.debug("Load model...")
    model = load_model(model_path)
    logging.info("Model successfully loaded...")

    logging.debug("Prediction is started...")
    y_pred = predict_class(X, model)

    save_predictions(X, y_pred, save_results)
    logging.info(f'Results saved to {save_results}')

if __name__ == '__main__':
    main()