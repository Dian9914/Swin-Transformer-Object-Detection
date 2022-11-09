import os

from RabbitMQ.rabbitMQ import RabbitMQ
from dotenv import load_dotenv

load_dotenv()


# create a function which is called on incoming messages
def callback(body):
    print('received message from channel with body', body)


def main():
    rabMQ = RabbitMQ(host=os.getenv("RABBITMQ_HOST"), port=os.getenv("RABBITMQ_PORT"),
                     queue=os.getenv("RABBITMQ_QUEUE"), heartbeat=int(os.getenv("RABBITMQ_HEARTBEAT")))
    rabMQ.consume(callback=callback)
    rabMQ.close()


if __name__ == "__main__":
    main()
