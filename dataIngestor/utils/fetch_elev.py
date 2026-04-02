import requests
import json
def fetch_elevation(lat, lon):
    try:
        url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
        res= requests.get(url).json()
        return res["results"][0]["elevation"]
    except:
        return 500
