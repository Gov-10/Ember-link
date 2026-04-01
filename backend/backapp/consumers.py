import json
import redis
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
from .auth import validate_token
import os
from dotenv import load_dotenv
load_dotenv()
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

class FloodConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            query_string = self.scope["query_string"].decode()
            params = parse_qs(query_string)
            token = params.get("token", [None])[0]
            if not token:
                await self.close()
                return
            claims = validate_token(token)
            self.user_sub = claims["sub"]
            self.role = "ngo" if "ngos" in claims.get("cognito:groups", []) else "user"
            self.region = self.scope["url_route"]["kwargs"]["region"]
            self.group_name = f"flood_{self.region}_{self.role}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            latest = redis_client.get(f"flood:latest:{self.region}")
            if latest:
                await self.send(text_data=latest)
        except Exception as e:
            print("WebSocket auth error:", str(e))
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name,self.channel_name)

    async def send_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))


