# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, trigger):
        # defines self.trigger as the string the class instance is called with
        
        # formats trigger by removing punctuation
        for punc in string.punctuation:
            trigger = trigger.replace(punc, ' ')
            
        # splits trigger into a list of words, also forces lowercase
        self.trigger = trigger.lower().split()
    
    def is_phrase_in(self, search_string):
               
        # formats search string by removing punctuation
        for punc in string.punctuation:
            search_string = search_string.replace(punc, ' ')
            
        # splits search string into a list of words, also forces lowercase
        search_string = search_string.lower().split()
        
        # creates and fills a dictionary with trigger words as keys and a list of the positions
        # that trigger word occurs in in the searched string
        trig_index = {}
        for trig in self.trigger:
            trig_index[trig] = []
            for i, word in enumerate(search_string):
                if word == trig:
                    trig_index[trig].append(i)
            # if the trigger word does not occur in the searched string,
            # the list will be empty and this will break the loop and return False
            if trig_index[trig] == []:
                return False
        
        # checks that the trigger words all appear in order somewhere in the searched string
        # does not break if a trigger word appears out of order elsewhere in the string
        matched_order = []
        for i, trig in enumerate(self.trigger):
            if i == 0:
                matched_order.append(True)
            else:
                # trig_index(trig) accesses the list of positions with key trig
                for position in trig_index[trig]:
                    if position - 1 in trig_index[self.trigger[i-1]]:
                        matched_order.append(True)
        if len(matched_order) >= len(self.trigger) and all(matched_order):
            return True
        else:
            return False
        
# Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        # assumes story is a NewsStory object
        # retrieves the title from the story object
        return self.is_phrase_in(story.get_title())
        
     
# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        # assumes story is a NewsStory object
        # retrieves the title from the story object
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
    def __init__(self, date_string):
        self.trigger_time = datetime.strptime(date_string, "%d %b %Y %H:%M:%S") #.replace(tzinfo=) ?
        # self.trigger_time.replace(tzinfo=pytz.timezone("EST"))
        
# Problem 6
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        story_time = story.get_pubdate().replace(tzinfo=None)
        # print(story_time, self.trigger_time)
        if story_time < self.trigger_time:
            return True
        else:
            return False
    
class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        story_time = story.get_pubdate().replace(tzinfo=None)
        if story_time > self.trigger_time:
            return True
        else:
            return False

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, not_trigger):
        self.not_trigger = not_trigger
    
    def evaluate(self, story):
        if self.not_trigger.evaluate(story):
            return False
        return True

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, and_trigger1, and_trigger2):
        self.and_trigger1 = and_trigger1
        self.and_trigger2 = and_trigger2
    
    def evaluate(self, story):
        if self.and_trigger1.evaluate(story) and self.and_trigger2.evaluate(story):
            return True
        return False

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, or_trigger1, or_trigger2):
        self.or_trigger1 = or_trigger1
        self.or_trigger2 = or_trigger2
    
    def evaluate(self, story):
        if self.or_trigger1.evaluate(story) or self.or_trigger2.evaluate(story):
            return True
        return False


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
    
    return filtered_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    simple_triggers = {
       'TITLE': TitleTrigger,
       'DESCRIPTION': DescriptionTrigger,
       'BEFORE': BeforeTrigger,
       'AFTER': AfterTrigger
       }
    compound_triggers= {
       'AND': AndTrigger,
       'OR': OrTrigger,
       'NOT': NotTrigger
       }
    # create a dictionary of triggers for use by compound triggers, and initialize the return list
    trigger_dict = {}
    triggerlist = []
    
    # break each line into arguments 
    for line in lines:
        line_split = line.split(',')
        
        # adds trigger entries to trigger_dict as instances of their trigger type
        if line_split[0] != 'ADD':
            trig_title = line_split[0]
            trig_type = line_split[1]
            trig_arg = line_split[2]
            if trig_type in simple_triggers:
                trigger_dict[trig_title] = simple_triggers[trig_type](trig_arg)
            if trig_type in compound_triggers:
                trig_arg2 = line_split[3]
                trigger_dict[trig_title] = compound_triggers[trig_type](trigger_dict[trig_arg], trigger_dict[trig_arg2])
        # after dictionary is created, this adds final triggers to triggerlist
        # note: this will not include any triggers defined after the add line
        else:
            for word in line_split:
                if word != 'ADD':
                    triggerlist.append(trigger_dict[word])    

    return triggerlist



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("coronavirus")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Biden")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

