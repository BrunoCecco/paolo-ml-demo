import React, { useState } from "react";
import axios from "axios";
import "./App.css"

function App() {
  const [formData, setFormData] = useState({
    house_age: "5",
    distance_to_tube_station: "500",
    number_of_local_stores: "3",
    model_type: "linear"
  });
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate that all fields have values
    if (!formData.house_age || !formData.distance_to_tube_station || !formData.number_of_local_stores) {
      setError("Please fill in all fields");
      return;
    }

    try {
      const payload = {
        house_age: parseInt(formData.house_age),
        distance_to_tube_station: parseInt(formData.distance_to_tube_station),
        number_of_local_stores: parseInt(formData.number_of_local_stores),
        model_type: formData.model_type
      };
      
      console.log("Sending payload:", payload);  // Debug print
      
      const response = await axios.post("http://localhost:8000/predict", payload);
      console.log("Received response:", response.data);  // Debug print
      
      setPrediction(response.data.prediction[0]);
      // setPrediction(response.data.prediction[0]);
    } catch (error) {
      console.error("Error making prediction:", error);
      console.error("Error response:", error.response?.data);  // Debug print
      setError("Error making prediction. Please check your inputs and the console for details.");
    }
  };

  return (
    <div className="App">
      <div className="form-container">
        <h1>
          House Price Predictor
        </h1>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="house_age">House Age (years)</label>
            <input
              type="number"
              id="house_age"
              name="house_age"
              value={formData.house_age}
              onChange={handleChange}
            />
          </div>
          
          <div className="input-group">
            <label htmlFor="distance_to_tube_station">Distance to Tube Station (meters)</label>
            <input
              type="number"
              id="distance_to_tube_station"
              name="distance_to_tube_station"
              value={formData.distance_to_tube_station}
              onChange={handleChange}
            />
          </div>
          
          <div className="input-group">
            <label htmlFor="number_of_local_stores">Number of Local Stores</label>
            <input
              type="number"
              id="number_of_local_stores"
              name="number_of_local_stores"
              value={formData.number_of_local_stores}
              onChange={handleChange}
            />
          </div>
          
          <div className="input-group">
            <label htmlFor="model_type">Model Type</label>
            <select
              id="model_type"
              name="model_type"
              value={formData.model_type}
              onChange={handleChange}
            >
              <option value="random_forest">Random Forest</option>
              <option value="linear">Linear Regression</option>
              <option value="knn">K-Nearest-Neighbours</option>              
            </select>
          </div>

          <button type="submit">Predict Price</button>
        </form>

        {error && <div className="error-message">{error}</div>}
        
        {prediction && (
          <div className="prediction-result">
            <span>Predicted Price per m²: </span> <b> £{prediction.toFixed(2)}</b>
            {/* <p>Using model: {formData.model_type}</p> */}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
