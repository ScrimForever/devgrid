import boto3
import os
from loguru import logger

client = boto3.resource('sqs', region_name='us-east-1')
receive_client = boto3.client('sqs', region_name='us-east-1', )
queue = client.get_queue_by_name(QueueName=f"{os.getenv('SQS_QUEUE_NAME')}")

