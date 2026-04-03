from fastapi import FastAPI
from dotenv import load_dotenv
import os, json, logging, requests
import networkx as nx
import osmnx as ox
from google.cloud import pubsub_v1
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
PROJECT_ID = os.getenv("PROJECT_ID")
ML_SUBSCRIPTION = os.getenv("ML_SUBSCRIPTION")
EVAC_TOPIC = os.getenv("EVAC_TOPIC_ID")
NINJA_API_URL = os.getenv("NINJA_API_URL")
subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, ML_SUBSCRIPTION)
evac_topic_path = publisher.topic_path(PROJECT_ID, EVAC_TOPIC)
GRAPH_CACHE = {}

def get_graph(region, coords):
    if region not in GRAPH_CACHE:
        logger.info(f"Downloading graph for {region}...")
        GRAPH_CACHE[region] = ox.graph_from_point(
            coords, dist=5000, network_type='drive'
        )
    return GRAPH_CACHE[region]

def get_safe_shelters(region):
    try:
        response = requests.get(f"{NINJA_API_URL}/shelters?region={region}")
        return response.json()
    except Exception as e:
        logger.error(f"DB Fetch Error: {e}")
        return []
def get_ngos():
    try:
        response=requests.get(f"{NINJA_API_URL}/ngos")
        return response.json()
    except Exception as e:
        logger.error(str(e))
        return []

def block_flooded_roads(G, flood_coords, radius=800):
    try:
        flood_node = ox.nearest_nodes(G, flood_coords[1], flood_coords[0])
        nodes_to_remove = nx.single_source_dijkstra_path_length(
            G, flood_node, cutoff=radius, weight='length'
        ).keys()
        G_blocked = G.copy()
        G_blocked.remove_nodes_from(nodes_to_remove)
        logger.info(f"Blocked {len(list(nodes_to_remove))} nodes")
        return G_blocked
    except Exception as e:
        logger.error(f"Road blocking error: {e}")
        return G

def calculate_evac_route(G, start_coords, shelters):
    orig_node = ox.nearest_nodes(G, start_coords[1], start_coords[0])
    best_route = None
    closest_shelter = None
    min_dist = float('inf')
    for shelter in shelters:
        try:
            dest_node = ox.nearest_nodes(
                G, shelter['longitude'], shelter['latitude']
            )

            route = nx.shortest_path(G, orig_node, dest_node, weight='length')
            dist = nx.shortest_path_length(G, orig_node, dest_node, weight='length')
            if dist < min_dist:
                min_dist = dist
                best_route = route
                closest_shelter = shelter
        except nx.NetworkXNoPath:
            continue
    return best_route, closest_shelter, min_dist

def callback(message):
    try:
        data = json.loads(message.data.decode("utf-8"))
        if data.get("res") != "HIGH":
            message.ack()
            return
        region = data.get("region")
        lat = data.get("latitude")
        lon = data.get("longitude")
        if not (region and lat and lon):
            logger.warning("Missing location data")
            message.ack()
            return
        shelters = get_safe_shelters(region)
        ngos=get_ngos()
        if not shelters:
            logger.warning("No shelters available")
            message.ack()
            return
        start = (lat, lon)
        G = get_graph(region, start)
        G_blocked = block_flooded_roads(
            G,
            flood_coords=start,
            radius=800
        )
        route, target, distance = calculate_evac_route(
            G_blocked,
            start,
            shelters
        )
        if not target or not route:
            logger.warning("No valid evacuation route found")
            message.ack()
            return
        route_coords = [
            (G_blocked.nodes[n]['y'], G_blocked.nodes[n]['x'])
            for n in route
        ]
        output = {
            "risk": data.get("res"),
            "region": region,
            "target_shelter": target['name'],
            "distance_m": distance,
            "route": route_coords,
            "ngos": ngos,
            "instructions": f"Proceed to {target['name']}. Distance: {round(distance/1000, 2)} km"
        }
        publisher.publish(
            evac_topic_path,
            json.dumps(output).encode("utf-8")
        )
        logger.info(f"Evac Plan Generated for {region}")
        message.ack()
    except Exception as e:
        logger.error(f"Error: {e}")
        message.nack()

app = FastAPI()

@app.on_event("startup")
def start_sub():
    flow_control = pubsub_v1.types.FlowControl(max_messages=10)
    subscriber.subscribe(
        subscription_path,
        callback=callback,
        flow_control=flow_control
    )
    logger.info("Evac Service Running...")

@app.get("/health")
def health():
    return {"status": "RUNNING"}
