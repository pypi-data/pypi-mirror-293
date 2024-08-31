import pika

class RabbitMQAdapter:
    def __init__(self, host='localhost', username='liferaft', password='admin', queue='default'):
        self.host = host
        self.username = username
        self.password = password
        self.queue = queue
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(host=self.host, credentials=credentials)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)
            print("Successfully connected to RabbitMQ")
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection to RabbitMQ closed")

# Test the connection
adapter = RabbitMQAdapter()
adapter.connect()
adapter.close_connection()
