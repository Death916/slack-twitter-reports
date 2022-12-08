#samdesk-alerts

from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
import time
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import make_report as mr
import threading
import gensim



# Read the environment variables
SLACK_TOKEN = os.environ["SLACK_API_TOKEN"]
SLACK_ALERT_SOCKET = os.environ["SLACK_ALERT_SOCKET"]

# Install the Slack app and get xoxb- token in advance
app = App(token=SLACK_ALERT_SOCKET)
 
CURRENT_MESSAGE = "hi"
LOOP = 0



# Listen for incoming messages
@app.event("message")
def handle_message_events(body, **kwargs):
    #logger.info(body)
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
    global CURRENT_MESSAGE
    CURRENT_MESSAGE = message


def parse_message(CURRENT_MESSAGE):
   
    print("here2")
    print(CURRENT_MESSAGE.split(" ")[0] + " this is the message")
    return(CURRENT_MESSAGE)

def summary():

def main():
    global CURRENT_MESSAGE
    while True:
            msg = CURRENT_MESSAGE
            print("here3")
            print(CURRENT_MESSAGE)
            parse_message(msg)
            CURRENT_MESSAGE = ""
            time.sleep(10)
    
    


# Start your app

    
with ThreadPoolExecutor(max_workers=3) as executor:
    while True:
        #executor.submit(main)
        
        
        executor.submit(SocketModeHandler(app, os.environ["SLACK_ALERT_SOCKET"]).start())
    

 
   
    
