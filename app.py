import os
import json
from flask import Flask, render_template, jsonify, request, flash
from chron_am import searchUrl, retrieveRawData
from timeline import Timeline
from search_form import SearchForm

app = Flask(__name__)
#TODO form security
#TODO secret_key
app.secret_key = 'some_secret'

@app.route('/getTimelineData/<topic>', methods=['GET'])
def getTimelineData(topic):
	tl = Timeline(topic, json.loads(retrieveRawData(searchUrl(topic)))["items"])
	timeline_data = {}
	timeline_data["title"] = tl.getTitleSlide()
	app.logger.debug("Title slide: %s", tl.getTitleSlide())
	timeline_data["events"] = tl.getEventSlides()
	app.logger.debug("Event slides: %s", tl.getEventSlides())
	timeline_json = jsonify(timeline_data)
	app.logger.debug("Converted JSON for timeline: %s", timeline_json)
	return timeline_json

@app.route('/', methods=['GET','POST'])
def main():
	form = SearchForm(request.form)
	if request.method == 'POST':
		key_word = form.key_word.data
		form.key_word.data = ''
		return render_template('timeline.html', key_word=key_word)
	else: 
		return render_template('index.html', form=form) 

if __name__ == "__main__":
	app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)