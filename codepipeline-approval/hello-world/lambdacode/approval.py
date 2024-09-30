from typing import Dict
import boto3

codepipeline = boto3.client("codepipeline")


def lambda_handler(event: Dict[str, str], context):
    approval: str = event.get("approval")

    if approval not in ["Approved", "Rejected"]:
        return "Approval state must be either Approved or Rejected"

    pipeline_name: str = event["pipeline"]
    stage_name: str = event["stage"]
    action_name: str = event["action"]

    pipeline_state = codepipeline.get_pipeline_state(name=pipeline_name)
    token: str
    for stage in pipeline_state["stageStates"]:
        if stage["stageName"] != stage_name:
            continue
        for action in stage["actionStates"]:
            if action["actionName"] != action_name:
                continue
            token = action["latestExecution"]["token"]
            break

    codepipeline.put_approval_result(
        pipelineName=pipeline_name,
        stageName=stage_name,
        actionName=action_name,
        result={
            "summary": f"Execution was {approval.lower()} through Slack ChatBot",
            "status": approval,
        },
        token=token,
    )
    return f"Pipeline approval action for {pipeline_name} was {approval}"
