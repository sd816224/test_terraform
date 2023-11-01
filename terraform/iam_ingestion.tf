resource "aws_iam_role" "role_for_ingestion_lambda" {
  name               = "role_for_ingestion_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_policy" "cloudwatch_logs_policy_for_ingestion_lambda" {
  name        = "ingestion_lambda_cloudwatch_logs_policy"
  description = "Allows ingestion lambda to write logs to cloudwatch"
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
        resources = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.ingestion_lambda}:*"
      }
    ]
  })
}

resource "aws_iam_policy" "ingestion_lambda_s3_policy" {
  name        = "ingestion_lambda_s3_policy"
  description = "Allows reading from code bucket and writing to ingestion data bucket"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        actions = "s3:GetObject",
        effect = "Allow",
        resources = "${aws_s3_bucket.lambda_code_bucket.arn}/*" # ??
      },
      {
        actions = "s3:PutObject",
        effect = "Allow",
        resources = "${aws_s3_bucket.ingestion_data_bucket.arn}/*",
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ingestion_lambda_cw_role_attachment" {
  role       = aws_iam_role.role_for_ingestion_lambda.name
  policy_arn = aws_iam_policy.cloudwatch_logs_policy_for_ingestion_lambda.arn
}

resource "aws_iam_role_policy_attachment" "ingestion_lambda_s3_policy_attachment" {
  role       = aws_iam_role.role_for_ingestion_lambda.name
  policy_arn = aws_iam_policy.ingestion_lambda_s3_policy.arn
}


# separate dirs for each lambda logs? Log groups?
