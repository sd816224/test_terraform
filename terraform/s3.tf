resource "aws_s3_bucket" "lambda_code_bucket" {
  bucket_prefix = "nc-de-project-lambda-code-bucket-"
}

resource "aws_s3_bucket" "ingestion_data_bucket" {
  bucket_prefix = "nc-de-project-ingested-data-bucket-"
}

resource "aws_s3_bucket" "transformed_data_bucket" {
  bucket_prefix = "nc-de-project-transformed-data-bucket-"
}

# Tagging? 


