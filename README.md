#  EmberLink: The Neural Network for Disaster Survival
**EmberLink** is an event-driven, AI-powered command center designed to navigate the chaos of urban flooding. By merging real-time sensor data with graph theory and Large Language Models (LLMs), it provides citizens and NGOs with the **safest** possible evacuation routes, not just the shortest ones.

### NOTE: Currently, for demo purposes, some sections of this project use Demo Data
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
5. Caching: Redis
6. Queue System: GCP PubS
7. Other Tools: Amazon API Gateway (Rate Limiting), AWS Lambda
