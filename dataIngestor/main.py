import time
import json
import requests
from datetime import datetime
from google.cloud import pubsub_v1
import os
from dotenv import load_dotenv
import logging
from utils.fetch_weath import fetch_weather
from utils.fetch_sat import fetch_satellite
from utils.signals import compute_signals
from utils.hydrology import estimate_hydro
from utils.geo_mapping import get_geo_features
from utils.fetch_elev import fetch_elevation
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()
import random 
import asyncio
from fastapi import FastAPI
app = FastAPI()

PROJECT_ID=os.getenv("PROJECT_ID")
TOPIC_ID=os.getenv("TOPIC_ID")
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
PUBLISH_INTERVAL = 900
REGIONS = [
    {"name": "dehradun", "lat": 30.3165, "lon": 78.0322},
    {"name": "rishikesh", "lat": 30.0869, "lon": 78.2676},
    {"name": "haridwar", "lat": 29.9457, "lon": 78.1642},
    {"name": "rudraprayag", "lat": 30.2844, "lon": 78.9811},
    {"name": "chamoli", "lat": 30.4034, "lon": 79.3228},
    {"name": "devprayag", "lat": 30.1460, "lon": 78.5994}
]
def publish(data):
    payload = json.dumps(data).encode("utf-8")
    publisher.publish(topic_path, payload)
    print("Published:", data)

def generate_mock_data(region):
    rainfall = random.randint(0, 60)
    return {
        "region": region["name"],
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": random.randint(5, 25),
        "rainfall": rainfall,
        "wind": random.randint(0, 20),
        "satellite_rainfall": rainfall + random.randint(0, 10),
        "combined_rainfall": rainfall + random.randint(5, 15),
        "extreme_rain_alert": rainfall > 25,
        "flood_risk": rainfall > 40,
    }

@app.get("/health")
def healthchek():
    return {"status": "RUNNING"}

async def ingest_loop():
    logger.info("Ingestor on hai ji...")
    while True:
        for region in REGIONS:
            try:
                if USE_MOCK:
                    data = generate_mock_data(region)
                else:
                    weather = fetch_weather(region["lat"], region["lon"])
                    sat = fetch_satellite(region["lat"], region["lon"])
                    elev = fetch_elevation(region["lat"], region["lon"])
                    geo = get_geo_features(region["name"])
                    hydro = estimate_hydro(weather["rainfall"], elev)
                    signals = compute_signals(weather, sat)
                    data = {
                        "region": region["name"],
                        "timestamp": datetime.utcnow().isoformat(),
                        "Rainfall (mm)": weather["rainfall"],
                        "Temperature (°C)": weather["temperature"],
                        "Humidity (%)": weather["humidity"],
                        "Satellite_Rainfall": sat["satellite_rainfall"],
                        "River Discharge (m³/s)": hydro["river_discharge"],
                        "Water Level (m)": hydro["water_level"],
                        "Elevation (m)": elev,
                        "Land Cover": geo["land_cover"],
                        "Soil Type": geo["soil_type"],
                        "Population_Density": 300,
                        "Infrastructure": 0,
                        "Historical Floods": 1,
                        "Latitude": region["lat"],
                        "Longitude": region["lon"]
                    }
                publish(data)
            except Exception as e:
                logger.error(f"Error in region {region['name']}: {e}")
        await asyncio.sleep(PUBLISH_INTERVAL)


@app.on_event("startup")
async def start_ingestor():
    asyncio.create_task(ingest_loop())


@app.get("/trigger")
def trigger_once():
    logger.info("Manual trigger called")
    for region in REGIONS:
        data = generate_mock_data(region) if USE_MOCK else {
            "region": region["name"],
            "timestamp": datetime.utcnow().isoformat(),
        }
        publish(data)
    return {"status": "triggered"}

