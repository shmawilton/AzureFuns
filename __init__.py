from azure.cosmos import CosmosClient, PartitionKey
import random
import datetime
import os
from config import settings

# Initialize Cosmos client
client = CosmosClient(settings['host'], credential=settings['master_key'])

# Create or get database
database_name = 'sensorDB'
database = client.create_database_if_not_exists(id=database_name)

# Create or get container
container_name = 'sensorContainer'
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/sensorID"),
    offer_throughput=400
)

# Function to simulate sensor data
def simulate_sensor_data(sensor_id):
    return {
        "id": f"sensor_{sensor_id}_{datetime.datetime.now().isoformat()}",
        "sensor_id": sensor_id,
        "temperature": round(random.uniform(8, 15), 2),
        "wind": round(random.uniform(15, 25), 2),
        "relative_humidity": round(random.uniform(40, 70), 2),
        "co2": round(random.uniform(500, 1500), 2),
        "timestamp": datetime.datetime.now().isoformat()
    }

# Simulate data for 20 sensors and insert into the container
for sensor_id in range(1, 21):
    sensor_data = simulate_sensor_data(sensor_id)
    container.upsert_item(sensor_data)

print("Data generation and insertion complete.")
