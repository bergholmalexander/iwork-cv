from flask import Flask, request, abort
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
        if id == "":
            abort(400, "Bad Request: No id was entered")
        try:
            url = urlHandler.getUrl(id)
        except:
            abort(404, "Not Found: Could not find url for given id")
        try:
            image = urlHandler.getGDImage(url)
        except:
            abort(404, "Not Found: Could not download an image at given url")
        try:
            template = urlHandler.getGDImage('https://drive.google.com/uc?export=download&id=1FLqmm12Q3DEM_Ae7QfDHl8HOZeO_-Ffr')
        except:
            abort(404, "Not Found: Could not download template at given url")
        try:
            points = detection.findPoints(image, 0.5, template)
        except:
            abort(500, "Internal Server Error: Template Matching algorithm failed")
        return {'coordinates': points}, 200

api.add_resource(HelloWorld, '/') # Landing page
api.add_resource(GetCoordinates, '/floors/detect/<string:id>') # Landing page

if __name__ == '__main__':
    app.run(debug=True)
