#from flask import current_app

class Election(object):

    def __init__(self, year, candidates, winner):
        #current_app.logger.debug("Gathering data for election year: %s", year)
        
        self.year = year
        self.candidates = []
        for candidate in candidates:
            self.candidates.append(Candidate(**candidate))
        self.winner = winner
	
class Candidate(object):
    
    def __init__(self, first, last, party, state, won):
        self.first = first
        self.last = last
        self.party = party
        self.state = state
        self.won = won