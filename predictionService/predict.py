import joblib
import pandas as pd
model = joblib.load("flood_model.pkl")
def predict_risk(data_dict):
    df = pd.DataFrame([data_dict])
    prob = model.predict_proba(df)[0][1]
    if prob > 0.60:
        level = "HIGH"
    elif prob > 0.4:
        level = "MEDIUM"
    else:
        level = "LOW"
    return {
        "risk_score": float(prob),
        "risk_level": level
    }


# data={
#     "Rainfall (mm)": 200,
#     "Temperature (°C)": 16,
#     "Humidity (%)": 95,
#     "River Discharge (m³/s)": 800,
#     "Water Level (m)": 20,
#     "Elevation (m)": 300,
#     "Population Density": 500,
#     "Latitude": 30.4034,
#     "Longitude": 79.3228,
#     "Land Cover": "Urban",
#     "Soil Type": "Silt",
#     "Infrastructure": 0,
#     "Historical Floods": 1
# }
# print(predict_risk(data))
