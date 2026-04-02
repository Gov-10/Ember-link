import joblib
import pandas as pd
model = joblib.load("flood_model.pkl")
def predict_risk(data_dict):
    df = pd.DataFrame([data_dict])
    prob = model.predict_proba(df)[0][1]
    if prob > 0.75:
        level = "HIGH"
    elif prob > 0.4:
        level = "MEDIUM"
    else:
        level = "LOW"
    return {
        "risk_score": float(prob),
        "risk_level": level
    }
