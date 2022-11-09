import json
import os

from RabbitMQ.rabbitMQ import RabbitMQ
from dotenv import load_dotenv

load_dotenv()


def main():
    rabMQ = RabbitMQ(host=os.getenv("RABBITMQ_HOST"), port=os.getenv("RABBITMQ_PORT"),
                     queue=os.getenv("RABBITMQ_QUEUE"), heartbeat=int(os.getenv("RABBITMQ_HEARTBEAT")))

    with open('../data/mission_images.json') as file:
        data = json.load(file)
    rabMQ.publish(json.dumps(data), routing_key=os.getenv("RABBITMQ_QUEUE"))
    rabMQ.close()


if __name__ == "__main__":
    main()
