from flask import current_app
from time import gmtime, strftime
from requests import Session
import grequests
import math

BASE_URL = "http://chroniclingamerica.loc.gov"
SEARCH_URL = "{}/search/pages/results/?".format(BASE_URL)
MAX_PAGES = 5
ITEMS_PER_PAGE = 50
TIMEOUT = 30
REQ_THREADS = 5

OR_TERMS = ["elect","election","presidential","president","candidate","party"]
AND_TERMS = ["president","election","candidate"]
PROX_DIST = 5
'''
import ijson

f = urlopen('http://.../')
objects = ijson.items(f, 'earth.europe.item')
cities = (o for o in objects if o['type'] == 'city')
for city in cities:
    do_something_with(city)
    
'''

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
    
def startChronAmSearch(e, callback):
    session = Session()
    results = []
    for candidate in e.candidates:
        startRetrieve(candidateSearchParams(e.year, candidate.first, candidate.last), session, callback)

def startRetrieve(params, session=Session(), callback=None):
    page_1 = session.get(SEARCH_URL, params=params)
    first_json = page_1.json()
    total_items = first_json["totalItems"]
    pages = int(math.ceil(float(total_items)/ITEMS_PER_PAGE))
    if(pages > MAX_PAGES): pages = MAX_PAGES
    reqs = []
    resps = []
    resps.extend(first_json["items"])
    for page in range(2,pages+1):
        #params["page"] = str(page_num)
        reqs.append(grequests.request('GET', SEARCH_URL+"page={}".format(page), timeout=TIMEOUT, params=params, session=session))
    for resp in grequests.imap(reqs, False, REQ_THREADS, exception_handler=exception_handler):
        current_app.logger.debug("Requesting data from %s", resp.request.path_url)
        resps.extend(resp.json()["items"])
    return resps
    

'''

def makeStateCounts(data):
    topicByState = {}
    for page in data:
        topicByState[page["state"][0]] = topicByState.get(page["state"][0], 0) + 1
    topicByState["max"] = sorted(topicByState.values(), reverse=True)[0]
    return topicByState

def wordCountInOCR(topic, ocr):
    return ocr.count(topic)

    for line in ocr:
        count += len(re.findall(topic, line))
        current_app.logger.debug(count)
        #if topic in line: wordcount += 1
    return count


for url in urls:
    words_gen = (word.strip(punctuation).lower() for line in urllib.urlopen(url) for word in line.split())
    for word in words_gen:
        if not(word in ignored_words or len(word) < 4):
            words[word] = words.get(word, 0) + 1
top_words = sorted(words.iteritems(), key=itemgetter(1), reverse=True)[:N]
for word, frequency in top_words:
    print "%s: %d" % (word, frequency)
'''   