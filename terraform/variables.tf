terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "=4.33.0"
    }
  }
}

# Variables

variable "lambda_function_name" {
  description = "AWS Lambda function name"
  default     = "rbk-slack-webhook-tf1"
}

variable "description" {
  description = "Function description"
  default     = "Rubrik Slack webhook handler"
}

variable "region" {
  description = "AWS region"
  default     = "eu-west-1"
}

