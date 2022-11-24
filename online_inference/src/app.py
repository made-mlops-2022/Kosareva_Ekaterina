import logging
import os

from typing import List, Optional
import uvicorn
from fastapi import FastAPI, HTTPException
import utils
from utils import DataResponseModel, DataRequestModel, prepare_data, new_prediction
from sklearn.ensemble import RandomForestClassifier

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.path.pardir
    )
)  # .../api

MODEL_PATH = os.path.join(BASE_DIR, '../model/rfc_model.sav')

model:Optional[RandomForestClassifier] = None

# Initialize an instance of FastAPI
app = FastAPI()

#Load model while startup
@app.on_event("startup")
def load_model():
    '''Load pre-trained classifier'''
    global model
    try:
        clf = utils.load_model(MODEL_PATH)
    except FileNotFoundError as err:
        logging.error(err)
        return
    model = clf
    return {"message": "Model has loaded"}


# Define the default route
@app.get("/")
def root():
    """Root message"""
    return {"message": "Welcome to Heart Disease Cleavlend Classification FastAPI"}


# Define the "helth" endpoint
@app.post("/helth")
def check_model():
    """"Check if model loaded"""
    if (not (model)):
        raise HTTPException(status_code=200,
                            detail="Model didn't load")
        return
    else:
        return {"message": "Model sucsessfuly loaded"}


@app.post("/predict/", response_model=List[DataResponseModel])
def predict_class(request: DataRequestModel) -> List[DataResponseModel]:
    if not check_model():
        logging.errr("Model didn't load")
        raise HTTPException(
            status_code=500,
            detail="You MAST load model to make predictions"
        )
    data = prepare_data(request)
    prediction = new_prediction(data=data, classifier=model)

    return [DataResponseModel(predicted_class=pred_class) for pred_class in prediction]



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    uvicorn.run("app:app", host="0.0.0.0", port=os.getenv("PORT", 8000))
