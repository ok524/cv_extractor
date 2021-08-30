import os
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from dotenv import load_dotenv
load_dotenv()

import json
import asyncio
import aio_pika
from aio_pika import connect, IncomingMessage, ExchangeType

from makeplaintext.main import convert2text

def on_message(message: IncomingMessage):
    with message.process():
        print(" [cv] %r:%r" % (message.routing_key, message.body))
        ajson = {}
        try:
            ajson = json.loads(message.body)
            converted_filename = convert2text(ajson['filepath'], ajson['filename'], ajson['hash_val'], ajson['outputfolder'])
        except Exception as e:
            raise(e)


async def main(loop):
    # Perform connection
    connection = await connect(
        os.environ.get('MQ_AMQP'), loop=loop
    )

    # Creating a channel
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    # Declare an exchange
    topic_logs_exchange = await channel.declare_exchange(
        os.environ.get('MQ_TOPIC_UPLOAD'), ExchangeType.TOPIC
    )

    # Declaring queue
    queue = await channel.declare_queue(
        os.environ.get('MQ_QUEUE_EXTRACT'), durable=True
    )

    binding_keys = [os.environ.get('MQ_ROUTE_UPLOAD')]

    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
        sys.exit(1)

    for binding_key in binding_keys:
        await queue.bind(topic_logs_exchange, routing_key=binding_key)

    # Start listening the queue with name 'task_queue'
    await queue.consume(on_message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))

    # we enter a never-ending loop that waits for
    # data and runs callbacks whenever necessary.
    print(" [*] Waiting for messages. To exit press CTRL+C")
    loop.run_forever()
