from flask import current_app
from math import floor

class Election(object):

    def __init__(self, year, candidates, winner):
        current_app.logger.debug("Gathering data for election year: %s", year)
        
        self.year = year
        self.candidates = []
        for candidate in candidates:
            self.candidates.append(Candidate(**candidate))
        self.winner = winner
        
    def getCensusYear(self):
        return int(floor(float(self.year)/10)*10)
    
    def getMapPath(self):
        return "static/map-data/json/{}.json".format(self.getCensusYear())
        
    def getCandidateChronamPath(self, candidate):
        return "static/election-data/{}/{}".format(self.year, candidate.getChronamFile())
        
    def getStatsPath(self):
        return "static/election-data/{}/stats.json".format(self.year)
	
class Candidate(object):
    
    def __init__(self, first, last, party, state, won):
        self.first = first
        self.last = last
        self.party = party
        self.state = state
        self.won = won
        
    def getChronamFile(self):
        return "chronam-{}.json".format(self.last)