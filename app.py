import os
import json
from flask import Flask, render_template, jsonify, request, flash
from utils import retrieveData, candidateSearchParams
from timeline import Timeline
from forms import SearchForm
from map import makeStateCounts

app = Flask(__name__)
#TODO form security
#TODO secret_key
app.secret_key = 'some_secret'

@app.route('/getTimelineData/<topic>')
def getTimelineData(topic):
	#tl = Timeline(topic, retrieveData(timelineSearchParams(topic)))
	timeline_data = {}
	#timeline_data["title"] = tl.getTitleSlide()
	#timeline_data["events"] = tl.getEventSlides()
	return jsonify(timeline_data)
	
@app.route('/candidate_1/<year>')
def candidate_1(year):
	js = retrieveData(candidateSearchParams(year, "Grover", "Cleveland"))
	state_counts = makeStateCounts(js)
	return jsonify(state_counts)
	
@app.route('/candidate_2/<year>')
def candidate_2(year):
	js = retrieveData(candidateSearchParams(year, "James", "Blaine"))
	state_counts = makeStateCounts(js)
	return jsonify(state_counts)
	
def frontPage():
	return render_template('index.html', form=SearchForm())

@app.route('/', methods=['GET','POST'])
def main():
	if request.method == 'POST':
		form = SearchForm(request.form)
		if form.validate():
			year = form.year.data
			return render_template('map.html', year=year)
		else:
			flash('Please choose an election year')
			return frontPage()
	else: 
		return frontPage()

if __name__ == "__main__":
	app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)