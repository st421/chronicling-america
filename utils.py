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

OR_TERMS = ["elect","election","presidential","president","candidate","party"]
AND_TERMS = ["president","election","candidate"]
PROX_DIST = 5

'''
dateFilterType=range
date1=01%2F01%2F1884
date2=11%2F30%2F1884
sequence=1
'''
def createTextSearchParams(terms):
    params = terms[0]
    for term in terms[1:]:
        params += " "
        params += term
    return params

def getBaseUrl():
    return BASE_URL
    
def searchParams():
    search_params = {
        "sort":"relevance",
        "rows":str(ITEMS_PER_PAGE),
        "proxdistance":str(PROX_DIST),
        "sequence":"1",
        "searchType":"advanced",
        "format":"json"
    }
    return search_params
    
def candidateSearchParams(year, first, last):
    search_params = searchParams()
    search_params["dateFilterType"] = "yearRange"
    search_params["date1"] = year
    search_params["date2"] = year
    search_params["ortext"] = createTextSearchParams(OR_TERMS)
    search_params["andtext"] = createTextSearchParams(AND_TERMS)
    search_params["proxtext"] = createTextSearchParams([first, last])
    return search_params
    
def exception_handler(request, exception):
    current_app.logger.error("Unable to retrieve data from %s: %s", request.path_url, exception)    

def retrieveData(params):
    session = Session()
    page_1 = session.get(SEARCH_URL, params=params)
    total_items = page_1.json()["totalItems"]
    pages = int(math.ceil(float(total_items)/ITEMS_PER_PAGE))
    if(pages > MAX_PAGES): pages = MAX_PAGES
    reqs = []
    reps = []
    reps.extend(page_1.json()["items"])
    for page_num in range(2,pages+1):
        #params["page"] = str(page_num)
        #reps.extend(session.get(SEARCH_URL, params=params).json()["items"])
        reqs.append(grequests.request('GET', SEARCH_URL+"page={}".format(page_num), timeout=TIMEOUT, params=params, session=session))
    for resp in grequests.imap(reqs, False, REQ_THREADS, exception_handler=exception_handler):
        print(resp.request.path_url)
        js = resp.json()["items"]
        reps.extend(js)
    return reps