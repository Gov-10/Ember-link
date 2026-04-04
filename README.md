#  EmberLink: The Neural Network for Disaster Survival
**EmberLink** is an event-driven, AI-powered command center designed to navigate the chaos of urban flooding. By merging real-time sensor data with graph theory and Large Language Models (LLMs), it provides citizens and NGOs with the **safest** possible evacuation routes, not just the shortest ones.

### NOTE: Currently, for demo purposes, some sections of this project use Demo Data

## Demo video
[![Watch Demo](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=IUFPjjRpaHs)
(Please note that this video was recorded in Nagpur, hence the distance~970km)

## Architecture Diagram
![System Architecture](./docs/arc.png)

## Key Features
* **🛰️ Real-Time Threat Analysis:** Live WebSocket integration for regional flood risk monitoring.
* **📍 Dynamic Dijkstra Routing:** Calculates evacuation paths using Dijkstra’s algorithm on OpenStreetMap (OSM) data, factoring in real-time "hazard zones."
* **🤖 AI Decision Maker:** Utilizes LangChain & ChatGroq to craft localized emergency protocols and SMS alerts.
* **🛡️ Role-Based Command:** Distinct interfaces and permissions for **Citizens** and **NGO Responders** via AWS Cognito Groups.
* **📡 Tactical HUD:** A high-contrast, dark-mode dashboard designed for visibility in high-stress emergency environments.

## Tech Stack
1. Frontend: NextJS
2. Backend Services: Django Ninja, FastAPI
3. Messaging: Twilio
4. Authentication: Amazon Cognito
5. Caching: Redis, Cloudflare workers (for caching external API results)
6. Queue System: GCP Pub/Sub
8. Other Tools: Amazon API Gateway (Rate Limiting), AWS Lambda

## Setup 
1. Cloning and virtual env setup
   ```bash
   git clone https://github.com/Gov-10/Ember-link
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Frontend
   ```bash
   cd front
   npm install
   npm run dev
   ```
3. Django Ninja
   ```bash
   cd backend
   pip3 install -r requirements.txt
   python3 manage.py migrate
   daphne backend.asgi:application
   ```
4. dataIngestor
   ```bash
   cd dataIngestor
   pip3 install -r requirements.txt
   uvicorn main:app --reload --port 8001
   ```
5. decisionMaker
   ```bash
   cd decisionMaker
   pip3 install -r requirements.txt
   uvicorn main:app --reload --port 8002
   ```
6. evacService
   ```bash
   cd evacService
   pip3 install -r requirements.txt
   uvicorn main:app --reload --port 8003
   ```
7. predictionService
   ```bash
   cd predictionService
   pip3 install -r requirements.txt
   uvicorn main:app --reload --port 8004
   ```
8. worker
   ```bash
   cd worker
   pip3 install -r requirements.txt
   uvicorn worker:app --reload --port 8005
   ```
   
## Environment Variables
1. Frontend
   ```bash
   NEXT_PUBLIC_USER_POOL_ID
   NEXT_PUBLIC_USER_POOL_CLIENT_ID
   ```
2. Django Ninja
   ```bash
   COGNITO_REGION
   USER_POOL_ID
   USER_POOL_CLIENT_ID
   REDIS_HOST
   REDIS_PASSWORD
   REDIS_PORT
   ```
3. Data Ingestor
   ```bash
   TOPIC_PATH
   USE_MOCK=True
   ```
4. Decision Maker
   ```bash
   SUBSCRIPTION2_PATH
   HISTORY_TOPIC
   GROQ_API_KEY
   NINJA_API_URL
   ACCOUNT_SID
   AUTH_TOKEN
   COMPANY_NUMBER
   ```
5. Prediction Service
   ```bash
   SUBSCRIPTION_PATH
   ML_TOPIC
   ```
6. Worker
   ```bash
   FINAL_SUB
   COGNITO_REGION
   USER_POOL_ID
   USER_POOL_CLIENT_ID
   REDIS_HOST
   REDIS_PORT
   REDIS_PASSWORD
   ```

   
