import json
import re
from string import punctuation
from operator import itemgetter
from requests import Session
import grequests
import math
from election import Election

BASE_URL = "http://chroniclingamerica.loc.gov"
SEARCH_URL = "{}/search/pages/results/?".format(BASE_URL)
ITEMS_PER_PAGE = 50
TIMEOUT = 30
REQ_THREADS = 5

OR_TERMS = ["elect","election","presidential","president","candidate","party"]
AND_TERMS = ["president","election","candidate"]
PROX_DIST = 5

def loadElectionData(year):
	with open('static/election-data/{}/election.json'.format(year)) as f:
		js = json.load(f)
		e = Election(**js)
		return e
		
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
    print("Unable to retrieve data from %s: %s", request.path_url)    
    print(exception)
    
def makeStateCounts(data):
    topicByState = {}
    for page in data:
        topicByState[page["state"][0]] = topicByState.get(page["state"][0], 0) + 1
    topicByState["max"] = sorted(topicByState.values(), reverse=True)[0]
    return topicByState
   
def writeElectionMedia(year, candidate, js): 
    for page in js:
        page["ocr_eng"] = ""
    with open('static/election-data/{}/chronam-{}.json'.format(year,candidate),'w') as f:
        json.dump(js,f)
    state_counts = makeStateCounts(js)
    with open('static/election-data/{}/stats-{}.json'.format(year,candidate),'w') as f:
        json.dump(state_counts,f)

def getElectionMedia(params, session=Session()):
    page_1 = session.get(SEARCH_URL, params=params)
    first_json = page_1.json()
    total_items = first_json["totalItems"]
    pages = int(math.ceil(float(total_items)/ITEMS_PER_PAGE))
    reqs = []
    resps = []
    resps.extend(first_json["items"])
    for page in range(2,pages+1):
        reqs.append(grequests.request('GET', SEARCH_URL+"page={}".format(page), timeout=TIMEOUT, params=params, session=session))
    for resp in grequests.imap(reqs, False, REQ_THREADS, exception_handler=exception_handler):
        print("Requesting data from %s", resp.request.path_url)
        resps.extend(resp.json()["items"])
    return resps
    
def getAndWriteElectionMedia(e):
    session = Session()
    results = []
    for candidate in e.candidates:
        writeElectionMedia(e.year, candidate.last, getElectionMedia(candidateSearchParams(e.year, candidate.first, candidate.last), session))
    
for i in range(1840,1924,4):
    e = loadElectionData(i)
    getAndWriteElectionMedia(e)