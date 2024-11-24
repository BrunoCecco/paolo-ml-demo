import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import numpy as np

# Add BASE_PATH at the top
BASE_PATH = "/Users/paoloceccolini/Documents/GitHub/paolo-ml-demo/backend/"

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

    # Save the scaler with full path
    joblib.dump(scaler, f"{BASE_PATH}scaler.pkl")
    print(f"Saved scaler to {BASE_PATH}scaler.pkl")

    print("Data loaded and split into training and test sets.")
    return X_train, y_train, X_train_scaled, X_test_scaled, y_train, y_test

def train_models(X_train_scaled, y_train, X_test_scaled, y_test):
    models = {
        'linear': LinearRegression(),
        'knn': KNeighborsRegressor(n_neighbors=5),
        'random_forest': RandomForestRegressor(n_estimators=100, random_state=42)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name} model...")
        # Train the model
        model.fit(X_train_scaled, y_train)
        
        # Make predictions
        predictions = model.predict(X_test_scaled)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        
        # Save the model with full path
        model_path = f"{BASE_PATH}{name}_model.pkl"
        joblib.dump(model, model_path)
        print(f"Saved {name} model to {model_path}")
        
        # Store results
        results[name] = {
            'model': model,
            'mse': mse,
            'r2': r2
        }
        
        print(f"{name.capitalize()} Model Performance:")
        print(f"MSE: {mse:.4f}")
        print(f"R2 Score: {r2:.4f}")
    
    return results

if __name__ == "__main__":
    # Load and preprocess data
    X_train, y_train, X_train_scaled, X_test_scaled, y_train, y_test = load_data('realestate.csv')
    
    # Train all models
    results = train_models(X_train_scaled, y_train, X_test_scaled, y_test)
    
    print("\nAll models trained and saved successfully!")