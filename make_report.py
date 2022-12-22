import gensim
import time
import spacy
import os
import tweepy
import shutil
import hashlib
""" Creating reports from samdesk alerts"""

class SamReport():
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
        self.tokens = "" #tokens from alert_txt
        self.location = "" #location of incident
        self.distance = "" #distance from incident
        self.debug_active = True
        self.message_hash = "" #hash of alert_txt
        self.last_10_hashes = [] #list of last 10 hashes
    def store_raw_alert(self, alert_txt):
        """store raw alert text in file"""

        with open(self.raw_file, "a") as f:
            f.write(alert_txt + "\n")
            f.close()
            print("alert_txt stored")
            self.alert_txt = alert_txt

        

    def set_incident(self):
        """parse alert_txt for incident type"""
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
        stop_words = spacy.lang.en.stop_words.STOP_WORDS
        for token in tokens:
            if token in stop_words:
                tokens.remove(token)
        self.tokens = tokens
        return tokens
       
    
    def make_summary(self):
        '''generate summary of alert_txt'''
        
        

        try:
            self.summary = gensim.summarization.summarize(self.alert_txt, ratio=0.6)
            if self.summary == "":
                self.summary = self.alert_txt
        
            print("summary completed")
        except:
            print("summary failed")
            self.summary = self.alert_txt
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
        if inc_type == "Police Activity".lower():
            impact = "Police Presence"

        #TODO: put individual impact statements in a dictionary

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
        #select first word in alert_txt
        self.distance = ""
        self.distance = self.tokens[0]
        
        for ent in self.doc.ents:
            
                
            if ent.label_ == "ORG":
                self.distance += ent.text
                self.location = ent.text
                break
        
        return self.distance

    def set_location(self):
        self.location = self.location
        return self.location

    def set_variables(self):
        ''' helper function to set all variables'''
        self.tokenize()
        self.set_incident()
        self.set_impact()
        self.set_references()
        self.set_image()
        self.set_inc_type()
        self.set_distance()
        self.set_location()
        self.make_summary()
        
        self.parse_tokens(self.tokens)
        #self.create_message_hash()

               
   
    def parse_tokens(self, tokens):
        '''add spaces between tokens and remove punctuation'''
        parsed = ""
        #list of punctuation to remove including slashes and asterisks
        punctuation = [",", ".", "?", "!", ":", ";", "(", ")", "[", "]", "{", "}", "/", "*", "'", '"', "#", "“", "”", "\n"]
        for token in tokens:
            parsed += token + " "
        for ent in self.doc.ents:
            if ent.label_== "CARDINAL":
                if ent.text  in parsed:
                    parsed = parsed.replace(ent.text, "")

                
            elif ent.label_ == "ORG":
                if ent.text in parsed:
                    parsed = parsed.replace(ent.text, "")
            elif ent.label_ == "PRODUCT":
                if ent.text in parsed:
                    parsed = parsed.replace(ent.text, "")
                    break
        for punc in punctuation:
            parsed = parsed.replace(punc, "")
        for word in parsed.split():
            if word.lower() == "and":
                parsed = parsed.replace(word, "\"and\"")
        parsed = parsed.replace("  ", " ")
        

        
        return parsed
    
    def archive(self):
        '''copy raw alert to archive folder with message hash as filename'''

        #create archive folder if it doesn't exist in current directory
        if not os.path.exists("archive"):
            os.makedirs("archive")
        
        message_hash = self.message_hash
        message_hash = str(message_hash[:10])

        #create archive file name
        archive_file = "archive/" + "-" + message_hash + ".txt"
        #check if archive file already exists
        if os.path.exists(archive_file):
            print("archive file already exists")
            return False

        #write raw alert to archive file
        with open(archive_file, "w") as f:
            f.write(self.alert_txt)
            f.close()
            print("archive file created")
            
    def  create_message_hash(self,last_10_hashes):
        '''create list of hash of last 10 messages'''
        #create hash of message
        message_hash = hashlib.sha256(self.alert_txt.encode('utf-8')).hexdigest()
        message_hash = str(message_hash[:10])
        self.message_hash = message_hash
        
       
        return message_hash


       
       
                           
    def compare_hashes(self,message_hash, last_10_hashes):
        '''compare hash of current message to last 10 hashes'''
        
        if message_hash in last_10_hashes:
            print("message already hashed")
            return False
        else:
            return True
        #the true means the message is not a duplicate


            


    def debug(self):
        print("debugging")
        self.set_variables()
        self.store_raw_alert(self.alert_txt)
        

       
        print("alert_txt: " + self.alert_txt)
        print("tokens: " + str(self.tokens))
        print("summary: " + self.summary)
        print("impact: " + self.impact)
        print("references: " + self.references)
        print("image: " + self.image)
        print("incident type: " + self.inc_type)
        print("raw_file: " + self.raw_file)
        print("report_file: " + self.report_file)
        print("time_stamp: " + self.time_stamp)
        print("distance: " + self.distance)
        print("location: " + self.location)
        print("message_hash: " + self.message_hash)
        # make 3 lines of -'s
        for i in range(4):
            print(" - - - - - - - - - - COMPLETE- - - - - - - - - - - ")

        """
        tsearch = TwitterSearch()
        parsed = self.parse_tokens(self.tokens)
        result = tsearch.search_twitter(parsed)
        print("twitter result: " + result)
        link = tsearch.create_tweet_link(result)
        print("tweet link: " + link)
        """

    def makereport(self):
        with open(self.report_file, "a") as f:
            f.write("Summary: " + self.summary + "\n")
            f.write("Impact: " +    self.impact + "\n")
            f.write("References: " + self.references + "\n")
            f.write("Map: " + self.image + "\n")  
            f.write("Incident Type: " + self.inc_type + "\n")
            f.close()
            print("report completed")

class TwitterSearch():
    def __init__(self):
        self.twitter_token = os.environ["twitter_token"]
        self.current_tweet_id = ""
        self.current_user_name = ""
        
    

    def search_twitter(self, input_txt):
        #get first 500 characters of alert_txt
        search_term = input_txt[30:50]
        search_term = str(search_term)
        #search twitter for part of alert_txt and return most recent tweet. use v2 twitter api with tweepy
        client = tweepy.Client(self.twitter_token)
        response = client.search_recent_tweets(search_term, expansions="author_id", tweet_fields="created_at")
        most_recent_username = response[0]['users'][0]['username']
        most_recent_tweet_id = response[0]['id']
        self.current_tweet_id = most_recent_tweet_id
        self.current_user_name = most_recent_username
        return most_recent_username, most_recent_tweet_id

    def create_tweet_link(self, *kwargs):
        """
        This function takes username and tweet_id of a tweet and returns a link for the tweet.
        Parameters
        ----------
        username : username for the tweet(string)
        tweet_id : unique tweet id associated with each twitt.  (string)
        """
        username = self.current_user_name
        tweet_id = self.current_tweet_id
        tweet_url = f"https://twitter.com/{username}/status/{tweet_id}"
        return tweet_url