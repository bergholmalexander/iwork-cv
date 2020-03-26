import requests, urlHandler, detection, ocr, json, utils, time
from flask import Flask, request, abort
from flask_restful import Resource, Api
from flask_cors import CORS
from redis import Redis
from worker import conn
import rq

#import urllib
#import datetime

app = Flask(__name__)
CORS(app)
api = Api(app)
q = rq.Queue(connection=conn)

# CONFIG
threshold = 0.5

class HelloWorld(Resource):
    def get(self):
        return {'about': 'Hello World!'}

class GetCoordinates(Resource):
    def get(self, id):
        # TODO: Error checking i.e. id empty
        job = q.enqueue(performCVByID, id)
        return job.get_id(), 201

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

class Ping(Resource):
    def get(self, id):
        # TODO: Error checking i.e. id empty
        try:
            rq_job = rq.job.Job.fetch(id, connection=conn) # If bug, probably connection=conn
        except: #(redis.exceptions.RedisError, rq.exceptions.NoSuchJobError)
            abort(400, "Bad Request: ID was not found")
        if rq_job.is_finished:
            if rq_job.result[0] != 200:
                abort(rq_job.result[0], rq_job.result[1])
            return rq_job.result[1], 200
        else:
            return "Incomplete task", 202

api.add_resource(HelloWorld, '/') # Landing page
api.add_resource(GetCoordinates, '/floors/detect/<string:id>')
api.add_resource(GetCoordinatesByURL, '/floors/detectu')
api.add_resource(Timeout, '/sleep') # make sleep and timeout
api.add_resource(Ping, '/ping/<string:id>') # make sleep and timeout
#api.add_resource(GetCoordinatesByURL, '/floors/detectu/<string:url>')

def performCVByID(id):
    if id == "":
        return (400, "Bad Request: No id was entered") #abort(400, "Bad Request: No id was entered")
    try:
        url = urlHandler.getUrl(id)
    except:
        return (404, "Not Found: Could not find url for given id")
    try:
        image = urlHandler.getGDImage(url)
    except:
        return (400, "Not Found: Could not download an image at given url")
    try:
        templates = utils.getTemplates()
        w, h = utils.hwAverage(templates)[::-1]
        # w, h = template.shape[::-1]
    except:
        return (500, "Internal Server Error: Failed to handle templates")
    try:
        points = detection.findPointsAllTemplates(image, threshold, templates)
    except:
        return (500, "Internal Server Error: Template Matching algorithm failed")
    try:
        o = ocr.bulkPointOCR(points, image, w, h)
    except:
        return (500, "Internal Server Error: OCR failed")
    return (200, o)

def performCVByURL(url):
    try:
        image = urlHandler.getGDImage(url)
    except:
        return (400, "Not Found: Could not download an image at given url")
    try:
        templates = utils.getTemplates()
        w, h = utils.hwAverage(templates)[::-1]
        # w, h = template.shape[::-1]
    except:
        return (500, "Internal Server Error: Failed to handle templates")
    try:
        points = detection.findPointsAllTemplates(image, threshold, templates)
    except:
        return (500, "Internal Server Error: Template Matching algorithm failed")
    try:
        o = ocr.bulkPointOCR(points, image, w, h)
    except:
        return (500, "Internal Server Error: OCR failed")
    return (200, o)

if __name__ == '__main__':
    app.run(debug=True)
