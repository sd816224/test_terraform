# resource "aws_cloudwatch_event_rule" "event_bridge_invoke_ingestion_lambda_rule" {
#   name                = "invoke-ingestion-lambda-from-event-bridge"
#   schedule_expression = "rate(10 minutes)"
# }

# resource "aws_cloudwatch_event_target" "ingestion_lambda_event_target" {
#   rule = aws_cloudwatch_event_rule.event_bridge_invoke_ingestion_lambda_rule.name
#   arn  = aws_lambda_function.ingestion_lambda.arn
# }




variable  "ingestiontrigger"{
    type=string
}

resource "aws_scheduler_schedule" "ingestion_trigger" {
  name = "ingestion_trigger"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "rate(1 minutes)"

  target {
    arn      = "arn:aws:scheduler:::aws-sdk:sqs:sendMessage"
    role_arn = aws_iam_role.role_for_ingestion_lambda.arn
    input = var.ingestiontrigger
  }
}

resource "aws_lambda_permission" "allow_scheduler" {
  statement_id   = "AllowExecutionFromEventBridge"
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.ingestion_lambda.function_name
  principal      = "events.amazonaws.com"
  source_arn     = aws_scheduler_schedule.ingestion_trigger.arn
}