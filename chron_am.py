import sys
from urllib2 import Request, urlopen, URLError
from flask import current_app

BASE_URL = "http://chroniclingamerica.loc.gov"

def getBaseUrl():
    return BASE_URL
'''
def parse_json_words(json_string):
    original_data = json.loads(json_string)
    items = original_data["items"]
    ocr_urls_list = []
    for item in items:
        ocr_urls_list.append('http://chroniclingamerica.loc.gov{}ocr.txt'.format(item["id"]))
    return ocr_urls_list
'''
def searchUrl(topic):
    url = '{}/search/pages/results/?andtext={}&format=json'.format(BASE_URL, topic)
    return url
    
def retrieveRawData(url):
    current_app.logger.debug("Retrieving data from %s", url)
    request = Request(url)
    try:
    	response = urlopen(request)
    	json_data = response.read()
        return json_data
    except URLError, e:
        current_app.logger.debug("Unable to retrieve data: %s", e)