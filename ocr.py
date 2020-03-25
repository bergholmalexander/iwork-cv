import cv2
import numpy as np
import pytesseract

def bulkPointOCR(points, img, w, h):
    # points = [(1789, 677), (1561, 682), (1556, 847), (1836, 847), (2087, 930), (1291, 934), (1816, 1039), (1317, 1081), (2305, 1113), (1054, 1120), (2061, 1141), (1552, 1226), (1846, 1226), (2170, 1311), (1468, 1426), (1843, 1427), (2239, 1487), (2520, 1563), (1288, 1654), (1499, 1657), (1666, 1659), (2334, 1766), (1027, 1771), (2072, 1941), (1336, 1950), (1705, 2010), (1802, 2093), (1611, 2155), (1933, 2160), (1725, 2161), (1831, 2164)]
    # left here incase it needs to be tested again
    compiled = []
    for p in points:
        print("before match")
        match = cv2.cvtColor(img[p[1]-np.floor(h/2).astype(int):p[1]+np.floor(h/2).astype(int)+1, (p[0]-np.floor(w/2).astype(int)):p[0]+np.floor(w/2).astype(int)+1], cv2.COLOR_BGR2RGB)
        print("after match")
        print("printing match")
        print(match.shape)
        print("printing edges")
        print(img[p[1]-np.floor(h/2).astype(int))
        print(p[1]+np.floor(h/2).astype(int)+1)
        print((p[0]-np.floor(w/2).astype(int)))
        print(p[0]+np.floor(w/2).astype(int)+1])
        text = pytesseract.image_to_string(match,
                            config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789ABC')
        if text == "":
            print("cannot find anything in this case!")
        else:
            print(text)
        compiled.append({"x": int(p[0]), "y": int(p[1]), "workspace_name": text})
    return compiled
