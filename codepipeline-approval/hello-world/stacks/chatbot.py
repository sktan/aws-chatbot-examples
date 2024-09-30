from aws_cdk import (
    Stack,
    aws_chatbot as chatbot,
    aws_sns as sns,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_events as events,
    aws_events_targets as targets,
)
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

        # Eventbridge To Slack
        with open("lambdacode/pipeline.py", "r") as f:
            test_lmabda_code = f.read()
        pipeline_lambda = lambda_.Function(
            self,
            "eventdump-lambda",
            code=lambda_.Code.from_inline(test_lmabda_code),
            handler="index.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            environment={"SNS_TOPIC": chatbot_sns.topic_arn},
        )
        chatbot_sns.grant_publish(pipeline_lambda)

        events.Rule(
            self,
            "eventdump-rule",
            event_pattern=events.EventPattern(
                source=["aws.codepipeline"],
                detail_type=["CodePipeline Action Execution State Change"],
                detail={
                    "type": {
                        "owner": ["AWS"],
                        "provider": ["Manual"],
                        "category": ["Approval"],
                    }
                },
            ),
            targets=[targets.LambdaFunction(pipeline_lambda)],
        )
        # Eventbridge To Slack

        # Pipeline Approval Lambda
        with open("lambdacode/approval.py", "r") as f:
            approval_lambda_code = f.read()
        approval_lambda = lambda_.Function(
            self,
            "approval-lambda",
            code=lambda_.Code.from_inline(approval_lambda_code),
            handler="index.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
        )
        approval_lambda.add_to_role_policy(
            statement=iam.PolicyStatement(
                actions=[
                    "codepipeline:GetPipelineState",
                    "codepipeline:PutApprovalResult",
                ],
                resources=["*"],
            )
        )
        approval_lambda.grant_invoke(slack_channel)
        # Pipeline Approval Lambda
