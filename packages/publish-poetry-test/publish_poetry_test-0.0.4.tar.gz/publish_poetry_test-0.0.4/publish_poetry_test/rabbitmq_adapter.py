import pika

class RabbitMQAdapter:
    def __init__(self, host='localhost', port=5672, username='liferaft', password='admin'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
            self.connection = pika.BlockingConnection(parameters)
            print("Successfully connected to RabbitMQ")
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection to RabbitMQ closed")

# Example usage:
if __name__ == "__main__":
    adapter = RabbitMQAdapter(host='localhost', username='liferaft', password='admin')
    adapter.connect()
    adapter.close_connection()
