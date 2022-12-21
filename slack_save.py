#samdesk-alerts

from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
import time
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from make_report import SamReport


# Read the environment variables
SLACK_TOKEN = os.environ["SLACK_API_TOKEN"]
SLACK_ALERT_SOCKET = os.environ["SLACK_ALERT_SOCKET"]

# Install the Slack app and get xoxb- token in advance
app = App(token=SLACK_ALERT_SOCKET)
 
CURRENT_MESSAGE = "hi"
LOOP = 0
DEBUG = False
input = input("debug? (y/n): ")
if input == "y":
    DEBUG = True
    print("debugging")
else:
    print("not debugging")

class slack_save:
    

   

    # Listen for incoming messages
    @app.event("message")
    def handle_message_events(body, **kwargs):
        #logger.info(body)
        message = body["event"]["text"]
        
        # Get the channel ID
        event_id = body.get("event_id")

        print(event_id)


        # initialize report class and create file name
        report_title = time.asctime() + ".txt"
        
        report_title = report_title.replace(" ", "-") #replace spaces in file name with hyphens 

        
        report = SamReport(report_title, message)

        # store message in report file
        # alert variable set in report class by raw_alert method
        report.store_raw_alert(message)

    
        if DEBUG == True:
            report.debug()

       

        # send summary 


        

if __name__ == "__main__":
    
        
     with ThreadPoolExecutor(max_workers=5) as executor:
            while True:
            #executor.submit(main()).start()
            
            
                executor.submit(SocketModeHandler(app, os.environ["SLACK_ALERT_SOCKET"]).start())
        
        
    
    
        
