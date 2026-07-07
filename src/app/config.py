import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_USERNAME = os.getenv("KAFKA_USERNAME", "")
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD", "")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "user_service")
KAFKA_SSL_CA_LOCATION = os.getenv("KAFKA_SSL_CA_LOCATION", "ca.pem")