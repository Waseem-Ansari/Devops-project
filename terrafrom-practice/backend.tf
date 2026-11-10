terraform {
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 5.0"
        }
    }

    backend "s3" {
        bucket   = "waseem-tf-state-2026"
        key      = "practice/terraform.tfstate"
        region   = "ap-south-1"
        dynamodb_table = "terraform-locks"
        encrypt = true
    }
}