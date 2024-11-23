from fastapi import FastAPI, UploadFile, File
import pandas as pd
import joblib
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.56.1:3000", "http://localhost:3000"],  # Allow all origins for development (adjust in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Load the pre-trained model
model = joblib.load("/Users/paoloceccolini/Documents/GitHub/paolo-ml-demo/backend/house_price_model.pkl")



class Features(BaseModel):
    number_of_rooms: int
    square_footage: int
    location_score: int

@app.get("/")
def read_root():
    return {"message": "Welcome to the House Price Prediction API"}

@app.post("/predict")
def predict_house_price(input: any):
    # Convert input features to DataFrame
    input_data = pd.DataFrame([input.features])
    predictions = model.predict(input_data)
    return {"prediction": predictions.tolist()}
