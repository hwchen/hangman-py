#! /usr/bin/env python3

# test server, serves one json file

from flask import Flask, jsonify

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/data')
def data():
    data = {"sessionID": 10, "sessionWins": 4, "sessionLosses": 3, "current": "**rh**", "wrong": 8}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
