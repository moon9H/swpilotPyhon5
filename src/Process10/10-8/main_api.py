# 과정 10 - (문제8) 집으로 가는 길
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()
model = joblib.load('iris_model.pkl')

class IrisInput(BaseModel):
    features: list[float]

@app.post('/predict')
def predict_iris(data: IrisInput):
    x_input = np.array(data.features).reshape(1, -1)
    prediction = model.predict(x_input)
    return {'prediction': int(prediction[0])}