from flask import current_app
'''
class Election(object):

    def __init__(self, year):
        current_app.logger.debug("Gathering data for election year: %s", year)
        
        self.year = year
        self.candidate_1 = TODO
        self.candidate_2 = TODO
        self.candidates = []
  
    def getEventSlides(self):
        return self.event_list

    def getTitleSlide(self):
        return self.titleSlide.getSlide()
	
class Candidate(object):
    
    def __init__(self, first, last, party, home_state):
        self.first = first
        self.last = last
        self.party = party
        self.home_state = home_state
    
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
        return "<a href='{}{}'>Page {} from the {}</a>".format(getBaseUrl(), pageId, pageNum, paperName)
        #self.textDict["text"] = item["ocr_eng"]

    def addMedia(self, seqId):
        self.media_dict["url"] = '{}{}.pdf'.format(getBaseUrl(), seqId[:-1])
'''