import cv2
import numpy as np
from matplotlib import pyplot as plt
from pylab import array, plot, show, axis, arange, figure, uint8
import glob
import os

THRESH_HOLD = 100

def isNumber(x, y, w, h, shape):
    ''' return True if a rect bounds a number
    '''
    result = True

    result &= w < shape[1]*.6
    result &= h < shape[0]*.6
    
    result &= (x > 5) and (shape[1] - x > w + 10)
    result &= (y > 5) and (shape[0] - y > h + 10)

    result &= (w > 150) and (h > 300)

    ratio = float(h) / float (w)
    result &= ratio == sorted((1.7, ratio, 4.0))[1]

    return result

def toOtherCor(x,y, w, h, shape):
    lx = shape[1] - (x + w)
    ly = shape[0] - (y + h)

    rx = lx + w
    ry = ly + h
     
    return str.format("{0} {1} {2} {3} 0\n" ,lx, ly, rx, ry)

def preThreshHold(img, name):
    ''' a little process before threshholding
    '''
    img = cv2.equalizeHist(img)
        
    clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(12,12))
    img = clahe.apply(img)    
    return img



def getNumbers(img, name, threshhold):    
    ret1,thresh = cv2.threshold(img,threshhold,255,cv2.THRESH_BINARY)

    _, contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_TREE,\
                                              cv2.CHAIN_APPROX_SIMPLE)
        
    outImg = np.zeros(img.shape, np.uint8)
    outImg += 255
    fo = open('out\\' + name + '.txt', 'w')
        
    for cnt in contours:
        rect = cv2.boundingRect(cnt)
        x, y, w, h = rect
        if isNumber(x, y, w, h, img.shape):
            #cv2.rectangle(outImg, (x, y), (x + w, y + h), (0,0,0),2)
            hull = cv2.convexHull(cnt)
            
            outImg[y: y+h, x : x + w] = thresh[y:y+h, x:x+w]
            cv2.drawContours(outImg, [cnt], 0, (125, 125, 125), 5)
            fo.write(toOtherCor(x,y,w,h,img.shape))
    fo.close()
    cv2.imwrite('out\\' + name + '.tiff', outImg)


#imageList = ['inp\\DSC_0002.JPG']
imageList = glob.glob("inp\\*.JPG")


for imgPath in imageList:
    glbCount = 0
    print imgPath , ' : '
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)

    dir, name = os.path.split(imgPath)    
    img = preThreshHold(img, name)
    getNumbers(img, name[:-4], THRESH_HOLD)