from utils import getBaseUrl
from flask import current_app

class Timeline(object):

    def __init__(self, topic, originalJson):
        current_app.logger.debug("Creating timeline for topic: %s", topic)
        
        self.titleSlide = TimelineSlide(topic)
        self.event_list = []
        
        for eventJson in originalJson:
            self.event_list.append(TimelineEvent(eventJson).getSlide())
  
    def getEventSlides(self):
        return self.event_list

    def getTitleSlide(self):
        return self.titleSlide.getSlide()
	
class TimelineSlide(object):
    
    def __init__(self, title):
        self.event_dict = {}
        self.text_dict = {}
        
        self.addText(title)
        self.event_dict["text"] = self.text_dict
        
    def addText(self, title):
        self.text_dict["headline"] = title
        #self.textDict["text"] = item["ocr_eng"]
        
    def getSlide(self):
        return self.event_dict
    
class TimelineEvent(TimelineSlide):

    def __init__(self, eventJson):
        TimelineSlide.__init__(self, self.constructHeadline(eventJson["id"], eventJson["sequence"], eventJson["title"]))
        
        self.media_dict = {}
        self.date_dict = {}
        
        self.addDate(eventJson["date"])
        self.addMedia(eventJson["id"])
        self.event_dict["media"] = self.media_dict
        self.event_dict["start_date"] = self.date_dict

    def addDate(self, originalDate):
        self.date_dict["year"] = originalDate[0:4]
        self.date_dict["month"] = originalDate[4:6]
        self.date_dict["day"] = originalDate[6:8]

    def constructHeadline(self, seqId, pageNum, paperName):
        return '<a href="{}{}">Page {} from the {}</a>'.format(getBaseUrl(), seqId, pageNum, paperName)
        #self.textDict["text"] = item["ocr_eng"]

    def addMedia(self, seqId):
        self.media_dict["url"] = '{}{}.pdf'.format(getBaseUrl(), seqId[:-1])