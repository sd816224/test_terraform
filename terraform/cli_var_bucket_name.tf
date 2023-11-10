
variable  "bucketname"{
    type=string
}


resource "aws_s3_bucket" "testing_bucket" {
  bucket_prefix = var.bucketname
}

