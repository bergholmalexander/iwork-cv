import requests, urlHandler, detection, ocr, json, utils, time
from flask import Flask, request, abort
from flask_restful import Resource, Api
from flask_cors import CORS
#import urllib
#import datetime

app = Flask(__name__)
CORS(app)
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
            templates = utils.getTemplates()
            w, h = utils.hwAverage(templates)[::-1]
            # w, h = template.shape[::-1]
        except:
            abort(500, "Internal Server Error: Failed to handle templates")
        try:
            points = detection.findPointsAllTemplates(image, 0.7, templates)
        except:
            abort(500, "Internal Server Error: Template Matching algorithm failed")
        try:
            o = ocr.bulkPointOCR(points, image, w, h)
        except:
            abort(500, "Internal Server Error: OCR failed")
        return o, 200

class Timeout(Resource):
    def get(self):
        # TODO: Error checking i.e. id empty
        time.sleep(60)
        return 200

class GetCoordinatesByURL(Resource):
    def get(self):
        # TODO: Error checking i.e. id empty
        req = request.get_json()
        url = req['url']
        print(url)
        if url == '':
            abort(400, "Bad Request: Invalid URL")
        try:
            image = urlHandler.getGDImage(url)
        except:
            abort(404, "Not Found: Could not download an image at given url")
        try:
            templates = utils.getTemplates()
            w, h = utils.hwAverage(templates)[::-1]
            # w, h = template.shape[::-1]
        except:
            abort(500, "Internal Server Error: Failed to handle templates")
        try:
            points = detection.findPointsAllTemplates(image, 0.5, templates)
        except:
            abort(500, "Internal Server Error: Template Matching algorithm failed")
        try:
            o = ocr.bulkPointOCR(points, image, w, h)
        except:
            abort(500, "Internal Server Error: OCR failed")
        return o, 200

api.add_resource(HelloWorld, '/') # Landing page
api.add_resource(GetCoordinates, '/floors/detect/<string:id>')
api.add_resource(GetCoordinatesByURL, '/floors/detectu')
api.add_resource(Timeout, '/sleep') # make sleep and timeout
#api.add_resource(GetCoordinatesByURL, '/floors/detectu/<string:url>')

if __name__ == '__main__':
    app.run(debug=True)
