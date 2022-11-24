import os
import pandas as pd
import pytest
import json
from fastapi.testclient import TestClient
from online_inference.src.app import app


@pytest.fixture()
def data_path() -> str:
    return "data/data.csv"


@pytest.fixture()
def model_path() -> str:
    os.environ['PATH_TO_MODEL'] = 'model/rfc_model.sav'
    return os.getenv("PATH_TO_MODEL")


def test_root_page():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to Heart Disease Cleavlend Classification FastAPI"}


def test_get_predict(data_path, model_path):
    with TestClient(app) as client:
        data = pd.read_csv(data_path).drop('condition', axis=1)
        features = data.columns.tolist()
        data = data.values.tolist()[:3]
        response = client.post("/predict/", data=json.dumps({"data":data, "features":features}))
        assert response.status_code == 200
        assert response.json()[0]["predicted_class"] == 0

def test_invalid_features(model_path):
    with TestClient(app) as client:
        fake_data = pd.DataFrame(data={'id': [1, 2], 'feature': [0.3, 1.5]})
        features = fake_data.columns.tolist()
        fake_data = fake_data.values.tolist()
        response = client.post("/predict/", data=json.dumps({"data":fake_data, "features":features}))
        assert response.status_code != 200
