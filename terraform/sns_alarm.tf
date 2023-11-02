# resource "aws_sns_topic" "log_notification_topic" {
#   name = "nc-de-project-pipeline-log-topic"
# }

# resource "aws_sns_topic_subscription" "email_subscription" {
#   topic_arn = aws_sns_topic.log_notification_topic.arn
#   protocol  = "email"
#   endpoint  = "my@email.com"
# }

# resource "aws_cloudwatch_log_metric_filter" "error_metric_filter" {
#   name           = "lambda-log-error-filter"
#   pattern        = "[ERROR]"
#   # log_group_name = aws_cloudwatch_log_group.ingestion_log_group.name ### ?
#   log_group_name = "/aws/lambda/ingestion_lambda" #?

#   metric_transformation {
#     name      = "error-log-count"
#     namespace = "Namespace" #?
#     value     = "1"
#   }
# }
# # Same shit as above for different levels of logs. see python log levels below.

# resource "aws_cloudwatch_metric_alarm" "error_alarm" {
#   alarm_name          = "error-log-alarm"
#   comparison_operator = "GreaterThanOrEqualToThreshold"
#   evaluation_periods = 1
#   metric_name        = "error-log-count" # reference to above metric_transfomation
#   namespace           = "Namespace"      # reference to above metric_transfomation
#   period             = 3600  # 1 hour
#   statistic           = "SampleCount"
#   threshold           = 10   # Adjust this threshold as needed
#   alarm_description   = "Notify when there are lambda error logs"
#   alarm_actions       = [aws_sns_topic.log_notification_topic.arn] # ref to topic
#   dimensions = {
#     LogGroupName = aws_cloudwatch_log_group.ingestion_log_group.name # again a path or a resource here?
#   }
# }

# resource "aws_cloudwatch_log_group" "ingestion_log_group" {
#   name = "/aws/lambda/ingestion-lambda"
# }

# How to link this to cloudwatch policy????

# NOTES:

# Do we need to create separate resources for log groups or can just use a path?
# One topic for the whole pipeline and different lambdas and log severity levels should be sufficient.
# Look into different protocols and endpoints: Slack? Dashboard? API?

# DEBUG - Detailed information, typically of interest only when diagnosing problems.
# INFO - Confirmation that things are working as expected.

# WARNING - An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
# ERROR - Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL - A serious error, indicating that the program itself may be unable to continue running.