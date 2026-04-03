#TODO: pubsub subscriber code add karna-> pending
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
PROJECT_ID=os.getenv("PROJECT_ID")
HISTORY_SUBSCRIPTION=os.getenv("HISTORY_SUBSCRIPTION")
subscriber=pubsub_v1.SubscriberClient()
subscription_path=subscriber.subscription_path(PROJECT_ID, HISTORY_SUBSCRIPTION)
load_dotenv()

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
    async_to_sync(channel_layer.group_send)(
        f"flood_{region}",
        {
            "type": "send_update",
            "data": data
        }
    )

def callback(message):
    try:
        data=json.loads(message.data.decode("utf-8"))
        region = data.get("region")
        msg=data.get("message")
        route=data.get("route")
        risk=data.get("risk_level")
        status=data.get("status")
        target_shelter=data.get("target_shelter")
        dt = {"region":region,"message":msg,"route":route,"risk":risk,"status":status,"target_shelter":target_shelter}
        publish_update(region, dt)
        message.ack()
    except Exception as e:
        logger.error(str(e))
        message.nack()


@app.get("/health")
def chek():
    return {"status": "running"}

@app.on_event("startup")
def sta():
    flow_control=pubsub_v1.types.FlowControl(max_messages=10)
    subscriber.subscribe(subscription_path, callback=callback, flow_control=flow_control)
    logger.info("worker is on...")
