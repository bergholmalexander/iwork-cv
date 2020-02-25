from flask import Flask, request
from flask_restful import Resource, Api
import requests
import urllib

app = Flask(__name__)
#api = Api(app)
@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
