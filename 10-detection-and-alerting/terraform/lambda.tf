resource "aws_cloudwatch_log_group" "detection_lambda" {
  name              = "/aws/lambda/detection-handler"
  retention_in_days = 7
}

data "archive_file" "detection_lambda_package" {
  type        = "zip"
  source_file = "../lambda/detection_handler.py"
  output_path = "detection_handler.zip"
}

resource "aws_lambda_function" "detection_handler" {
  function_name = "detection-handler"
  runtime       = "python3.12"
  handler       = "detection_handler.lambda_handler"
  role          = aws_iam_role.detection_lambda.arn

  filename         = data.archive_file.detection_lambda_package.output_path
  source_code_hash = data.archive_file.detection_lambda_package.output_base64sha256

  timeout       = 5
  memory_size   = 128
  architectures = ["arm64"]

  depends_on = [
    aws_cloudwatch_log_group.detection_lambda
  ]
}

resource "aws_lambda_permission" "eventbridge_iam_policy_change" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.detection_handler.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.iam_policy_change.arn
}
