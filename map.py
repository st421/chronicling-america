'''
import json
#import urllib
import re
from string import punctuation
from operator import itemgetter
from flask import current_app
from utils import getJson

# eliminate most common words https://en.wikipedia.org/wiki/Most_common_words_in_English
# prepositions
# quantifiers (many, few, etc.)
# eliminate single characters
# eliminate days of week, months, state names, etc.
#http://chroniclingamerica.loc.gov/search/pages/results/?date1=1836&date2=1922&sequence=&lccn=&state=&rows=50&ortext=&proxtext=%22jim+crow%22&year=&phrasetext=&andtext=&proxValue=&dateFilterType=yearRange&page=34&sort=state&format=json

def makeWordCounts(topic, year):
    raw_json = getJson(topic, year)
urls = parse_json_words(get_data())
#url = "http://chroniclingamerica.loc.gov/lccn/sn82016187/1907-05-23/ed-1/seq-1/ocr.txt"
N = 20
ignored_words = set(['','the','a','of','and','to','in','our','that','it','be','is','with','for','by','we','this','their','as','on','which','not','are','but','was','all','will','shall','tho','or','from','he','she','its','an','such','have','at','them','his','has','were','who','us','they','i','I','had','you','would','one','been','there','into','before','other','said','when','today','yesterday','made','here','some','about','more','last','time','over','much','after','than','very','great'])                                
words = {}
wordcount = 0
for url in urls:
    for line in urllib.urlopen(url):
        if 'Taft' in line: wordcount += 1
    print wordcount
    wordcount = 0
    

def parse_json_words(json_string):
    original_data = json.loads(json_string)
    items = original_data["items"]
    ocr_urls_list = []
    for item in items:
        ocr_urls_list.append('http://chroniclingamerica.loc.gov{}ocr.txt'.format(item["id"]))
    return ocr_urls_list

for url in urls:
    words_gen = (word.strip(punctuation).lower() for line in urllib.urlopen(url) for word in line.split())
    for word in words_gen:
        if not(word in ignored_words or len(word) < 4):
            words[word] = words.get(word, 0) + 1
        
top_words = sorted(words.iteritems(), key=itemgetter(1), reverse=True)[:N]
for word, frequency in top_words:
    print "%s: %d" % (word, frequency)
'''