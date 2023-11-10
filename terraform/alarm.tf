# resource "aws_sns_topic" "log_notification_topic" {
#   name = "nc-de-project-pipeline-log-topic"
# }

# resource "aws_sns_topic_subscription" "email_subscription" {
#   topic_arn = aws_sns_topic.log_notification_topic.arn
#   protocol  = "email"
#   endpoint  = "nc404namenotfound@gmail.com"
# }


# resource "aws_cloudwatch_log_metric_filter" "warning_metrics_filter_ingest" {
#   name           = "ingestion-log-warning-filter"
#   pattern        = "WARNING"
#   log_group_name = "/aws/lambda/${aws_lambda_function.ingestion_lambda.function_name}"

#   metric_transformation {
#     name      = "ingestion-warning-log-count"
#     namespace = "IngestionMetrics"
#     value     = "1"
#   }
# }
# resource "aws_cloudwatch_log_metric_filter" "error_metric_filter_ingest" {
#   name           = "ingestion-log-error-filter"
#   pattern        = "ERROR"
#   log_group_name = "/aws/lambda/${aws_lambda_function.ingestion_lambda.function_name}"
  
#   metric_transformation {
#     name      = "ingestion-error-log-count"
#     namespace = "IngestionMetrics"
#     value     = "1"
#   }
# }
# resource "aws_cloudwatch_log_metric_filter" "runtime_error_ingest" {
#   name           = "IngestionRuntimeError"
#   pattern        = "RuntimeError"
#   log_group_name = "/aws/lambda/${aws_lambda_function.ingestion_lambda.function_name}"

#   metric_transformation {
#     name      = "ingestion-runtime-log-count"
#     namespace = "IngestionMetrics"
#     value     = "1"
#   }
# }

