import boto3
import os
import json

from typing import Dict, Any

sns = boto3.resource("sns")
topic = sns.Topic(os.getenv("SNS_TOPIC"))


def lambda_handler(event: Dict[str, Any], context):
    approval_state = event.get("detail", {}).get("state")
    print(json.dumps(event))
    if approval_state == "STARTED":
        print("CodePipeline Approval Requested and Waiting")
        notification = {
            "version": "1.0",
            "source": "custom",
            "content": {
                "textType": "client-markdown",
                "description": f"@here CodePipeline '{event['detail']['pipeline']}' Stage '{event['detail']['stage']}' is awaiting approval.",
            },
            "metadata": {
                "threadId": event["detail"]["execution-id"],
                "additionalContext": {
                    "pipeline": event["detail"]["pipeline"],
                    "stage": event["detail"]["stage"],
                    "action": event["detail"]["action"],
                },
            },
        }
        topic.publish(Message=json.dumps(notification))
        return
    if approval_state == "SUCCEEDED":
        print("CodePipeline Approval Request Approved")
        return
    if approval_state == "FAILED":
        print("CodePipeline Approval Request Rejected")
        return
