import os
import json
from collections import defaultdict
from election import Election

def writeStats(election): 
    by_state = defaultdict(lambda: [])
    for candidate in election.candidates:
        pages = loadCandidateChronam(election.year, candidate.last)
        for page in pages:
            for state in page["state"]:
                by_state[state].append(page)
        with open('static/election-data/{}/chronam_{}.json'.format(election.year,candidate.last), 'w') as f:
            json.dump(by_state,f)

def loadCandidateChronam(year, lastName):
    with open('static/election-data/{}/chronam-{}.json'.format(year,lastName)) as f: 
        js = json.load(f)
        return js

def loadElectionData(year):
	with open('static/election-data/{}/election.json'.format(year)) as f:
		js = json.load(f)
		e = Election(**js)
		return e
		
for i in range(1836,1924,4):
    writeStats(loadElectionData(i))