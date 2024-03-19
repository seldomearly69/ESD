import pika

def set_up():
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()

    # Define exchange name and queues
    exchange_name = "ESD"
    email_queue = "Email_Queue"

    # Assert the exchange and queues
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=True)
    channel.queue_declare(queue=email_queue, durable=True)

    # Setting bindings
    channel.queue_bind(exchange=exchange_name, queue=email_queue, routing_key="*.email")

    print("Channels, Exchange & Queues created")

    # Closing the channel and connection
    channel.close()
    connection.close()


