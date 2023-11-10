module "nc_project_init_bucket_module"{
  source="terraform-aws-modules/s3-bucket/aws"

  bucket_prefix="data-bucket-iii"

  output=
}
