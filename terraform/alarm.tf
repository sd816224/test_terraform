resource "aws_sns_topic" "log_notification_topic" {
  name = "nc-de-project-pipeline-log-topic"
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.log_notification_topic.arn
  protocol  = "email"
  endpoint  = "nc404namenotfound@gmail.com"
}


resource "aws_cloudwatch_log_metric_filter" "warning_metrics_filter" {
  name           = "ingestion-log-warning-filter"
  pattern        = "WARNING"
  log_group_name = "/aws/lambda/${aws_lambda_function.ingestion_lambda.function_name}"

  metric_transformation {
    name      = "warning-log-count"
    namespace = "IngestionMetrics"
    value     = "1"
  }
}

resource "aws_cloudwatch_log_metric_filter" "error_metric_filter" {
  name           = "ingestion-log-error-filter"
  pattern        = "ERROR"
  log_group_name = "/aws/lambda/${aws_lambda_function.ingestion_lambda.function_name}"
  
  metric_transformation {
    name      = "error-log-count"
    namespace = "IngestionMetrics"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "error_alert" {
  alarm_name          = "ingestion-error"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = aws_cloudwatch_log_metric_filter.error_metric_filter.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.error_metric_filter.metric_transformation[0].namespace
  period              = 600
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "This metric monitors number of errors coming from the Ingestion Lambda in ten minute intervals"
  alarm_actions       = [aws_sns_topic.log_notification_topic.arn]
}

resource "aws_cloudwatch_metric_alarm" "warning_alert" {
  alarm_name          = "ingestion-warning"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = aws_cloudwatch_log_metric_filter.warning_metrics_filter.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.warning_metrics_filter.metric_transformation[0].namespace
  period              = 600
  statistic           = "Sum"
  threshold           = 2
  alarm_description   = "This metric monitors number of warnings coming from the Ingestion Lambda in ten minute intervals"
  alarm_actions       = [aws_sns_topic.log_notification_topic.arn]

}

resource "aws_cloudwatch_log_metric_filter" "runtime_error" {
  name           = "RuntimeError"
  pattern        = "RuntimeError"
  log_group_name = "/aws/lambda/${aws_lambda_function.ingestion_lambda.function_name}"

  metric_transformation {
    name      = "runtime-log-count"
    namespace = "IngestionMetrics"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "runtime_alert" {
  alarm_name          = "RuntimeAlarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = aws_cloudwatch_log_metric_filter.runtime_error.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.runtime_error.metric_transformation[0].namespace
  period              = 600
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "This metric monitors for runtime errors"
  alarm_actions       = [aws_sns_topic.log_notification_topic.arn]

}

# #####Needs attention in regards to the namespace 

# resource "aws_cloudwatch_metric_alarm" "duration_alert" {
#   alarm_name          = "DurationAlarm"
#   comparison_operator = "GreaterThanOrEqualToThreshold"
#   evaluation_periods  = 1
#   metric_name         = "Duration"
#   namespace           = "AWS/Lambda/Ingestion"
#   statistic           = "Average"
#   period              = 10
#   threshold           = 1000
#   alarm_description   = "This metric monitors function execution duration"
#   alarm_actions       = [aws_sns_topic.log_notification_topic.arn]
# }

# #######^^^^^^^^^^^^^^^^^^^





# How to link this to cloudwatch policy????
# NOTES:
# One topic for the whole pipeline and different lambdas and log severity levels should be sufficient.
# Look into different protocols and endpoints: Slack? Dashboard? API?
# DEBUG - Detailed information, typically of interest only when diagnosing problems.
# INFO - Confirmation that things are working as expected.
# WARNING - An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
# ERROR - Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL - A serious error, indicating that the program itself may be unable to continue running.