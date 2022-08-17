#samdesk-alerts

import time
import os
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import make_report as mr


# Read the environment variables
SLACK_TOKEN = os.environ["SLACK_API_TOKEN"]
SLACK_ALERT_SOCKET = os.environ["SLACK_ALERT_SOCKET"]

# Install the Slack app and get xoxb- token in advance
app = App(token=SLACK_ALERT_SOCKET)
 
CURRENT_MESSAGE = ""
LOOP = 0

def main():
    new_message = handle_message_events(app)
    parse_message(new_message)



# Listen for incoming messages
@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)
    message = body["event"]["text"]
    
    # Get the channel ID
    event_id = body.get("event_id")

    print(message)
    print(event_id)
    print("here")
    
    # store message id for title
    report = mr.samreport(time.asctime() + ".txt")
    # store message in report file
    report.raw_alert(message)
    CURRENT_MESSAGE = message
    return(CURRENT_MESSAGE)


def parse_message(CURRENT_MESSAGE):
   
    print("here2")
    print(CURRENT_MESSAGE.split(" ")[0] + " this is the message")
    return(CURRENT_MESSAGE)


def main():
     while True:
        handle_message_events()
        parse_message()
        LOOP += 1
        print(LOOP)



# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_ALERT_SOCKET"]).start()
    main()
    
