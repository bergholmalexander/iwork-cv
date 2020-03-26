import glob
import numpy as np
import cv2

def getTemplates(path="templates/"):
    print(glob.glob(path+"*"))
    return [cv2.imread(i, 0) for i in ['templates/templateloc2.jpg', 'templates/template3.jpg', 'templates/template1.jpg']] # On local ['templates/templateloc2.jpg', 'templates/template3.jpg', 'templates/template1.jpg']
    #will fix to not be hardcoded later --> glob.glob(path+"*")
def hwAverage(templates):
    s = [list(row) for row in [t.shape for t in templates]]
    hw = np.mean(s, axis=0)
    return (hw[0], hw[1])
