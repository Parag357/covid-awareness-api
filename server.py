from flask import Flask, render_template, jsonify
import os
import scrapper

app = Flask(__name__, template_folder=".", static_folder='assets')


@app.route('/')
def index():
    return "This is an API for covid-19-awarness site."


@app.route('/stats')
def stats():
    return jsonify(scrapper.scrap_stats())


@app.route('/news')
def news():
    return jsonify(scrapper.scrap_news())


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


port = int(os.environ.get('PORT', 8000))
app.run(host='0.0.0.0', port=port, debug=False)
