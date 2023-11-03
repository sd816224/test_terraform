# resource "aws_lambda_function" "warehouse_loading_lambda" {
#     function_name    = var.warehouse_loading_lambda
#     handler          = "loading_lambda.lambda_handler" 
#     runtime          = "python3.11"
#     role             = aws_iam_role.role_for_warehouse_loading_lambda.arn
#     s3_bucket        = aws_s3_bucket.lambda_code_bucket.id
#     s3_key           = "loading_lambda/loading_lambda.zip"
#     layers        = []
#     source_code_hash = data.archive_file.loading_lambda_code_zip.output_base64sha256
#     # depends_on = [***layer***]
# }