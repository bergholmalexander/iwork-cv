import glob
import numpy as np
import cv2

def getTemplates(path="templates/"):
    return [cv2.imread(i, 0) for i in glob.glob(path+"*")]

def hwAverage(templates):
    s = [list(row) for row in [t.shape for t in templates]]
    hw = np.mean(s, axis=0)
    return (hw[0], hw[1])
