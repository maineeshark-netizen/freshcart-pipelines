
import pika
import json
import random
import time
import uuid
from datetime import datetime

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

channel.exchange_declare(
    exchange="rapido-dispatch",
    exchange_type="topic",
    durable=True
)

cities = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "whitefield"]
}

count = 0

try:
    while True:
        count += 1

        city = random.choice(list(cities.keys()))
        zone = random.choice(cities[city])
        request_type = random.choice(["ride", "food"])

        routing_key = f"{city}.{zone}.{request_type}"

        message = {
            "id": str(uuid.uuid4()),
            "city": city,
            "type": request_type,
            "ts": datetime.now().isoformat()
        }

        # Send a bad message every 10 messages
        if count % 10 != 0:
            message["zone"] = zone

        channel.basic_publish(
            exchange="rapido-dispatch",
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )

        print(
            f"Published #{count}: {routing_key} | {message}",
            flush=True
        )

        time.sleep(2)

except KeyboardInterrupt:
    print("Dispatcher stopped.")

finally:
    connection.close()
