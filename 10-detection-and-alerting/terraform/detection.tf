resource "aws_cloudwatch_event_bus" "detection_lab" {
  name = "detection-lab"
}

resource "aws_cloudwatch_event_rule" "route_cloudtrail_events" {
  name           = "detection-lab-route-cloudtrail"
  description    = "Routes CloudTrail API events to the detection lab event bus."
  event_bus_name = "default"

  event_pattern = jsonencode({
    source = [
      "aws.iam"
    ]
    detail-type = [
      "AWS API Call via CloudTrail"
    ]
  })
}

resource "aws_cloudwatch_event_target" "detection_lab_bus" {
  rule           = aws_cloudwatch_event_rule.route_cloudtrail_events.name
  event_bus_name = "default"

  arn      = aws_cloudwatch_event_bus.detection_lab.arn
  role_arn = aws_iam_role.eventbridge_routing.arn
}

resource "aws_cloudwatch_event_rule" "iam_policy_change" {
  name           = "detection-lab-iam-policy-change"
  description    = "Detects IAM role policy changes."
  event_bus_name = aws_cloudwatch_event_bus.detection_lab.name

  event_pattern = jsonencode({
    source = [
      "aws.iam"
    ]
    detail-type = [
      "AWS API Call via CloudTrail"
    ]
    detail = {
      eventSource = [
        "iam.amazonaws.com"
      ]
      eventName = [
        "PutRolePolicy"
      ]
    }
  })
}

resource "aws_cloudwatch_event_target" "iam_policy_change" {
  rule           = aws_cloudwatch_event_rule.iam_policy_change.name
  event_bus_name = aws_cloudwatch_event_bus.detection_lab.name
  target_id      = "detection-handler"
  arn            = aws_lambda_function.detection_handler.arn
}
