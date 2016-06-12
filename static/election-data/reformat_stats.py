import os
import json
from election import Election

def writeStats(election): 
    stats = []
    for candidate in election.candidates:
        cStats = loadCandidateStats(election.year, candidate.last)
        candidate_stats = {}
        candidate_stats["candidate"] = candidate.last
        candidate_stats["mentions"] = cStats
        stats.append(candidate_stats)
    with open('static/election-data/{}/stats.json'.format(election.year), 'w') as f:
        json.dump(stats,f)
        
def loadCandidateStats(year, candidate):
    with open('static/election-data/{}/stats-{}.json'.format(year,candidate)) as f: 
        js = json.load(f)
        return js

def loadElectionData(year):
	with open('static/election-data/{}/election.json'.format(year)) as f:
		js = json.load(f)
		e = Election(**js)
		return e
		
for i in range(1840,1924,4):
    writeStats(loadElectionData(i))