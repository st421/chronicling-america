import json
import sys
from urllib2 import Request, urlopen, URLError

def parse_json(json_string):
    original_data = json.loads(json_string)
    items = original_data["items"]
    events_list = []
    for item in items:
        event_dict = {}
        media_dict = {}
        date_dict = {}
        text_dict = {}
        #text_dict["headline"] = item["title"]
        #text_dict["text"] = item["ocr_eng"]
        date_dict["year"] = item["date"][0:4]
        date_dict["month"] = item["date"][4:6]
        date_dict["day"] = item["date"][6:8]
        text_dict["headline"] = '<a href="http://chroniclingamerica.loc.gov{}">Page {} from the {}</a>'.format(item["id"], item["sequence"], item["title"])
        media_dict["url"] = 'http://chroniclingamerica.loc.gov{}.pdf'.format(item["id"][:-1])
        event_dict["media"] = media_dict
        event_dict["start_date"] = date_dict
        event_dict["text"] = text_dict
        events_list.append(event_dict)
    return events_list

def get_data(url):
    request = Request(url)
    try:
    	response = urlopen(request)
    	json_data = response.read()
        return json_data
    except URLError, e:
        print 'Unable to retrieve data', e