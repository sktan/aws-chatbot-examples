from aws_cdk import Stack, aws_chatbot as chatbot, aws_sns as sns, aws_lambda as lambda_
from constructs import Construct


class ChatBot(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Start Chatbot Minimum Requirements
        chatbot_sns = sns.Topic(self, "test_chatbot_sns")
        slack_channel = chatbot.SlackChannelConfiguration(
            self,
            id="my_slack_channel",
            slack_channel_configuration_name="test",
            # Your Slack Workspace ID when viewing it via the web-browser and starts with T
            slack_workspace_id="T0123456789",
            # Your Slack Channel ID (use the copy channel link and it's the segment that starts with C)
            slack_channel_id="C0123456789",
        )
        slack_channel.add_notification_topic(chatbot_sns)
        # End Chatbot Minimum Requirements

        # Test Lambda (Hello Name)
        with open("lambdacode/test.py", "r") as f:
            test_lmabda_code = f.read()
        test_lambda = lambda_.Function(
            self,
            "test-lambda",
            code=lambda_.Code.from_inline(test_lmabda_code),
            handler="index.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
        )

        test_lambda.grant_invoke(slack_channel)
        # Test Lambda (Hello Name)
