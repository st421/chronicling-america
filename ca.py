from flask import Blueprint, render_template, json, jsonify, request, flash, url_for, current_app
from timeline import Timeline
from forms import SearchForm
from election import Election

ca = Blueprint('ca', __name__, template_folder='templates', static_folder='static')

@ca.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		form = SearchForm(request.form)
		if form.validate():
			year = form.year.data
			e = loadElectionData(year)
			return render_template('ca/map.html', e=e)
		else:
			flash('Please choose an election year')
			return frontPage()
	else: 
		return frontPage()

def frontPage():
	return render_template('ca/index.html', form=SearchForm())

@ca.route('/getCurrentElectionJson')
def getCurrentElectionJson():
	return jsonify(current_app.current_election_json)
	
@ca.route('/getTimelinePath/<year>/<name>/<state>')
def getTimelinePath(year, name, state):
	return render_template('ca/timeline.html', year=year, name=name, state=state)
	
@ca.route('/getTimelineData/<year>/<name>/<state>')
def getTimelineData(year, name, state):
	tl = Timeline(year, name, state, loadChronamData(year, name, state))
	timeline_data = {}
	timeline_data["title"] = tl.getTitleSlide()
	timeline_data["events"] = tl.getEventSlides()
	return jsonify(timeline_data)
		
def loadChronamData(year, candidate, state):
	with ca.open_resource('static/election-data/{}/chronam_{}.json'.format(year, candidate)) as f:
		js = json.load(f)
		return js[state]
	
def loadElectionData(year):
	with ca.open_resource('static/election-data/{}/election-stats.json'.format(year)) as f:
		js = json.load(f)
		current_app.current_election_json = Election.addData(js)
		e = Election(**js)
		return e