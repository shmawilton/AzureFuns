import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://sensorsql.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'DtzEssvymXLpgFxSUgwjbeedaujBvmJYtPWDBJwrr7UmUu0MuOGgTm3mP7Hvfb4JGeK3h54hw9qIACDbRVUVTQ=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'sensorDB'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'sensorContainer'),
}