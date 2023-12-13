from azure.cosmos import CosmosClient, PartitionKey
import matplotlib.pyplot as plt
import os
from config import settings

# Initialize Cosmos client
client = CosmosClient(settings['host'], credential=settings['master_key'])

# Get database and container
database_name = 'sensorDB'
container_name = 'sensorContainer'
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

# Function to retrieve sensor data
def retrieve_sensor_data():
    sensor_data = {}
    query = "SELECT c.sensor_id, c.temperature, c.wind, c.timestamp FROM c ORDER BY c.timestamp"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))

    for item in items:
        sensor_id = item['sensor_id']
        if sensor_id not in sensor_data:
            sensor_data[sensor_id] = {'temperature': [], 'wind': [], 'timestamps': []}

        sensor_data[sensor_id]['temperature'].append(item['temperature'])
        sensor_data[sensor_id]['wind'].append(item['wind'])
        sensor_data[sensor_id]['timestamps'].append(item['timestamp'])

    return sensor_data

# Retrieve data
data = retrieve_sensor_data()

# Plotting function
def plot_sensor_data(data):
    plt.figure(figsize=(15, 6))

    # Temperature plot
    plt.subplot(1, 2, 1)
    for sensor_id, readings in data.items():
        plt.plot(readings['timestamps'], readings['temperature'], label=f'Sensor {sensor_id}')
    plt.title('Temperature over Time for Each Sensor')
    plt.xlabel('Time')
    plt.ylabel('Temperature (Celsius)')
    plt.legend()

    # Wind plot
    plt.subplot(1, 2, 2)
    for sensor_id, readings in data.items():
        plt.plot(readings['timestamps'], readings['wind'], label=f'Sensor {sensor_id}')
    plt.title('Wind Speed over Time for Each Sensor')
    plt.xlabel('Time')
    plt.ylabel('Wind Speed (miles/hour)')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Plot the data
plot_sensor_data(data)
