import pika

class RabbitMQAdapter:
    def __init__(self, host='localhost', queue='default'):
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def send_message(self, message):
        if not self.channel:
            raise Exception("Not connected to RabbitMQ")
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=message)
        print(f" [x] Sent '{message}'")

    def consume_messages(self, callback):
        if not self.channel:
            raise Exception("Not connected to RabbitMQ")
        self.channel.basic_consume(queue=self.queue, on_message_callback=callback, auto_ack=True)
        print(f" [*] Waiting for messages in '{self.queue}'. To exit press CTRL+C")
        self.channel.start_consuming()

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print(" [x] Connection closed")
