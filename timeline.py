from utils import getBaseUrl
from flask import current_app

class Timeline(object):

    def __init__(self, year, name, state, items):
        
        current_app.logger.debug("Creating timeline for %s in %s", name, year)
        
        self.titleSlide = TimelineSlide('{} newspaper coverage of <span class="{}">{}</span> | <span class="year">{}</span>'.format(state, "blue", name, year))
        self.event_list = []
        
        for page in items:
            try:
                self.event_list.append(TimelineEvent(page).getSlide())
            except Exception as e:
                current_app.logger.info(e)
                pass
  
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

    def __init__(self, page):
        TimelineSlide.__init__(self, self.constructHeadline(page["id"], page["sequence"], page["title"]))
        
        self.media_dict = {}
        self.date_dict = {}
        
        self.addDate(page["date"])
        self.addMedia(page["id"])
        self.event_dict["media"] = self.media_dict
        self.event_dict["start_date"] = self.date_dict

    def addDate(self, date):
        self.date_dict["year"] = date[0:4]
        self.date_dict["month"] = date[4:6]
        self.date_dict["day"] = date[6:8]

    def constructHeadline(self, pageId, pageNum, paperName):
        return "<a href='{}{}'>{}</a>".format(getBaseUrl(), pageId, paperName)
        #self.textDict["text"] = item["ocr_eng"]

    def addMedia(self, seqId):
        self.media_dict["url"] = '{}{}.pdf'.format(getBaseUrl(), seqId[:-1])
        current_app.logger.debug(self.media_dict["url"])