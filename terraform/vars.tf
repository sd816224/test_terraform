variable "ingestion_lambda" {
  type    = string
  default = "ingestion_lambda"
}

variable "transformation_lambda" {
  type    = string
  default = "transformation_lambda"
}

variable "warehouse_loading_lambda" {
  type    = string
  default = "warehouse_loading_lambda"
}