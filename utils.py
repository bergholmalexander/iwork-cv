import glob
import numpy as np
import cv2

def getTemplates(path="templates/"):
    return [cv2.imread(i, 0) for i in ['templates/templateloc2.jpg', 'templates/template3.jpg', 'templates/template2.jpg', 'templates/template1.jpg']]
    # glob.glob(path+"*") because apparently ordering might matter?

def hwAverage(templates):
    s = [list(row) for row in [t.shape for t in templates]]
    hw = np.mean(s, axis=0)
    return (hw[0], hw[1])
