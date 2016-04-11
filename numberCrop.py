import cv2
import numpy as np
from matplotlib import pyplot as plt
from pylab import array, plot, show, axis, arange, figure, uint8
import glob
import os

def loadImage(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)    
    return img


def checkSize(w, h):
    return (w > 80) and (h > 300)\
        and (h/w > 1.5) and (h/w < 5)

def getNumbers(img, name, threshHold, isBest = False):
    numbers = []    
    ret,thresh = cv2.threshold(img,threshHold,255,0)            
    if (isBest):
        cv2.imwrite(name + str(threshHold) + 'thresh.jpg', thresh)
    _, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,
                                              cv2.CHAIN_APPROX_SIMPLE)
    i = 0;
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        i = i + 1
        if checkSize(w, h):
            ret, numberThresh = cv2.threshold(img[y:y+h, x:x+w], threshHold, 255, 0)
            numbers.append((name + str(i), numberThresh))

    return numbers;

def getMaxNumbers(img, name):
    result = []
    bestTH = 60
    for threshHold in range(50, 100):
        numbers = getNumbers(img, name, threshHold)
        if (len(result) < len(numbers)):
            result = numbers
            bestTH = threshHold
    getNumbers(img, name, bestTH, True)
    return result


def writeOut(name, img):
    cv2.imwrite('out\\' + name + '.jpg', img)
    fo = open('out\\' + name + '.txt', 'w')
    heigh, width = img.shape
    fo.write('0 0 ' + str(width) + ' ' + str(heigh))
    fo.close()

#imageList = ["inp\\DSC_0012.JPG"] 
imageList = glob.glob("inp\\*.JPG")

for imgPath in imageList:
    
    img = loadImage(imgPath)       
    dir, name = os.path.split(imgPath)    
    numbers = getMaxNumbers(img, name)
    for name, number in numbers:
        writeOut(name, number)

exit()