import boto3
from dotenv import load_dotenv

import json
import os

QUEUE_NAME = "md410.fifo"
QUEUE_URL = "https://sqs.af-south-1.amazonaws.com/960171457841/md410.fifo"


load_dotenv()

SESSION = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
SQS = SESSION.resource(
    "sqs",
    region_name="af-south-1",
)
QUEUE = SQS.Queue(QUEUE_URL)


def send_data(data: str, group_id: str = "default"):
    d = json.dumps(data)
    response = QUEUE.send_message(MessageBody=d, MessageGroupId=group_id)


def read_data(max_number_of_messages=1, timeout=5):
    results = QUEUE.receive_messages(
        AttributeNames=["All"],
        MaxNumberOfMessages=max_number_of_messages,
        WaitTimeSeconds=timeout,
    )
    [r.delete() for r in results]
    return [r.body for r in results]


if __name__ == "__main__":
    send_data({"foo": "bar"})
