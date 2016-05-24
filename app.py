import os
from flask import Flask, render_template, jsonify, request, flash
from loc_data import *
from search_form import SearchForm

app = Flask(__name__)
#TODO form security
#TODO secret_key
app.secret_key = 'some_secret'

@app.route('/getTimelineData/<topic>',methods=['GET'])
def getTimelineData(topic):
	url = 'http://chroniclingamerica.loc.gov/search/pages/results/?andtext={}&format=json'.format(topic)
	event_list = parse_json(get_data(url))
	text_dict = {}
	text_dict["headline"] = topic
	text_dict["text"] = ""
	title_dict = {}
	title_dict["text"] = text_dict
	timeline_data = {}
	timeline_data["title"] = title_dict
	timeline_data["events"] = event_list
	return jsonify(timeline_data)

@app.route('/',methods=['GET','POST'])
def main():
	form = SearchForm(request.form)
	if request.method == 'POST':
		key_word = form.key_word.data
		form.key_word.data = ''
		return render_template('timeline.html', key_word=key_word)
	else: 
		return render_template('index.html', form=form) 

if __name__ == "__main__":
	app.debug = True
	app.logger.warning("fiddlesticks!")
	app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)