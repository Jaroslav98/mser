import pika
from pymongo import MongoClient

RABBIT_QUEUE = 'newstr'
SERVER_HOST = 'mongodb://localhost:27017/'
SERVER_DB = 'verge'
SERVER_COLLECTION = 'articles'


def callback(ch, method, parameters, body):
    """
    Put data in Mongo DB.
    :return: None
    """
    print(" [x] Received %r" % body.decode("utf-8"))
    client = MongoClient(SERVER_HOST)
    db = client[SERVER_DB]
    col = db[SERVER_COLLECTION]
    x = body.decode("utf-8").split("|")
    print(x)
    y = col.insert_one({"title": x[0], "author": x[1], "views": x[2], "href": x[3]})


def get_data() -> None:
    """
    Get data from Rabbit MQ.
    :return: None
    """
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.basic_consume(queue=RABBIT_QUEUE,
                          auto_ack=True,
                          on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    get_data()
