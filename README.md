# Rubrik Security Cloud Slack Connector (AWS Lambda version)

## What does it do?

This connector runs as a Lambda Function and provides a webhook URL for Rubrik Security Cloud (RSC, formerly Polaris) to send alerts to. This provides simple connectivity to Slack as it sends alert information as BlockKit formatted messages into a Slack channel.

![alt text](https://github.com/chrisbeckett/rbk-slack-webhook-lambda/blob/main/slack-event.png "Slack screenshot")

## How does it work?

Create a new webhook in the RSC "Security Settings" page (can be accessed via the gear icon in the top right hand corner) and filter out the required events and severity. For example, to send backup operations events to Slack, you may wish to select the "Backup", "Diagnostic", "Maintenance" and "System" event types with the "Critical" and "Warning" severities.

Product documentation can be found at https://docs.rubrik.com/en-us/saas/saas/common/webhooks.html.

![alt text](https://github.com/chrisbeckett/rbk-slack-webhook-lambda/blob/main/slack-connector-architecture.png "Architecture overview")

## What do I need to get started?

- An RSC tenant (including URL, e.g. myorg.my.rubrik.com)
- A Slack account
- A Slack channel to send alerts to
- An incoming Slack webhook URL (https://api.slack.com/messaging/webhooks)
- Python 3.7/3.8/3.9 (3.10 is not currently supported by Azure Functions)
- Git
- AWS command line tools
- Terraform

## Obtaining the code

Run **git clone https://github.com/chrisbeckett/rbk-slack-webhook-lambda.git**

## Deploying the Lambda Function - Quick Start

The quickest way to deploy the function is to use the Terraform files provided in the /terraform folder. Simply update the **variables.tf** file to reflect your preferences around function names, AWS region to deploy etc. Pay special attention to the environment variables. If these are not configured properly, installation will fail.

For example, change the variables file to deploy your function to **EU West 1 (Ireland)**

```
terraform {
required_providers {
aws = {
source = "hashicorp/aws"
version = "=4.33.0"
}
}
}

# Variables

variable "lambda_function_name" {
description = "AWS Lambda function name"
default = "rbk-slack-webhook-tf1"
}

variable "description" {
description = "Function description"
default = "Rubrik Slack webhook handler"
}

variable "region" {
description = "AWS region"
default = "eu-west-1"
}
```

Also, make sure that your RSC tenant and Slack webhook URLs are correctly added to the **create_lambda_function.tf** file

```
environment_variables = {
    RSC_TENANT_URL    = "https://acme-corp.my.rubrik.com"
    SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/TXXXXXXX/BXXXXXXX/XXXXXXXXXXXXX"
  }
```

**Known Issue** You may need to run **terraform apply** twice in order to generate the Function URL.

## Creating the RSC webhook

Take the Function URL (e.g. https://xxxxxxxxx.lambda-url.eu-west-1.on.aws) created by the Terraform template (Lambda function | Configuration | Function URL) and add it to your RSC webhook target configuration

![alt text](https://github.com/chrisbeckett/rbk-slack-webhook-lambda/blob/main/aws-function-url.png "Lambda Function URL")

**In RSC :-**

![alt text](https://github.com/chrisbeckett/rbk-slack-webhook-lambda/blob/main/webhook-url.png "RSC webhook target URL")
