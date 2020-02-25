from flask import Flask, request
from flask_restful import Resource, Api
import requests
import urllib
import urlHandler
import detection

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'about': 'Hello World!'}

class GetCoordinates(Resource):
    def get(self, id):
        # Check if floorId is empty
        url = getUrl(id)
        # baseURL = 'https://icbc-go-api.herokuapp.com/floors/' # Should we be making this a get request?
        # resp = requests.get(baseURL+id)
        # url = json.loads(resp.text)["download_url"]
        # decodedURL = urllib.parse.unquote(id) handled in loads
        image = getGDImage(url)
        template = getGDImage('https://drive.google.com/uc?export=download&id=1FLqmm12Q3DEM_Ae7QfDHl8HOZeO_-Ffr')
        # resp = requests.get(url, stream=True)
        # resp.raw.decode_content = True
        # test = urllib.request.urlopen(url)
        # image = np.asarray(bytearray(test.read()), dtype="uint8")
        # image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
        points = findPoints(image, 0.5, template)
        return {'coordinates': points}

api.add_resource(HelloWorld, '/') # Landing page
api.add_resource(getCoordinates, '/floors/detect/<str:id>') # Landing page

if __name__ == '__main__':
    app.run(debug=True)
