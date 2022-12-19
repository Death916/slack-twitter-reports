import gensim
import time
import spacy
""" Creating reports from samdesk alerts"""

class samreport():
    def __init__(self, file_name, alert_txt):
        self.alert_txt = alert_txt
        self.nlp = spacy.load("en_core_web_sm")
        self.doc = self.nlp(self.alert_txt)
        self.inc_type = "" #incident type
        self.references = "" #url from tweet
        self.image = "" #map image from location
        self.impact = "" #impact of incident
        self.summary = "" #summary of incident
        self.raw_file = file_name #raw alert file name
        self.report_file = "" #report file name
        self.time_stamp = time.asctime() #time stamp for report file name

    def store_raw_alert(self, alert_txt):

        with open(self.raw_file, "a") as f:
            f.write(alert_txt + "\n")
            f.close()
            print("alert_txt stored")
            self.alert_txt = alert_txt

        

    def set_incident(self):
     #parse alert_txt for incident type
        for ent in self.doc.ents:
            print(ent.text, ent.label_)
            if ent.label_ == "EVENT":
                self.inc_type = ent.text
                print("incident type: " + self.inc_type)
                return self.inc_type
                break
            elif ent.label_ == "ROOT":
                self.inc_type = ent.text
                print("incident type: " + self.inc_type)
                return self.inc_type
                break
            elif ent.label_ == "":
                pass                
            
        return self.inc_type

    def tokenize(self):
        tokens = [token.text for token in self.doc]
        return tokens
       

    def make_summary(self):
        self.summary = gensim.summarization.summarize(self.alert_txt, ratio=0.2)
        if self.summary == "":
            self.summary = self.alert_txt
        print("Summary: " + self.summary)
        print("summary completed")
        return self.summary

    def set_impact(self):
        impact = ""
        inc_type = self.inc_type.lower()
        if inc_type == "fire".lower():
            impact = "Possible evacuation, Fire Danger"
        if inc_type == "Shooting".lower():
            impact = "Police Presence"
        if inc_type == "Bomb Threat".lower():
            impact = "Police Presence, Possible evacuation"
        if inc_type == "Suspicious Package".lower():
            impact = "Police Presence, Possible evacuation"
        if inc_type == "Suspicious Person".lower():
            impact = "Police Presence"
        if inc_type == "Suspicious Vehicle".lower():
            impact = "Police Presence"
        if inc_type == "Hazmat Incident".lower():
            impact = "Police Presence, Possible evacuation"
        
        self.impact = impact
        return self.impact

    def set_references(self):
        self.references = self.references
        return self.references

    def set_image(self):
        self.image = self.image
        return self.image

    def set_inc_type(self):
        self.inc_type = self.inc_type
        return self.inc_type

    def set_distance(self):
        pass
    

    def makereport(self):
        with open(self.report_file, "a") as f:
            f.write("Summary: " + self.summary + "\n")
            f.write("Impact: " +    self.impact + "\n")
            f.write("References: " + self.references + "\n")
            f.write("Map: " + self.image + "\n")  
            f.write("Incident Type: " + self.inc_type + "\n")
            f.close()
            print("report completed")

