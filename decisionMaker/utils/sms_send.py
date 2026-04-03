import os
from dotenv import load_dotenv
load_dotenv()
from twilio.rest import Client

ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
COMPANY_NUMBER = os.getenv("COMPANY_NUMBER")
client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_mess(rec, data):
    try:
        client.messages.create(body=data, from_=COMPANY_NUMBER, to=f'+{rec}')
    except Exception as e:
        print(f"Error: {e}")

