import os
import json
from election import Election

def writeStats(year, election, stats): 
    for candidate in election["candidates"]:
        for stat in stats:
            if stat["candidate"] == candidate["last"]:
                candidate["mentions"] = stat["mentions"]
    print(election)
    with open('static/election-data/{}/election-stats.json'.format(i), 'w') as f:
        json.dump(election,f)
        
def loadStats(year):
    with open('static/election-data/{}/stats.json'.format(year)) as f: 
        return json.load(f)

def loadElectionData(year):
	with open('static/election-data/{}/election.json'.format(year)) as f:
		return json.load(f)
		
for i in range(1836,1924,4):
    writeStats(i, loadElectionData(i), loadStats(i))