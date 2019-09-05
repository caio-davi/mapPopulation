#!/usr/bin/env python
from flask import Flask, render_template, make_response, request
from flask_json import FlaskJSON, JsonError, json_response
from flask_cors import CORS

app = Flask(__name__, instance_relative_config=True)

FlaskJSON(app)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')
