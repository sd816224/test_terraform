
variable  "tfstate_trigger"{
    type=string
    # default = "bucket-iii"
}

resource "aws_cloudwatch_event_rule" "event_bridge_invoke_ingestion_lambda_rule" {
  name                = "invoke-ingestion-lambda-from-event-bridge"
  schedule_expression = "cron(0/1 * * * ? *)"
}

resource "aws_cloudwatch_event_target" "ingestion_lambda_event_target" {
  rule = aws_cloudwatch_event_rule.event_bridge_invoke_ingestion_lambda_rule.name
  arn  = aws_lambda_function.ingestion_lambda.arn
  input =jsonencode({
    input_template = var.tfstate_trigger
  }) 
}

resource "aws_lambda_permission" "allow_scheduler" {
  statement_id   = "AllowExecutionFromEventBridge"
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.ingestion_lambda.function_name
  principal      = "events.amazonaws.com"
  source_arn     = aws_cloudwatch_event_rule.event_bridge_invoke_ingestion_lambda_rule.arn
}

