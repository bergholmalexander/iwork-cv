from flask import Flask, request
from flask_restful import Resource, Api
import requests
import urllib
import urlHandler
import detection
import json

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'about': 'Hello World!'}

class GetCoordinates(Resource):
    def get(self, id):
        # TODO: Error checking i.e. id empty
        url = urlHandler.getUrl(id)
        image = urlHandler.getGDImage(url)
        template = urlHandler.getGDImage('https://drive.google.com/uc?export=download&id=1FLqmm12Q3DEM_Ae7QfDHl8HOZeO_-Ffr')
        points = detection.findPoints(image, 0.5, template)
        print(points)
        return {'coordinates': points}

api.add_resource(HelloWorld, '/') # Landing page
api.add_resource(GetCoordinates, '/floors/detect/<string:id>') # Landing page

if __name__ == '__main__':
    app.run(debug=True)
