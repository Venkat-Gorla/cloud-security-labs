import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Log a compact security detection event received from EventBridge."""
    detail = event.get("detail", {})
    user_identity = detail.get("userIdentity", {})

    detection = {
        "detection": "iam-policy-change",
        "event_name": detail.get("eventName"),
        "principal": user_identity.get("arn"),
        "event_id": detail.get("eventID"),
    }

    logger.info(json.dumps(detection))

    return {"status": "processed"}
