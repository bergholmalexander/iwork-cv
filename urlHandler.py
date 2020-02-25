import requests, json
import urllib
import numpy as np
import cv2

def getUrl(id):
    baseURL = 'https://icbc-go-api.herokuapp.com/floors/' # Should we be making this a get request?
    resp = requests.get(baseURL+id)
    url = json.loads(resp.text)["download_url"]
    return url

def getGDImage(url):
    resp = requests.get(url, stream=True)
    resp.raw.decode_content = True
    imgraw = urllib.request.urlopen(url)
    image = np.asarray(bytearray(imgraw.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
    return image
