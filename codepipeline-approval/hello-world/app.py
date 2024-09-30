#!/usr/bin/env python3

import aws_cdk as cdk

from stacks.chatbot import ChatBot


app = cdk.App()

chatbot_stack = ChatBot(
    app,
    "sktan-chatbot",
    env=cdk.Environment(account="123456789012", region="ap-southeast-2"),
)

app.synth()
