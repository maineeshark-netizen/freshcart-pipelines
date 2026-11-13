
import pika
import sys
import json

if len(sys.argv) != 3:
    print("Usage: python driver.py NAME PATTERN")
    sys.exit(1)

name = sys.argv[1]
pattern = sys.argv[2]

# Connect to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)

channel = connection.channel()

# Declare the topic exchange
channel.exchange_declare(
    exchange="rapido-dispatch",
    exchange_type="topic",
    durable=True
)

# Create a private queue for this driver
result = channel.queue_declare(
    queue="",
    exclusive=True,
    auto_delete=True
)

queue_name = result.method.queue

# Bind queue using the given pattern
channel.queue_bind(
    exchange="rapido-dispatch",
    queue=queue_name,
    routing_key=pattern
)

print(f"{name} is waiting for requests matching: {pattern}")

def callback(ch, method, properties, body):
    message = json.loads(body)

    print(f"\nDriver: {name}")
    print(f"Routing key: {method.routing_key}")
    print(f"Message: {message}")

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=False
)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print(f"\n{name} stopped.")
    channel.stop_consuming()
finally:
    connection.close()
