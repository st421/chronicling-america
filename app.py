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
	
def loadElectionData(year):
	with app.open_resource('static/election-data/{}.json'.format(year)) as f:
		js = json.load(f)
		e = Election(**js)
		return e
		
@app.route('/getTimelineData/<topic>')
def getTimelineData(topic):
	#tl = Timeline(topic, retrieveData(timelineSearchParams(topic)))
	timeline_data = {}
	#timeline_data["title"] = tl.getTitleSlide()
	#timeline_data["events"] = tl.getEventSlides()
	return jsonify(timeline_data)
	
@app.route('/getMediaData/<year>/<first>/<last>')
def getMediaData(year, first, last):
	js = startRetrieve(candidateSearchParams(year, first, last))
	state_counts = makeStateCounts(js)
	return jsonify(state_counts)

@app.route('/', methods=['GET','POST'])
def main():
	if request.method == 'POST':
		form = SearchForm(request.form)
		if form.validate():
			year = form.year.data
			e = loadElectionData(year)
			#startChronAmSearch(e, TODO)
			return render_template('map.html', year=year, candidates=e.candidates)
		else:
			flash('Please choose an election year')
			return frontPage()
	else: 
		return frontPage()

if __name__ == "__main__":
	app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)