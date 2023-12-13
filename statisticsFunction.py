from azure.cosmos import CosmosClient
import numpy as np
from config import settings

# Initialize Cosmos client
client = CosmosClient(settings['host'], credential=settings['master_key'])

# Get database and container
database_name = 'sensorDB'
container_name = 'sensorContainer'
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

def calculate_statistics():
    query = "SELECT * FROM c"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))

    # Organize data by sensor
    sensor_data = {}
    for item in items:
        sensor_id = item['sensor_id']
        if sensor_id not in sensor_data:
            sensor_data[sensor_id] = {'temperature': [], 'wind': [], 'humidity': [], 'co2': []}
        
        sensor_data[sensor_id]['temperature'].append(item['temperature'])
        sensor_data[sensor_id]['wind'].append(item['wind'])
        sensor_data[sensor_id]['humidity'].append(item['relative_humidity'])
        sensor_data[sensor_id]['co2'].append(item['co2'])

    # Calculate statistics for each sensor
    statistics = {}
    for sensor_id, readings in sensor_data.items():
        statistics[sensor_id] = {
            'temperature': {
                'avg': np.mean(readings['temperature']),
                'min': np.min(readings['temperature']),
                'max': np.max(readings['temperature'])
            },
            'wind': {
                'avg': np.mean(readings['wind']),
                'min': np.min(readings['wind']),
                'max': np.max(readings['wind'])
            },
            'humidity': {
                'avg': np.mean(readings['humidity']),
                'min': np.min(readings['humidity']),
                'max': np.max(readings['humidity'])
            },
            'co2': {
                'avg': np.mean(readings['co2']),
                'min': np.min(readings['co2']),
                'max': np.max(readings['co2'])
            }
        }

    return statistics

# Perform the statistics calculation
sensor_statistics = calculate_statistics()
print(sensor_statistics)
