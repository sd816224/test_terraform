# resource "aws_lambda_function" "transformation_lambda" {
#   function_name    = var.transformation_lambda
#   handler          = "transformation_lambda.lambda_handler" 
#   runtime          = "python3.11"
#   role             = aws_iam_role.role_for_transformation_lambda.arn
#   s3_bucket        = aws_s3_bucket.lambda_code_bucket.id
#   s3_key           = "transformation_lambda/transformation_lambda.zip"
#   layers        = []
#   source_code_hash = data.archive_file.transformation_lambda_code_zip.output_base64sha256
#   # depends_on = [***layer***] 
# }