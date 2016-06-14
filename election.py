from flask import current_app
from math import floor

class Election(object):
    red = "red"
    blue = "blue"
    
    party_colors = {
        "Democratic":blue,
        "Whig":red,
        "Republican":red,
        "Progressive":red
    }

    def __init__(self, year, candidates, winner, max=0):
        current_app.logger.debug("Gathering data for election year: %s", year)
        
        self.year = year
        self.candidates = []
        for candidate in candidates:
            c = Candidate(**candidate)
            self.candidates.append(c)
        self.winner = winner
        
    def getCensusYear(self):
        return int(floor(float(self.year)/10)*10)
    
    def getMapPath(self):
        return "static/map-data/json/{}.json".format(self.getCensusYear())
        
    def getCandidateChronamPath(self, candidate):
        return "static/election-data/{}/{}".format(self.year, candidate.getChronamFileName())
        
    @staticmethod
    def getColor(party):
        return Election.party_colors[party]
        
    @staticmethod
    def addData(js):
        maximum = 0
        for candidate in js["candidates"]:
            candidate["color"] = Election.getColor(candidate["party"])
            current_max = candidate["mentions"]["max"]
            if current_max > maximum: maximum = current_max
        js["max"] = maximum
        return js
	
class Candidate(object):
    
    def __init__(self, first, last, party, state, won, color, mentions):
        self.first = first
        self.last = last
        self.party = party
        self.state = state
        self.won = won
        self.color = color

    def getChronamFileName(self):
        return "chronam_{}.json".format(self.last)