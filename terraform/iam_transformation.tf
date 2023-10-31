resource "aws_iam_role" "role_for_transformation_lambda" {
  name               = "role_for_transformation_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "cloudwatch_logs_policy_for_transformation_lambda" {
  name        = "transformation_lambda_cloudwatch_logs_policy"
  description = "Allows transformation lambda to write logs to cloudwatch"
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
        resources = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.transformation_lambda}:*"
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "transformation_lambda_cw_policy_attachment" {
  policy_arn = aws_iam_policy.cloudwatch_logs_policy_for_transformation_lambda.arn
  role = aws_iam_role.role_for_warehouse_transformation_lambda.name
}