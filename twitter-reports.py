#samdesk-alerts

from slack_sdk import WebClient
import os
import json

def main():
    # Read the environment variables
    slack_token = os.environ["SLACK_API_TOKEN"]
    slack_channel = os.environ["SLACK_CHANNEL"]
    slack_username = os.environ["SLACK_USERNAME"]
    
    # Create a WebClient for sending messages to Slack
    slack_client = WebClient(token=slack_token)

    def read_slack_messages():
        # Read the messages from the Slack channel
        response = slack_client.channels_history(channel=slack_channel, count=1)
        messages = response["messages"]
        if len(messages) == 0:
            return None
        return messages[0]
    