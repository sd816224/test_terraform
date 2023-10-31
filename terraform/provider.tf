terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.21.0"
    }
  }

  backend "s3" {
    bucket = "nc-de-project-backend-bucket"
    key    = "production/terraform.tfstate" 
    region = "eu-west-2"
  }
}

provider "aws" {
  region  = "eu-west-2"
}


# could specify key = "production/terraform.tfstate" 
# if we wanted to use the same bucket for test/ state
# probably don't need this. 