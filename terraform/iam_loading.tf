resource "aws_iam_role" "role_for_warehouse_loading_lambda" {
  name               = "role_for_warehouse_loading_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "cloudwatch_logs_policy_for_loading_lambda" {
  name        = "loading_lambda_cloudwatch_logs_policy"
  description = "Allows loading lambda to write logs to cloudwatch"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        actions   = "logs:CreateLogGroup",
        effect   = "Allow",
        resources = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
      },
      {
        actions   = ["logs:CreateLogStream","logs:PutLogEvents"]
        effect   = "Allow",
        resources = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.warehouse_loading_lambda}:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "loading_cw_policy_attachment" {
  policy_arn = aws_iam_policy.cloudwatch_logs_policy_for_loading_lambda.arn
  role = aws_iam_role.role_for_warehouse_loading_lambda.name
}

# resource "aws_iam_policy" "warehouse_loading_lambda_s3_policy" {
#   name        = "warehouse_loading_lambda_s3_policy"
#   description = "Allows reading from tranformed data bucket and writing to ingestion data bucket"
#   policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         actions = "s3:GetObject",
#         effect = "Allow",
#         resources = "${aws_s3_bucket.transformed_data_bucket.arn}/*" # ??
#       },
#       {
#         ######################## ToDo: this needs to be permission to write to warehouse db
#         actions = "s3:PutObject",
#         effect = "Allow",
#         resources = "${aws_s3_bucket.ingestion_data_bucket.arn}/*",
#       },
#     ]
#   })
# }