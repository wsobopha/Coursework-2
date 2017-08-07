from flask import Flask, flash, redirect, render_template, request, session, abort, g, url_for
from werkzeug import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/tc/Coursework-2/src/storage.db'
db = SQLAlchemy(app)

class Images(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(300))
	data = db.Column(db.LargeBinary)

app.secret_key = os.urandom(12)


# Uploads
photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
configure_uploads(app, photos)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		session.pop('user', None)

		if request.form['password'] == 'password':
			session['user'] = request.form['username']
			return redirect(url_for('profile'))

	return render_template('login.html')

@app.route('/profile')
def profile():
	if g.user:
		return render_template('profile.html')

	return render_template('login.html')

@app.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']

@app.route('/getsession')
def getsession():
	if 'user' in session:
		return session['user']
	else:
		return 'Not logged in!'

@app.route('/logout')
def logout():
	session.pop('user', None)
	return 'Logged out!'


@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if g.user:
		if request.method == 'POST':
			file = request.files['photo']
			newFile = Images(name=file.filename, data=file.read())
			db.session.add(newFile)
			db.session.commit()

			return 'Saved ' + file.filename + ' to the database'

		return render_template('upload.html')


	return render_template('login.html')




'''
			filename = photos.save(request.files['photo'])
			return redirect(url_for('uploaded_file', filename=filename))
		return render_template('upload.html')


@app.route('/login', methods=['POST'])
def login():
	if request.form['password'] == 'password' and request.form['username'] == 'admin':
		session['logged_in'] == True
		flash('right password')
	else:
		flash('wrong password!')
	return home()

@app.route('/logout')
def logout():
	session['logged_in'] = False
	return home()
'''

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)