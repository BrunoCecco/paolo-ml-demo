import React, { useState } from "react";
import axios from "axios";

function App() {
  const [formData, setFormData] = useState({
    number_of_rooms: "",
    square_footage: "",
    location_score: "",
  });
  const [prediction, setPrediction] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:8000/predict", {
        Headers: {
          "Content-Type": "application/json",
          "Origin": "http://localhost:3000",
          "Access-Control-Request-Method": "POST"
        },
        features: formData,
      });
      setPrediction(response.data.prediction[0]);
    } catch (error) {
      console.error("Error making prediction:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>House Price Prediction</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Number of Rooms:</label>
          <input
            type="number"
            name="number_of_rooms"
            value={formData.number_of_rooms}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Square Footage:</label>
          <input
            type="number"
            name="square_footage"
            value={formData.square_footage}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Location Score:</label>
          <input
            type="number"
            name="location_score"
            value={formData.location_score}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Predict</button>
      </form>
      {prediction && <h2>Predicted Price: ${prediction.toFixed(2)}</h2>}
    </div>
  );
}

export default App;
