
import redis
import json, os
from dotenv import load_dotenv
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from google.cloud import pubsub_v1
import logging
from fastapi import FastAPI
app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
load_dotenv()
credential_path="/home/govind/Ember-link/bright-raceway-468304-e1-d7622ad6eb37.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credential_path
subscriber=pubsub_v1.SubscriberClient()
subscription_path=os.getenv("FINAL_SUB")

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)
def publish_update(region, data):
    redis_client.set(
        f"flood:latest:{region}",
        json.dumps(data),
        ex=300
    )
    redis_client.publish(
        f"flood:{region}",
        json.dumps(data)
    )

def callback(message):
    try:
        # 1. Data decode karo
        raw_data = message.data.decode("utf-8")
        data = json.loads(raw_data)
        logger.info(f"Data aagya: {data}")
        
        region = data.get("region")

        # 2. Key names ko page.tsx ke hisaab se map karo
        # IMPORTANT: Frontend risk_level dhoond raha hai, toh wahi key name rakho
        dt = {
            "region": region,
            "message": data.get("message"), # Ye public message hai
            "route": data.get("route"),
            "risk_level": data.get("risk_level") or data.get("res") or "HIGH", # Dono handle ho gaye
            "status": data.get("status"),
            "target_shelter": data.get("target_shelter") or "TBD",
            "distance_m": data.get("distance_m") or 0,
            "instructions": data.get("instructions") or "No specific instructions yet",
            # Agar NGO data (aim) bhej rahe ho toh ye line bhi zaroori hai:
            "ngo_data": data.get("ngo_data", []) 
        }

        # 3. Redis update
        publish_update(region, dt)
        logger.info(f"✅ PUSHED TO DJANGO: {region}")
        message.ack()

    except Exception as e:
        logger.error(f"❌ Worker Error: {str(e)}")
        message.nack()


@app.get("/health")
def chek():
    return {"status": "running"}

@app.on_event("startup")
def sta():
    flow_control=pubsub_v1.types.FlowControl(max_messages=10)
    subscriber.subscribe(subscription_path, callback=callback, flow_control=flow_control)
    logger.info("worker is on...")
