# Welcome to my AWS Chatbot Examples Repository

In this repository, I will be providing working code samples used for my "Building witgh AWS Chatbot" blog series.

This will include both infrastructure as code (CDK) and the lambda function code so that deployment is as simple as possible.

## Pre-Requisites

1. Python 3.12
2. NodeJS (Any LTS Version)
3. AWS CDK

## Blog Series:

| Blog Post  | Code Reference |
| ------------- | ------------- |
| [Building with AWS Chatbot: Saying Hello to AWS Chatbot](https://www.sktan.com/blog/post/12-building-with-aws-chatbot-saying-hello-to-aws-chatbot/)  | Content Cell  |
| [Building with AWS Chatbot: Approving CodePipeline Executions Through ChatOps](https://www.sktan.com/blog/post/13-building-with-aws-chatbot-approving-codepipeline-executions-through-chatops/)  | Content Cell  |


## How to Deploy

1. Replace `env=cdk.Environment(account="123456789012", region="ap-southeast-2"),` in `app.py` with your AWS Account Id
2. Replace your slack workspace and channel id in `stacks/chatbot.py` with your own [by using these instructions](https://slack.com/intl/en-au/help/articles/221769328-Locate-your-Slack-URL-or-ID)
3. Run `pipenv sync` to install the requirements
4. Run `cdk deploy` to deploy the stack
