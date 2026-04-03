import os
import json
import logging
from dotenv import load_dotenv
load_dotenv()
from google.cloud import pubsub_v1
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)
PROJECT_ID = os.getenv("PROJECT_ID")
EVAC_SUB = os.getenv("EVAC_SUBSCRIPTION")
HISTORY_TOPIC = os.getenv("HISTORY_TOPIC_ID")
publisher = pubsub_v1.PublisherClient()
history_topic_path = publisher.topic_path(PROJECT_ID, HISTORY_TOPIC)
subscriber=pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, EVAC_SUB)
from utils.sms_send import send_mess
from langchain_groq import ChatGroq
import requests

#NOTE: GROQ API Key set karna baaki hai bhai

llm= ChatGroq(model="qwen/qwen3-32b", temperature=0, max_tokens=None, reasoning_format="hidden", timeout=None, max_retries=3)

                                        
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def healthchek():
    return {"status": "RUNNING"}

def message_gen(region, risk, shelter, instruction):
    prompt = f"""
    Context: A {risk} risk disaster is occurring in {region}. 
    Evacuation Route: {instruction} to {shelter}.
    Task: Draft a 160-character SMS for local villagers in Hindi and English.
    Make it urgent but calm.
    """
    msg= llm.invoke(prompt)
    return msg.content
def msg_ngo(region, risk, ngo, population):
    prompt = f"""  
            Context: A {risk} risk disaster is occuring in {region} with {population} density.
            Task: Draft a short SMS for a ngo with {ngo["ambulances"]} ambulances, {ngo["food_pac"]} food packets, {ngo["volunteers"]} volunteers, on how many vehicles to send, how many food packets to dispatch and how many volunteers to dispatch.
            Make it urgent but calm
    """
    msg= llm.invoke(prompt)
    return msg.content
NINJA_API_URL=os.getenv("NINJA_API_URL")
def get_users():
    try:
        resp=requests.get(f"{NINJA_API_URL}/users?role=user")
        return list(resp.json())
    except Exception as e:
        logger.error(f"error: {e}")
        return []

def callback(message):
    try:
        data=json.loads(message.data.decode("utf-8"))
        
        region=data.get("region")
        risk=data.get("res")
        route=data.get("route_coords")
        shelter=data.get("target_shelter")
        instruction=data.get("instructions")
        ngos= data.get("ngos")
        population=300
        for ngo in ngos:
            aim=msg_ngo(region, risk, ngo,population)
            send_mess(ngo["phone"], aim)
        msg=message_gen(region, risk, shelter, instruction)
        output={"region": region, "risk_level": risk, "message": msg, "route": route, "target_shelter": shelter, "status": "NOTIFIED"}
        publisher.publish(history_topic_path, json.dumps(output).encode("utf-8"))
        logger.info(f"AI message: {msg}")
        message.ack()
        users=get_users()
        for user in users:
            send_mess(user["phone"], msg)
    except Exception as e:
        logger.error(f"Error: {e}")
        message.nack()

@app.on_event("startup")
def start_sub():
    flow_control=pubsub_v1.types.FlowControl(max_messages=10)
    subscriber.subscribe(
        subscription_path,
        callback=callback,
        flow_control=flow_control
    )
    logger.info("AI on hai ji...")

    
    

        

