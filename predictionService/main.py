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
PROJECT_ID = os.getenv("PROJECT_ID")
SUBSCRIPTION_ID = os.getenv("DATA_SUBSCRIPTION")
ML_TOPIC_ID = os.getenv("ML_TOPIC_ID")
subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
ml_topic_path = publisher.topic_path(PROJECT_ID, ML_TOPIC_ID)
app = FastAPI()

def callback(message: pubsub_v1.subscriber.message.Message):
    try:
        data=json.loads(message.data.decode("utf-8"))
        logger.info(f"data: {data}")
        res = predict_risk(data)
        output = {"region": data["region"], "timestamp": data["timestamp"], **res}
        publisher.publish(ml_topic_path, json.dumps(output).encode("utf-8"))
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
    return {"status": "RUNNING"}


