import gensim
import time

class samreport():
    def __init__(self, report_file):
        self.report_file = report_file
        self.alert_txt = ""
        self.time = ""
        self.summary = ""
        self.impact= " "
        self.references= ""
        self.map= ""
        self.inc_type= ""

    # save raw incident alert_txt

    def raw_alert(self, raw_alert):

        with open(self.report_file, "a") as f:
            f.write(raw_alert + "\n")
            f.close()
            print("alert_txt stored")
            self.alert_txt = raw_alert


    def parse_message(CURRENT_MESSAGE):
   
        print("here2")
        #print(CURRENT_MESSAGE.split(" ")[0] + " this is the message")
        return(CURRENT_MESSAGE)

    # summarize alert_txt using gensim
    def make_summary(self, alert_txt):
        
        summ = gensim.summarization.summarize(alert_txt, ratio=0.2)
        print(summ)
        print("summary completed")
        print(time.asctime())
        return summ