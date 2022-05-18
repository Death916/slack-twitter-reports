#samdesk-alerts

from asyncore import read
from gzip import READ
import re
from slack_sdk import WebClient
import os
import json

def main():
    # Read the environment variables
    SLACK_TOKEN = os.environ["SLACK_API_TOKEN"]
    SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]
    
    
    # Create a WebClient for sending messages to Slack
    slack_client = WebClient(token=SLACK_TOKEN)

    class slack():
        def __init__(self, slack_client, SLACK_CHANNEL, SLACK_USERNAME):
            self.slack_client = slack_client
            self.SLACK_CHANNEL = SLACK_CHANNEL
            

        
        def read_messages():
            # Read the messages from the Slack channel
            response = slack_client.conversations_list()
            channel = response["channels"]
          
            print(messages)

            return messages[0]
        
    slack.read_messages()


    class twitter(): 
        # Read the environment variables

        #search for headlines
        def search_headlines(self):
            pass

if __name__ == "__main__":
    main()