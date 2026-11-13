
import pika
import json
import random
import time
import uuid
from datetime import datetime

# Connect to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

# Create a topic exchange
channel.exchange_declare(
    exchange="rapido-dispatch",
    exchange_type="topic",
    durable=True
)

cities = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "whitefield"]
}

try:
    while True:
        city = random.choice(list(cities.keys()))
        zone = random.choice(cities[city])
        request_type = random.choice(["ride", "food"])

        routing_key = f"{city}.{zone}.{request_type}"

        message = {
            "id": str(uuid.uuid4()),
            "city": city,
            "zone": zone,
            "type": request_type,
            "ts": datetime.now().isoformat()
        }

        channel.basic_publish(
            exchange="rapido-dispatch",
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

        print("Published:", routing_key, message)

        time.sleep(2)

except KeyboardInterrupt:
    print("Dispatcher stopped.")

finally:
    connection.close()
