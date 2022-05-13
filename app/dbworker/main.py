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

import psycopg2


def logger():
    pass


# Connection to database server
def getdb(conn):
    if conn is not None:
        return conn

    try:
        conn = psycopg2.connect(
            host=os.getenv("HOST", default="localhost"),
            database=os.getenv("DBNAME", default=None),
            port=os.getenv("DBPORT", default=5432),
            user=os.getenv("DBUSERNAME", default=None),
            password=os.getenv("DBPASSWORD", default=None),
        )
    except Exception as e:
        logger("Error", "002", f"getdb:: {e}\n")
        return None
        pass

    return conn


def commit_sql(file_list, conn):

    # Create cursor to execute SQL commands
    cur = conn.cursor()

    for item in file_list:

        # SQL statments
        command_insert = '''INSERT INTO tbl_cv(
            "hash_val",
            "filename",
            "converted_filename",
            "created_at",
            "updated_at",
            "status",
            "doc_stat",
        )
        VALUES (%s,%s,%s,%s,%s, %s)'''
        command_update = '''UPDATE tbl_cv SET doc_stat = %s, status = %s WHERE hash_val = %s;'''

        # Values
        aname = "none"
        user_uuid = "e3cdd791-9562-4f08-b353-3b8c01861f8b"
        submissionid = int(item["submissionid"])
        docid = int(item["docid"])
        json_str = item["json_str"]
        try:
            # INSERT
            cur.execute(command_insert, (
                submissionid,
                datetime.now(),
                aname,
                aname,
                aname + "_01",

                "file_" + aname,
                0.0,
                json_str,
                user_uuid,
                docid
            ))
            logger("Info", f"commit_sql: pending insert {submissionid} {docid}")
        except Exception as e:
            if -1 != f"{e}".find("bigint out of range"):
                raise Exception(f"PostgreSQL Error: {e}")
                return -1

            # UPDATE
            conn = getdb(None)
            cur = conn.cursor()
            cur.execute(command_update, (json_str, submissionid, docid))
            logger("Info", f"commit_sql: pending update {submissionid} {docid} {e}")
        finally:
            conn.commit()

    # Close the cursor
    cur.close()
    return 0


def on_message(message: IncomingMessage):
    with message.process():
        print(" [db] %r:%r" % (message.routing_key, message.body))
        ajson = {}
        try:
            ajson = json.loads(message.body)
            print(f" [db] {ajson['hash_val']}")

            # Operate JSON db
            dbjson = {}
            with open(os.environ.get('JSONDBPATH'), mode="r", encoding="utf-8") as f:
                dbjson = json.loads(f.read())
                if ajson['hash_val'] not in dbjson:
                    dbjson[ajson['hash_val']] = {
                        "path_pdf": f"/omar_prj/app/all_clap/cv_extractor/app/{ajson['filepath']}",
                        "path_txt": f"/omar_prj/app/all_clap/cv_extractor/app/data/output_files/converted_{ajson['filename']}_{ajson['hash_val']}.txt",
                    }

            with open(os.environ.get('JSONDBPATH'), mode="w", encoding="utf-8") as f:
                f.write(json.dumps(dbjson))

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
        os.environ.get('MQ_QUEUE_UPLOAD'), durable=True
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