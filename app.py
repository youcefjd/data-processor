import json
import time
from kafka import KafkaConsumer, KafkaProducer
from collections import defaultdict

# This example has two different result topics

# There is a Python client that is both a consumer (consumes from the source topic) and a producer (produces to a target topic)

# Kafka config

BOOTSTRAP_SERVERS = 'kafka:9092'
SOURCE_TOPIC = 'user-login'
PROCESSED_TOPIC = 'processed-logins'
AGGREGATION_TOPIC = 'user-aggregations'

# Consumer and Producer initialization function with retry
# I added the retry logic in case the broker doesn't spin up before the consumers and/or the producers

def create_kafka_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                SOURCE_TOPIC,
                bootstrap_servers=BOOTSTRAP_SERVERS,
                auto_offset_reset='earliest',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            return consumer
        except Exception as e:
            print(f"error creating consumer: {e}. retrying...")
            time.sleep(5)

def create_kafka_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=BOOTSTRAP_SERVERS,
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )
            return producer
        except Exception as e:
            print(f"error creating producer: {e}. Retrying...")
            time.sleep(5)

consumer = create_kafka_consumer()
producer = create_kafka_producer()

# Produce example data to user-login topic
def produce_to_user_login():
    login_data = {
        "user_id": "user123",
        "app_version": "1.0.0",
        "device_type": "mobile",
        "ip": "192.168.1.1",
        "locale": "en-US",
        "device_id": "device456",
        "timestamp": "2024-12-15T10:00:00"
    }
    producer.send(SOURCE_TOPIC, value=login_data)
    producer.flush() 
    print(f"Produced data to {SOURCE_TOPIC}: {login_data}")

# Simple aggregation logic
user_login_count = defaultdict(int)

produce_to_user_login()

# Consume and process messages
for message in consumer:
    data = message.value

    processed_data = {
        "user_id": data["user_id"],
        "app_version": data["app_version"],
        "device_type": data["device_type"],
        "ip": data["ip"],
        "locale": data["locale"],
        "device_id": data["device_id"],
        "processed_timestamp": data["timestamp"]  # Adding a timestamp key to account for when the message was processed
    }

    # Send the processed message to 'processed-logins' topic
    producer.send(PROCESSED_TOPIC, value=processed_data)

    # Update aggregation (in this case the count logins per user_id)
    user_login_count[data["user_id"]] += 1
    aggregation_data = {"user_id": data["user_id"], "login_count": user_login_count[data["user_id"]]}

    # Send aggregation results to 'user-aggregations' topic
    producer.send(AGGREGATION_TOPIC, value=aggregation_data)
