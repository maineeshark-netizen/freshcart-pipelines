
import pika
import sys
import json

if len(sys.argv) != 3:
    print("Usage: python driver.py NAME PATTERN")
    sys.exit(1)

name = sys.argv[1]
pattern = sys.argv[2]

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost")
)
channel = connection.channel()

channel.exchange_declare(
    exchange="rapido-dispatch",
    exchange_type="topic",
    durable=True
)

result = channel.queue_declare(
    queue="",
    exclusive=True,
    auto_delete=True
)
queue_name = result.method.queue

channel.queue_bind(
    exchange="rapido-dispatch",
    queue=queue_name,
    routing_key=pattern
)

print(f"{name} is waiting for: {pattern}", flush=True)


def callback(ch, method, properties, body):
    message = json.loads(body)

    if "zone" not in message:
        print(
            f"REJECTED: {method.routing_key} | Missing zone | NACK",
            flush=True
        )
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )
    else:
        print(
            f"PROCESSED: {method.routing_key} | {message}",
            flush=True
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=False
)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print(f"{name} stopped.")
    channel.stop_consuming()
finally:
    connection.close()
