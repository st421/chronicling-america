import sys
import json
from urllib2 import Request, urlopen, URLError
from flask import current_app

BASE_URL = "http://chroniclingamerica.loc.gov"
SEARCH_URL = '{}/search/pages/results/?'.format(BASE_URL)

search_params = {}
search_params['format'] = 'json'
search_params['page'] = '1'
search_params['sequence'] = '0'
search_params['rows'] = '20'
search_params['date1'] = ''
search_params['date2'] = ''
search_params['dateFilterType'] = ''

def getBaseUrl():
    return BASE_URL
    
def timelineSearchUrl(topic):
    search_params['sort'] = 'date'
    return searchUrl(topic)
   
def mapSearchUrl(topic, year):
    search_params['sort'] = 'state'
    search_params['dateFilterType'] = 'yearRange'
    search_params['date1'] = year
    search_params['date2'] = year
    return searchUrl(topic)

def searchUrl(topic, **kwargs):
    this_search = SEARCH_URL
    search_params['protext'] = topic
    for k, v in kwargs.items():
        if search_params.has_key(k):
            search_params[k] = v
    for k, v in search_params.items():
        this_search += ('&{}={}'.format(k,v))
    return this_search
    
def retrieveRawData(url):
    current_app.logger.debug("Retrieving data from %s", url)
    request = Request(url)
    try:
    	response = urlopen(request)
        return response.read()
    except URLError, e:
        current_app.logger.debug("Unable to retrieve data: %s", e)
        
def loadJson(url):
    return json.loads(retrieveRawData(url))
        
def getTimelineJson(topic):
    return loadJson(timelineSearchUrl(topic))
    
def getMapJson(topic, year):
    return loadJson(mapSearchUrl(topic, year))