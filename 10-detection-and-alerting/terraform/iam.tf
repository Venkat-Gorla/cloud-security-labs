resource "aws_iam_role" "detection_lab" {
  name = "detection-lab-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "detection_lab" {
  name = "detection-lab-policy"
  role = aws_iam_role.detection_lab.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject"]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role" "eventbridge_routing" {
  name = "detection-lab-eventbridge-routing-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "events.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "eventbridge_routing" {
  name = "detection-lab-eventbridge-routing-policy"
  role = aws_iam_role.eventbridge_routing.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "events:PutEvents"
        Resource = aws_cloudwatch_event_bus.detection_lab.arn
      }
    ]
  })
}
