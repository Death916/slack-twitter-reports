#samdesk-alerts

from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
import time
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from make_report import samreport


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
    report_title = time.asctime() + ".txt"
    
    report_title = report_title.replace(" ", "-") #replace spaces in file name with hyphens 

    
    report = samreport(report_title, message)

    # store message in report file
    # alert variable set in report class by raw_alert method
    report.store_raw_alert(message)
    

    # generate summary
     
    summ = report.make_summary()
    print("summary: " + summ)
    
    tokens = report.tokenize()
    print(tokens)
    incident_type = report.set_incident()
    print(incident_type)
    #report.makereport()

    # send summary 


    
with ThreadPoolExecutor(max_workers=5) as executor:
    while True:
        #executor.submit(main()).start()
        
        
        executor.submit(SocketModeHandler(app, os.environ["SLACK_ALERT_SOCKET"]).start())
    
       
 
   
    
