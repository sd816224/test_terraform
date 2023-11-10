# data "aws_caller_identity" "current"{}

# data "aws_region" "current"{}

# data "archive_file" "ingestion_lambda_code_zip" {
#   type        = "zip"
#   source_file = "${path.module}/../src/ingestion_lambda/ingestion_lambda.py"
#   output_path = "${path.module}/../src/ingestion_lambda/ingestion_lambda.zip"
# }


# resource "aws_s3_object" "ingestion_lambda_code_upload" {
#   bucket = aws_s3_bucket.lambda_code_bucket.id
#   key    = "ingestion_lambda/ingestion_lambda.zip"
#   source = data.archive_file.ingestion_lambda_code_zip.output_path
#   source_hash = filemd5(data.archive_file.ingestion_lambda_code_zip.output_path)
# }

