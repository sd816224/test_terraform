# terraform apply --auto-approve \
# -var bucketname='only-for-testing2-'

# abc='hello'
# echo ${abc}

# if aws s3api get-object \
# --bucket nc-project-backend20231107140228968000000001 \
# --key production/terraform.tfstate \
#  test.json

# then
# echo $(jq '.check_results' test.json)
# else

# fi

echo $(jq '.resources[0].instances' test.json)