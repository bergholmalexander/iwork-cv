import cv2
import numpy as np

# def match(image, template):
#     return cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED)

def findPoints(image, threshold, template):
    # img = cv2.imread(args.image_dir+image_path)
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Force greyscale
    res = cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED) #match(img_gray, template)
    # template = cv2.resize(template, (28,25), cv2.INTER_CUBIC)
    w, h = template.shape[::-1]
    loc = np.where( res >= threshold)
    prevPoint = []
    for pt in zip(*loc[::-1]):
        if (pt not in prevPoint): # TODO: Handle near other already found points
            prevPoint.append(pt) # Handle already detected case
    return prevPoint
