#TODO: pubsub subscriber code add karna-> pending
import redis
import json, os
from dotenv import load_dotenv
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
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
