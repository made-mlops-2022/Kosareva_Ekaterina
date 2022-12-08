import pickle
from typing import List, Union
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from fastapi import HTTPException
from pydantic import BaseModel, conlist


FEATURES = [
     "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal"
]

class DataRequestModel(BaseModel):
    data:List[conlist(Union[float, str, None], min_items=10, max_items=400)]
    features:List[str]


class DataResponseModel(BaseModel):
    predicted_class:int


def prepare_data(request:DataRequestModel):
    data = pd.DataFrame(request.data, columns=request.features)

    if "condition" in request.features:
        data.drop(['condition'], axis=1, inplace=True)
    print(data.columns.values)
    if (data.columns.values != FEATURES).any():
        raise HTTPException(
            status_code=400,
            detail=f"The list of features not correspond to : {FEATURES}"
        )

    return data

def load_model(model_path:str) -> object:
    """Load model"""
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model



def new_prediction(
        data: pd.DataFrame,
        classifier: RandomForestClassifier
) -> float:
    """make a prediction"""

    prediction = classifier.predict(data)
    return prediction
