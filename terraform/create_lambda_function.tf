module "lambda_function_existing_package_local" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = var.lambda_function_name
  description   = var.description
  handler       = "handler.slack_handler"
  runtime       = "python3.9"
  environment_variables = {
    RSC_TENANT_URL    = "https://myorg.my.rubrik.com"
    SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/TXXXXXXX/BXXXXXXX/XXXXXXXXXXXXX"
  }

  create_package         = false
  local_existing_package = "../rubrik-slack-handler-package.zip"

  ignore_source_code_hash = true

}

provider "aws" {
  region = var.region
}
resource "aws_lambda_function_url" "slack_handler_url" {
  function_name      = var.lambda_function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = ["*"]
    allow_methods     = ["*"]
    allow_headers     = ["date", "keep-alive"]
    expose_headers    = ["keep-alive", "date"]
    max_age           = 86400
  }
}
