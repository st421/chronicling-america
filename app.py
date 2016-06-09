import os
import json
from flask import Flask, render_template, jsonify, request, flash
from utils import retrieveData, mapSearchParams, timelineSearchParams
from timeline import Timeline
from forms import SearchForm
from map import makeStateCounts

app = Flask(__name__)
#TODO form security
#TODO secret_key
app.secret_key = 'some_secret'

@app.route('/getTimelineData/<topic>')
def getTimelineData(topic):
	tl = Timeline(topic, retrieveData(timelineSearchParams(topic)))
	timeline_data = {}
	timeline_data["title"] = tl.getTitleSlide()
	timeline_data["events"] = tl.getEventSlides()
	return jsonify(timeline_data)
	
@app.route('/getMapData/<year>')
def getMapData(topic, year):
	word_counts = makeStateCounts(topic, year)
	app.logger.debug(word_counts)
	return jsonify(word_counts)
	
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