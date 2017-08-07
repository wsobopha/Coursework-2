from flask import Flask, render_template, send_file, send_from_directory, redirect, url_for, request
import redis
import urlparse
import string
import os
from werkzeug.exceptions import HTTPException, NotFound
from math import floor

app = Flask(__name__)

redis = redis.Redis(host='localhost', port=6379, db=0)

def shortify(url):
	url_id = redis.get('reverse-url:' + url)
	if url_id is not None:
		return url_id
	url_num = redis.incr('last-url-id')
	url_id = b62_encode(url_num)
	redis.set('url-target:' + url_id, url)
	redis.set('reverse-url:' + url, url_id)
	return url_id

def b62_encode(number):
	base = string.digits + string.lowercase + string.uppercase
	assert number >=0, 'positive integer required'
	if number == 0:
		return '0'
	base62 = []
	while number != 0:
		number, i = divmod(number, 62)
		base62.append(base[i])
	return ''.join(reversed(base62))

@app.route('/')
def home():
	return render_template('index.html')


@app.route('/shortify', methods=['POST'])
def shortener():
	url_to_parse = request.form['input']
	parts = urlparse.urlparse(url_to_parse)
	if not parts.scheme in ('http', 'https'):
		error = "Please enter a valid url"
	else:
		#shortern url using encode to 62
		url_id = shortify(url_to_parse)
	return render_template('shortified.html', url_id=url_id)

@app.route("/<url_id>")
def go_to_url(url_id):
	url_target = redis.get('url-target' + url_id)
	if url_target is None:
		raise NotFound()
	redis.incr('click-count:' + url_id)
	return redirect(url_target)



if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)
