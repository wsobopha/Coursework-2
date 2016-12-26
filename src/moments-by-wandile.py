from flask import Flask, render_template, redirect, url_for, abort, request

app = Flask(__name__)

@app.route("/")
def home():
	return "Hello, welcome to Home"

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)