import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import numpy as np

# Load data
def load_data(filepath):
    # Load the data from realestate.csv
    data = np.loadtxt(filepath,delimiter=',')
    # Assuming the last column is the target variable
    X = data[:, :-1]  # Features
    y = data[:, -1]   # Target variable

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Add scaling here
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)


    print("Data loaded and split into training and test sets.")

    return X_train, y_train, X_train_scaled, X_test_scaled, y_train, y_test

# Train model
def train_model(X_train, y_train, X_test, y_test):
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    joblib.dump(model, "house_price_model.pkl")
    
    mse = mean_squared_error(y_test, predictions)
    return model, mse

X_train, y_train, X_train_scaled, X_test_scaled, y_train, y_test = load_data('realestate.csv')
model, mse = train_model(X_train_scaled, y_train, X_test_scaled, y_test)