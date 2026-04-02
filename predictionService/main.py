import os
from dotenv import load_dotenv
from predict import predict_risk
from google.cloud import pubsub_v1
import logging
load_dotenv()
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
PROJECT_ID=os.getenv("PROJECT_ID")
SUBSCRIPTION_ID=os.getenv("TOPIC_ID")
subscriber=pubsub_v1.SubscriberClient()
subscribe_path=subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

def subsc(message: pubsub_v1.subscriber.message.Message):
    message.ack()
    return message.data.decode("utf-8")

flow_control = pubsub_v1.types.FlowControl(max_messages=10)
streaming_pull_future = subscriber.subscribe(
    subscribe_path, callback=callback, flow_control=flow_control
)
#TODO: Complete remaining code
app = FastAPI()
@app.get("/health")
def healthchek():
    return {"status": "RUNNING"}
