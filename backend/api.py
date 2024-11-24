from fastapi import FastAPI, UploadFile, File
import pandas as pd
import joblib
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sklearn.preprocessing import StandardScaler
from fastapi import HTTPException

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.56.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Load all models and scaler
BASE_PATH = "/Users/paoloceccolini/Documents/GitHub/paolo-ml-demo/backend/"
linear_model = joblib.load(f"{BASE_PATH}linear_model.pkl")
knn_model = joblib.load(f"{BASE_PATH}knn_model.pkl")
rf_model = joblib.load(f"{BASE_PATH}rf_model.pkl")
scaler = joblib.load(f"{BASE_PATH}scaler.pkl")

class Features(BaseModel):
    house_age: int
    distance_to_tube_station: int
    number_of_local_stores: int
    model_type: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the House Price Prediction API"}

@app.get("/test")
def test():
    return {"message": "Test"}

@app.post("/predict")
def predict_house_price(input: Features):
    try:

        # Convert input features to DataFrame
        input_data = pd.DataFrame([[
            input.house_age,
            input.distance_to_tube_station,
            input.number_of_local_stores
        ]])

        print(input_data)
        
        # Scale the input data
        input_data_scaled = scaler.transform(input_data)
        
        # Select model based on input
        if input.model_type == "linear":
            model = linear_model
        elif input.model_type == "knn":
            model = knn_model
        elif input.model_type == "random_forest":
            model = rf_model
        else:
            raise ValueError("Invalid model type")
        
        # Make prediction
        predictions = model.predict(input_data_scaled)
        print(f"Made prediction: {predictions.tolist()}")  # Debug print
        return {"prediction": predictions.tolist()}
    
    except Exception as e:
        print(f"Error making prediction: {str(e)}")  # Debug print
        raise HTTPException(status_code=500, detail=str(e))
