from typing import Dict


def lambda_handler(event: Dict[str, str], context):
    return f"hello, {event.get('name', 'anonymous')}"
