import json
import redis
import asyncio
import os
import logging
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .auth import validate_token
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Redis Connection
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

class FloodConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            # 1. Auth & Region Setup
            query_string = self.scope["query_string"].decode()
            params = parse_qs(query_string)
            token = params.get("token", [None])[0]
            self.region = self.scope["url_route"]["kwargs"]["region"]
            self.redis_channel = f"flood:{self.region}"

            if not token:
                print(f"❌ [WS] No token for region: {self.region}")
                await self.close()
                return

            # Token Validation
            claims = await sync_to_async(validate_token)(token)
            if not claims:
                print(f"❌ [WS] Invalid token for user in {self.region}")
                await self.close()
                return

            await self.accept()
            print(f"✅ [WS] Connected to {self.region}. Listening to Redis: {self.redis_channel}")

            # 2. Push Initial State (Latest Cache)
            latest = await sync_to_async(redis_client.get)(f"flood:latest:{self.region}")
            if latest:
                print(f"📦 [WS] Sending initial cache for {self.region}")
                await self.send(text_data=latest)

            # 3. Start Pub/Sub Task
            self.listen_task = asyncio.create_task(self.listen_to_redis_pubsub())

        except Exception as e:
            print(f"💥 [WS] Connect Error: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, "listen_task"):
            self.listen_task.cancel()
            print(f"🔌 [WS] Disconnected from {self.region}. Task cancelled.")

    async def listen_to_redis_pubsub(self):
        pubsub = redis_client.pubsub()
        pubsub.subscribe(self.redis_channel)
        print(f"📡 [WS] Pub/Sub subscribed to {self.redis_channel}")

        try:
            while True:
                # get_message checks for new data in Redis
                message = await sync_to_async(pubsub.get_message)(
                    ignore_subscribe_messages=True, 
                    timeout=1.0
                )

                if message and message["type"] == "message":
                    raw_data = message["data"]
                    print(f"🔔 [WS] New Data received from Redis for {self.region}!")
                    
                    # 🔥 CRITICAL: Frontend ko data bhej rahe hain
                    await self.send(text_data=raw_data)
                    print(f"📤 [WS] Data sent to Frontend successfully.")

                await asyncio.sleep(0.1) # Prevent CPU spike

        except asyncio.CancelledError:
            pubsub.unsubscribe()
            pubsub.close()
        except Exception as e:
            print(f"💀 [WS] PubSub Loop Error: {str(e)}")
            await self.close()
