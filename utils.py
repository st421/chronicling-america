from flask import current_app
from time import gmtime, strftime
from requests import Session
import grequests
import math

BASE_URL = "http://chroniclingamerica.loc.gov"
SEARCH_URL = "{}/search/pages/results/?".format(BASE_URL)

def getBaseUrl():
    return BASE_URL
    
def searchParams():
    search_params = {
        "sort":"relevance",
        "rows":"50",
        "sequence":"1",
        "format":"json",
    }
    return search_params
    
def timelineSearchParams(topic):
    search_params = searchParams()
    search_params["andtext"] = topic
    return search_params
   
def mapSearchParams(topic, year):
    search_params = timelineSearchParams(topic)
    #search_params["sort"] = "state"
    search_params["dateFilterType"] = "yearRange"
    search_params["date1"] = year
    search_params["date2"] = year
    return search_params
    
def exception_handler(request, exception):
    current_app.logger.debug("Unable to retrieve data from %s: %s", request.path_url, exception)    

def retrieveData(params):
    session = Session()
    page_1 = session.get(SEARCH_URL, params=params)
    total_items = page_1.json()["totalItems"]
    pages = int(math.ceil(total_items/50))
    if(pages > 100): pages = 100
    reqs = []
    reps = []
    reps.extend(page_1.json()["items"])
    for page_num in range(2,pages):
        #params["page"] = str(page_num)
        #reps.extend(session.get(SEARCH_URL, params=params).json()["items"])
        reqs.append(grequests.request('GET', SEARCH_URL+"page={}".format(page_num), timeout=30, params=params, session=session))
    #rs = (grequests.get(u) for u in urls)
    #def imap(requests, stream=False, size=2, exception_handler=None)
    for resp in grequests.imap(reqs, False, 5, exception_handler=exception_handler):
        print(resp.request.path_url)
        reps.extend(resp.json()["items"])
    return reps