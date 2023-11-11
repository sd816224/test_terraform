# terraform apply --auto-approve \
# -var bucketname='only-for-testing2-'

# abc='hello'
# echo ${abc}

# if aws s3api get-object \
# --bucket nc-project-backend20231107140228968000000001 \
# --key production/terraform.tfstate \
#  instances.json

# then
# echo $(jq '.check_results' test.json)
# else

# fi

# echo $(jq '.resources[0].instances' test.json)


# terraform apply -target=module.nc_project_init_bucket_module --auto-approve 

#### checn json variable exist
# xxx=$(jq '.resources[0].instances' emptytf.json)
# echo "$xxx"

# if [jq -e . >/dev/null 2>&1 <<<"$xxx"] ; then
#     echo "Parsed JSON successfully and got something other than false/null"
# else
#     echo "Failed to parse JSON, or got false/null"
# fi

# echo $(jq '.resources[0].instances' emptytf.json) 


####check if document exist

# if aws s3api get-object \
# --bucket nc-project-backend20231107140228968000000001 \
# --key production/terraform.tfstate \
#  instances.json
# then 
#     xxx=$(jq '.resources[0].instances' instances.json)
#     if [jq -e . >/dev/null 2>&1 <<<"$xxx"] ; then
#         echo "bucket created already, instances file is ready"
#     else
#         echo 'create bucket here:'
#         terraform apply -target=module.nc_project_init_bucket_module --auto-approve 
#     fi
# else 
# terraform init
# terraform apply -target=module.nc_project_init_bucket_module --auto-approve 
# fi

# terraform apply -target=module.nc_project_init_bucket_module -auto-approve 
# aws s3api get-object \
# --bucket nc-project-backend20231107140228968000000001 \
# --key production/terraform.tfstate \
#  instances.json


# cat ./test.json

# terraform apply -auto-approve \
# -var ingestiontrigger='data-bucket-iii20231110162329077800000001'

terraform apply -target=module.nc_project_init_bucket_module --auto-approve 