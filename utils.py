from flask import current_app
from time import gmtime, strftime
from requests import Session
import grequests
import math

BASE_URL = "http://chroniclingamerica.loc.gov"
SEARCH_URL = "{}/search/pages/results/?".format(BASE_URL)
MAX_PAGES = 10
ITEMS_PER_PAGE = 50
TIMEOUT = 30
REQ_THREADS = 5

def getBaseUrl():
    return BASE_URL
    
def searchParams():
    search_params = {
        "sort":"relevance",
        "rows":str(ITEMS_PER_PAGE),
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
    current_app.logger.error("Unable to retrieve data from %s: %s", request.path_url, exception)    

def retrieveData(params):
    session = Session()
    page_1 = session.get(SEARCH_URL, params=params)
    total_items = page_1.json()["totalItems"]
    pages = int(math.ceil(total_items/ITEMS_PER_PAGE))
    if(pages > MAX_PAGES): pages = MAX_PAGES
    reqs = []
    reps = []
    reps.extend(page_1.json()["items"])
    for page_num in range(2,pages):
        #params["page"] = str(page_num)
        #reps.extend(session.get(SEARCH_URL, params=params).json()["items"])
        reqs.append(grequests.request('GET', SEARCH_URL+"page={}".format(page_num), timeout=TIMEOUT, params=params, session=session))
    for resp in grequests.imap(reqs, False, REQ_THREADS, exception_handler=exception_handler):
        print(resp.request.path_url)
        js = resp.json()["items"]
        reps.extend(js)
    return reps