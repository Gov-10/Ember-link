import requests
import os
import json
def fetch_satellite(lat, lon):
    url = (
        "https://power.larc.nasa.gov/api/temporal/point"
        f"?parameters=PRECTOT"
        f"&latitude={lat}&longitude={lon}"
        "&format=JSON&community=AG"
    )
    try:
        res = requests.get(url)
        data = res.json()
        values = data["properties"]["parameter"]["PRECTOT"]
        latest = list(values.values())[-1]
        return {"satellite_rainfall": latest}
    except:
        return {"satellite_rainfall": 0}
