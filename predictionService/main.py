import os
import json
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from google.cloud import pubsub_v1
from predict import predict_risk
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
credentials_path="/home/govind/Ember-link/bright-raceway-468304-e1-d7622ad6eb37.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credentials_path

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()
subscription_path = os.getenv("SUBSCRIPTION_PATH")
ml_topic_path = os.getenv("ML_TOPIC")
app = FastAPI()

def callback(message: pubsub_v1.subscriber.message.Message):
    try:
        data=json.loads(message.data.decode("utf-8"))
        logger.info(f"data: {data}")
        res = predict_risk(data)
        output = {"region": data["region"], "timestamp": data["timestamp"], "latitude": data["Latitude"], "longitude": data["Longitude"], **res}
        fut=publisher.publish(ml_topic_path, json.dumps(output).encode("utf-8"))
        logger.info(f"PUBLISHED: {fut.result()}")
        logger.info(f"ML result: {output}")
        message.ack()
    except Exception as e:
        logger.error(f"error: {e}")
        message.nack()

@app.on_event("startup")
def start_sub():
    flow_control = pubsub_v1.types.FlowControl(max_messages=10)
    subscriber.subscribe(
        subscription_path,
        callback=callback,
        flow_control=flow_control
    )
    logger.info("ML service on hai ji...")

@app.get("/health")
def chek():
    return {"status": ""}


