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
  arn            = aws_cloudwatch_event_bus.detection_lab.arn
}

resource "aws_cloudwatch_event_bus_policy" "allow_default_bus" {
  event_bus_name = aws_cloudwatch_event_bus.detection_lab.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowDefaultBusToRouteEvents"
        Effect = "Allow"
        Principal = {
          Service = "events.amazonaws.com"
        }
        Action   = "events:PutEvents"
        Resource = aws_cloudwatch_event_bus.detection_lab.arn
      }
    ]
  })
}
