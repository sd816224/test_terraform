resource "aws_lambda_function" "ingestion_lambda" {
  function_name    = var.ingestion_lambda
  # handler          = "reader.lambda_handler" 
  runtime          = "python3.11"
  role             = aws_iam_role.role_for_lambda.arn
  s3_bucket        = aws_s3_bucket.lambda_code_bucket.id
  # s3_key           = "function.zip"
  # layers        = []
  source_code_hash = data.archive_file.lambda.output_base64sha256
  # depends_on = [aws_lambda_layer_version.ingestion_layer] 
}

# ingetion  function handler name?
# code zip ?
# layer zip?
# make sure the layer resource is created first then create lambda.
