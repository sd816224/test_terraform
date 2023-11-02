# resource "aws_lambda_function" "warehouse_loading_lambda" {
#   function_name    = var.warehouse_loading_lambda
#   # handler          = "reader.lambda_handler" 
#   # runtime          = "python3.11"
#   role             = aws_iam_role.role_for_warehouse_loading_lambda.arn
#   # s3_bucket        = aws_s3_bucket.lambda_code_bucket.id
#   # s3_key           = "function.zip"
#   # layers        = []
#   #source_code_hash = data.archive_file.lambda.output_base64sha256
#   # depends_on = [aws_lambda_layer_version.ingestion_layer] 
# }