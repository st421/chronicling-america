import re
from string import punctuation
from operator import itemgetter
from flask import current_app

def makeStateCounts(data):
    topicByState = {}
    for page in data:
        topicByState[page["state"][0]] = topicByState.get(page["state"][0], 0) + 1
    topicByState["max"] = sorted(topicByState.values(), reverse=True)[0]
    return topicByState

def wordCountInOCR(topic, ocr):
    return ocr.count(topic)
    '''
    for line in ocr:
        count += len(re.findall(topic, line))
        current_app.logger.debug(count)
        #if topic in line: wordcount += 1
    return count
    '''
'''
for url in urls:
    words_gen = (word.strip(punctuation).lower() for line in urllib.urlopen(url) for word in line.split())
    for word in words_gen:
        if not(word in ignored_words or len(word) < 4):
            words[word] = words.get(word, 0) + 1
top_words = sorted(words.iteritems(), key=itemgetter(1), reverse=True)[:N]
for word, frequency in top_words:
    print "%s: %d" % (word, frequency)
'''       