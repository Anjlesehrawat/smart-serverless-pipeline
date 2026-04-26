import json
import boto3
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ProcessedFiles')

sns = boto3.client('sns')

SNS_TOPIC_ARN = "YOUR_SNS_TOPIC_ARN"


def lambda_handler(event, context):

    try:
        file_name = event['Records'][0]['s3']['object']['key']

        if not file_name.endswith(('.png', '.jpg', '.json', '.txt')):
            raise Exception("Invalid file type")

        data = {
            "file_id": file_name,
            "status": "processed",
            "timestamp": str(time.time())
        }

        table.put_item(Item=data)

        print("Processed:", file_name)

        return {"status": "success"}

    except Exception as e:

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Pipeline Error",
            Message=str(e)
        )

        print("Error:", str(e))
        raise e
