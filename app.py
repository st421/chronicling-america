import os
from flask import Flask, render_template, json, jsonify, request, flash, url_for, logging
from werkzeug.contrib.cache import SimpleCache
from logging import Formatter
from utils import startRetrieve, candidateSearchParams
from timeline import Timeline
from forms import SearchForm
from election import Election
from map import makeStateCounts

app = Flask(__name__)
#TODO form security
#TODO secret_key
app.secret_key = 'some_secret'
app.cache = SimpleCache(app)
h = logging.StreamHandler()
h.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.logger.addHandler(h)

def frontPage():
	return render_template('index.html', form=SearchForm())
	
def loadChronamData(year, candidate, state):
	with app.open_resource('static/election-data/{}/chronam_{}.json'.format(year, candidate)) as f:
		js = json.load(f)
		return js[state]
	
def loadElectionData(year):
	with app.open_resource('static/election-data/{}/election.json'.format(year)) as f:
		js = json.load(f)
		e = Election(**js)
		return e
		
@app.route('/getPartyColor/<party>')
def getPartyColor(party):
	return Election.getColor(party)
	
@app.route('/getTimelinePath/<year>/<name>/<state>')
def getTimelinePath(year, name, state):
	return render_template('timeline.html', year=year, name=name, state=state)
	
@app.route('/getTimelineData/<year>/<name>/<state>')
def getTimelineData(year, name, state):
	tl = Timeline(year, name, state, loadChronamData(year, name, state))
	timeline_data = {}
	timeline_data["title"] = tl.getTitleSlide()
	timeline_data["events"] = tl.getEventSlides()
	return jsonify(timeline_data)

@app.route('/', methods=['GET','POST'])
def main():
	if request.method == 'POST':
		form = SearchForm(request.form)
		if form.validate():
			year = form.year.data
			e = loadElectionData(year)
			return render_template('map.html', e=e)
		else:
			flash('Please choose an election year')
			return frontPage()
	else: 
		return frontPage()

if __name__ == "__main__":
	app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)