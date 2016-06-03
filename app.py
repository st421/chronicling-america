import os
import json
from flask import Flask, render_template, jsonify, request, flash
from utils import getTimelineJson, getMapJson
from timeline import Timeline
from forms import SearchForm

app = Flask(__name__)
#TODO form security
#TODO secret_key
app.secret_key = 'some_secret'

@app.route('/getTimelineData/<topic>')
def getTimelineData(topic):
	tl = Timeline(topic, getTimelineJson(topic)["items"])
	timeline_data = {}
	timeline_data["title"] = tl.getTitleSlide()
	timeline_data["events"] = tl.getEventSlides()
	return jsonify(timeline_data)

@app.route('/', methods=['GET','POST'])
def main():
	if request.method == 'POST':
		form = SearchForm(request.form)
		if form.validate():
			key_word = form.key_word.data
			year = form.year.data
			if year is 0:
				return render_template('timeline.html', key_word=key_word)
			else:
				return render_template('term-frequency-map.html', key_word=key_word, year=year)
		else:
			flash('Please enter a valid search topic')
			return render_template('index.html', form=SearchForm())
	else: 
		form = SearchForm()
		return render_template('index.html', form=form) 

if __name__ == "__main__":
	app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)