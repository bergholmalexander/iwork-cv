import cv2, glob, json, pytesseract
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
    mask = np.zeros(image.shape, np.uint8)
    for pt in zip(*loc[::-1]):
        y = np.floor(pt[1] + h/2).astype(int)
        x = np.floor(pt[0] + w/2).astype(int)
        if (mask[y, x] != 255): # TODO: Handle near other already found points
            mask[pt[1]:pt[1]+h, pt[0]:pt[0]+w] = 255
            prevPoint.append((x,y)) # Handle already detected case
        # prevPoint.append((x,y))
    return prevPoint

def findPointsAllTemplates(image, threshold, templates):
    # templates = glob.glob("./templates/*")
    results = []
    for template in templates:
        # template = cv2.imread(t,0)
        results.append(cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED))
    # res = cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED) #match(img_gray, template)
    prevPoint = []
    for res in results:
        w, h = template.shape[::-1]
        loc = np.where( res >= threshold)
        mask = np.zeros(image.shape, np.uint8)
        for pt in zip(*loc[::-1]):
            y = np.floor(pt[1] + h/2).astype(int)
            x = np.floor(pt[0] + w/2).astype(int)
            if ((x,y) not in prevPoint and mask[y, x] != 255): # TODO: Handle near other already found points
                mask[pt[1]:pt[1]+h, pt[0]:pt[0]+w] = 255
                prevPoint.append((x,y)) # Handle already detected case
    return prevPoint

def OCR(image):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format
    text = pytesseract.image_to_string(img_rgb, lang='eng',
                        config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789ABC')
    return text

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)
