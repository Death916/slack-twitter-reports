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

# debug
    print(message)
    print(event_id)
    print("here")
# debug

    # initialize report class and create file name

    report = mr.samreport(time.asctime() + ".txt")

    # store message in report file
    # alert variable set in report class by raw_alert method
    report.raw_alert(message)
    
    summ = report.make_summary(message)
    print(summ)
    #report.makereport()



"""
def main():
    global CURRENT_MESSAGE
    while True:
            msg = CURRENT_MESSAGE
            print("here3")
            print(CURRENT_MESSAGE)
            parse_message(msg)
            #print(summ)

            CURRENT_MESSAGE = ""
            time.sleep(10)
            print(time.asctime())
    
"""    


# Start your app

    
with ThreadPoolExecutor(max_workers=5) as executor:
    while True:
        #executor.submit(main()).start()
        
        
        executor.submit(SocketModeHandler(app, os.environ["SLACK_ALERT_SOCKET"]).start(), main()).start()
    
       
 
   
    
