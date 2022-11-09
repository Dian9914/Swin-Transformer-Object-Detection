import threading
import pika


class RabbitMQ:

    def __init__(self, host, queue, port=5672, heartbeat=60):
        # heartbeat of value 0 means no heartbeat. value is in seconds

        self.host = host
        self.port = port
        self.queue = queue
        self.heartbeat = heartbeat
        self.connection = None
        self.channel = None

        self.init_connection()

    def init_connection(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port, heartbeat=self.heartbeat))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue)

        self.connection = connection
        self.channel = channel

    def publish(self, body, exchange='', routing_key=''):
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body)

    def close(self):
        self.connection.close()

    def consume(self, callback=None):

        def cb(ch, method, properties, body):

            if callback is not None:
                t = threading.Thread(target=callback, args=(body, ))
                t.daemon = True
                t.start()

                while t.is_alive():
                    print("Heart beating")
                    self.connection.process_data_events()
                    self.connection.sleep(20)

            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("Finished and ack message ")

        self.channel.basic_consume(self.queue, cb)
        self.channel.start_consuming()
