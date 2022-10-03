from slack_sdk.webhook import WebhookClient
import dateutil.parser
import os
import json
import requests
import re


def slack_handler(event, context):
    # Set and log environment variables for both Slack webhook URL and RSC tenant
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    rsc_tenant_url = os.environ['RSC_TENANT_URL']

    # Verify environment variables have been set
    if slack_webhook_url and rsc_tenant_url:
        print(f'Slack webhook URL set to {slack_webhook_url}')
        print(
            f'Rubrik Security Cloud tenant URL set to {rsc_tenant_url}')
    else:
        print(
            f'Environment variables not set correctly, please review RSC and Slack webhook settings')

    # Check the RSC URL is reachable
    rsc_url_status = requests.get(rsc_tenant_url)
    if rsc_url_status.status_code != 200:
        print(
            f'RSC tenant URL does not seem to be responding, please check the environment variable')

    # Validate the Slack webhook URL is the correct syntax using RegEx
    slack_webhook_url_check = re.search(
        "https://hooks.slack.com/services/T[0-9A-Z]{10}/B[0-9A-Z]{10}/[a-zA-Z0-9]{24}", slack_webhook_url)
    if slack_webhook_url_check:
        print(f'Slack URL appears to be correctly formed')
    else:
        print(
            f'Slack URL appears to be malformed - please check and remediate')

    rsc_event_payload = event.get('body')
    rsc_event_payload_dict = json.loads(rsc_event_payload)

    if rsc_event_payload_dict:
        print(f'Finding alert summary content is - {rsc_event_payload_dict}')
        alert_summary = rsc_event_payload_dict['summary']
        alert_severity = rsc_event_payload_dict['severity']
        alert_timestamp = rsc_event_payload_dict['timestamp']
        alert_class = rsc_event_payload_dict['class']
        alert_event_id = rsc_event_payload_dict['custom_details']['seriesId']
        alert_object_name = rsc_event_payload_dict['custom_details']['objectName']
        alert_object_type = rsc_event_payload_dict['custom_details']['objectType']
        alert_cluster_id = rsc_event_payload_dict['custom_details']['clusterId']
        alert_formatted_timestamp = dateutil.parser.parse(alert_timestamp)
        alert_display_timestamp = alert_formatted_timestamp.ctime()
        review_findings_url = rsc_tenant_url + "/events"
        print(f'Building Slack message...')
        slack_webhook = WebhookClient(slack_webhook_url)
        slack_webhook_response = slack_webhook.send(
            blocks=[
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                    "text": {
                            "type": "plain_text",
                            "text": "Rubrik Security Cloud " + alert_severity + " severity event notification - Lambda",
                        "emoji": True
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":bell: *Event Information*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Event summary_* :\t" + alert_summary
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Severity_* :\t" + alert_severity
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Type_* :\t" + alert_class
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Event ID_* :\t" + alert_event_id
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Object Name_* :\t" + alert_object_name
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Object Type_* :\t" + alert_object_type
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Cluster ID_* :\t" + alert_cluster_id
                    }
                },
                {
                    "type": "section",
                    "text": {
                            "type": "mrkdwn",
                            "text": "*_Time_* :\t" + alert_display_timestamp
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":mag: *Recent events can be viewed in a browser by clicking the button*"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Latest Events",
                            "emoji": True
                        },
                        "value": "recent_events",
                        "url": review_findings_url,
                        "action_id": "button-action"
                    }
                },
                {
                    "type": "divider"
                }
            ]
        )
        print(f'Slack message sent successfully ')
    else:
        print(f'Empty message payload recieved ')
