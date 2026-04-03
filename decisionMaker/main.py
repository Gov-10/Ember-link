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
from langchain_groq import ChatGroq

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

def callback(message):
    try:
        data=json.loads(message.data.decode("utf-8"))
        
        region=data.get("region")
        risk=data.get("res")
        route=data.get("route_coords")
        shelter=data.get("target_shelter")
        instruction=data.get("instructions")
        msg=message_gen(region, risk, shelter, instruction)
        output={"region": region, "risk_level": risk, "message": msg, "route": route, "target_shelter": shelter, "status": "NOTIFIED"}
        publisher.publish(history_topic_path, json.dumps(output).encode("utf-8"))
        logger.info(f"AI message: {msg}")
        message.ack()
        #TODO: Idhar SMS ka code likhna baaki hai
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

    
    

        

