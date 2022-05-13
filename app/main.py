import os
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from dotenv import load_dotenv
load_dotenv()

import json

from typing import Optional
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import aio_pika
from aio_pika import connect, Message, DeliveryMode, ExchangeType

from util.util import group_line_to_para, genHashBinary
from extract.main import extract, Extractor


app = FastAPI()

origins = [
    "*",
    "http://localhost",
    "http://localhost:3001",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

paths = {
    "0": {
        "path_pdf": "zero",
        "path_txt": "zero",
    }
}

@app.get("/")
async def read_root():
    # a = Extractor('a')
    # b = Extractor('>bbbbbb')
    return {"Hello": "World" }


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):

    await file.seek(0)
    content = await file.read()
    with open('./data/{}'.format(file.filename), mode='b+w') as f:
        f.write(content)

    hash_val = genHashBinary('./data/{}'.format(file.filename))


    # Perform connection
    connection = await connect(
        os.environ.get('MQ_AMQP')
    )

    # Creating a channel
    channel = await connection.channel()

    topic_logs_exchange = await channel.declare_exchange(
        os.environ.get('MQ_TOPIC_UPLOAD'), ExchangeType.TOPIC
    )
    routing_key = os.environ.get('MQ_ROUTE_UPLOAD')

    # Message
    ajson = {
        "filepath": './data/{}'.format(file.filename),
        "filename": file.filename,
        "outputfolder": os.environ.get('PLAINTEXT_FOLDER'),
        "hash_val": hash_val,
    }
    message_body = f"{json.dumps(ajson)}".encode()
    message = Message(
        message_body,
        delivery_mode=DeliveryMode.PERSISTENT
    )

    # Sending the message
    await topic_logs_exchange.publish(message, routing_key=routing_key)
    print(" [x] Sent %r" % message)
    await connection.close()

    return {
        "filename": ajson['filename'],
        "hash_val": ajson['hash_val'],
    }


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    # File location
    path_pdf = paths[str(item_id)]['path_pdf'] if str(item_id) in paths else paths[str(0)]['path_pdf']
    path_txt = paths[str(item_id)]['path_txt'] if str(item_id) in paths else paths[str(0)]['path_txt']

    # print(path_pdf)
    # print(path_txt)

    # Query db for records
    dbjson = {}
    with open(os.environ.get('JSONDBPATH'), mode="r", encoding="utf-8") as f:
        dbjson = json.loads(f.read())

    print(json.dumps(dbjson))
    print()
    print(str(item_id))

    if str(item_id) in dbjson:
        path_pdf = dbjson[str(item_id)]['path_pdf']
        path_txt = dbjson[str(item_id)]['path_txt']

        print(path_pdf)
        print(path_txt)


    # Meta of file
    arr_folder = path_pdf.split("/")
    pdf_filename = arr_folder[len(arr_folder) - 1]
    arr_folder = path_txt.split("/")
    text_filename = arr_folder[len(arr_folder) - 1]

    # Extract information
    instance = Extractor(path_txt)
    ret = instance.run_all()

    # Original plaintext
    f = open(path_txt, mode='r')

    return {
        "text": group_line_to_para(f.read()),
        "meta": {
            "path_text": path_txt,
            "text_filename": text_filename,
            "pdf_filename": pdf_filename,
        },
        "data": {
            "name": {
                "text": ret['name'],
                "line": ret['name_lines'],
                "tag": ret['gender']
            },
            "email": ret['emails'],
            "education": ret['edus'] + [
                {
                    "major": "",
                    "school": "",
                    "grade": "",
                    "date": "",
                }
            ],
            "years": ret['years'],
            "workExp": [
                {
                    "title": "",
                    "organization": "",
                    "date": "",
                }
            ],
            "award": [
                {
                    "title": "",
                    "organization": "",
                    "date": "",
                }
            ],
            "qualification": [
                {
                    "title": "",
                    "organization": "",
                    "date": "",
                }
            ],
            "eca": ret['ecas'] + [
                {
                    "title": "",
                    "organization": "",
                    "date": "",
                }
            ],
            "skillSets": ret['skill_sets'],
            "ner": ret['entity'],
        },
        "status": "SUCCESS"
    }

"""
API functions map
1. upload file to server
    - hash
2. convert to plaintext
    - docx
    - image
    - pdf
3. parse/extract plaintext
    - NER
    - softskills
4. store into database
5. display result + query(sorting/filter) records
6. listing of entries (pagination)
7. Top 10 xyz
"""
