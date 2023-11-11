output "data_bucket_name"{
  description="created data bucket"
  value=module.nc_project_init_bucket_module.s3_bucket_id
}