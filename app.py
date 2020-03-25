from flask import Flask, request, abort
from flask_restful import Resource, Api
import requests
import urllib
import urlHandler
import detection
import ocr
import json
import utils

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
            templates = utils.getTemplates()
            w, h = utils.hwAverage(templates)[::-1]
            # w, h = template.shape[::-1]
        except:
            abort(500, "Internal Server Error: Failed to handle templates")
        try:
            points = detection.findPointsAllTemplates(image, 0.8, templates)
        except:
            abort(500, "Internal Server Error: Template Matching algorithm failed")
        try:
            o = ocr.bulkPointOCR(points, image, w, h)
        except:
            abort(500, "Internal Server Error: OCR failed")
        return o, 200

# class GetCoordinatesByURL(Resource):
#     def get(self, url):
#         try:
#             image = urlHandler.getGDImage(url)
#         except:
#             abort(404, "Not Found: Could not download an image at given url")
#         try:
#             templates = utils.getTemplates()
#             w, h = utils.hwAverage(templates)[::-1]
#         except:
#             abort(404, "Not Found: Could not download template at given url")
#         try:
#             points = detection.findPointsAllTemplates(image, 0.6, templates)
#         except:
#             abort(500, "Internal Server Error: Template Matching algorithm failed")
#         try:
#             o = ocr.bulkPointOCR(points, image, w, h)
#         except:
#             abort(500, "Internal Server Error: OCR failed")
#         return o, 200

api.add_resource(HelloWorld, '/') # Landing page
api.add_resource(GetCoordinates, '/floors/detect/<string:id>')
#api.add_resource(GetCoordinatesByURL, '/floors/detectu/<string:url>')

if __name__ == '__main__':
    app.run(debug=True)
