"""
Carter Frost
For hosting a website for magic card sorter
"""

# TODO: Website have a view of the bins with the cards 
# ontop of eachother get the url stored in the mtgsdk card class

import logging
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def main():
	mode = "Paused"

	if request.method == 'POST': #update everything
		mode = request.form['mode']
	bins=[0]*16
	with open('static/councils.txt', 'r') as file:
		modes = file.read().split('\n')
	# TODO: get bin names from google spredsheet
	binName = ["Upside Down", "Blue", "Red", "Colorless", "Mixed", "None", "..."]
	return render_template('index.html', modes=modes, mode=mode, bins=bins, table_header=binName)


@app.route('/static/<name>')
def resource(name) :
	"""Load a file from the static directory and return it to the browser."""
	with open ('static/' + name, 'rb') as f:
		return f.read()


@app.errorhandler(500)
def server_error(e):
	""" Just that it is an error handler"""
	print("Borked", e)
	return('I done borked up.', 500)


if __name__ == "__main__":
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(host="0.0.0.0", port=9090)
# app.run(host='::', port=9090, debug=True)

