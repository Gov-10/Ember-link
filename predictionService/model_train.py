import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
df = pd.read_csv("flood_risk.csv")
numerical_features = [
    "Rainfall (mm)",
    "Temperature (°C)",
    "Humidity (%)",
    "River Discharge (m³/s)",
    "Water Level (m)",
    "Elevation (m)",
    "Population Density",
    "Latitude",
    "Longitude"
]

categorical_features = [
    "Land Cover",
    "Soil Type"
]

binary_features = [
    "Infrastructure",
    "Historical Floods"
]

features = numerical_features + categorical_features + binary_features

X = df[features]
y = df["Flood Occurred"]
X[numerical_features] = X[numerical_features].fillna(X[numerical_features].mean())
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ],
    remainder="passthrough" 
    )
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    random_state=42,
    n_jobs=-1
)
pipeline = Pipeline([
    ("preprocessing", preprocessor),
    ("model", model)
])
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))
joblib.dump(pipeline, "flood_model.pkl")

