import cv2
import numpy as np
from matplotlib import pyplot as plt
from pylab import array, plot, show, axis, arange, figure, uint8
import glob
import os

global RECTANGLE_DISTANCE
global MIN_THRESH_HOLD
global MAX_THRESH_HOLD
global ALPHA 

RECTANGLE_DISTANCE = 100
MIN_THRESH_HOLD = 20
MAX_THRESH_HOLD = 120
ALPHA = 2



def isNumber(x, y, w, h):
    ''' (int x4) check if a rect is a Number
    '''
    return (w > 80) and (h > 300)\
        and (h/w > 1.5) and (h/w < 5)

    pass



def preThreshHold(img, name):
    ''' a little process before threshholding
    '''

    return img


def getNumbers(img, name, threshhold):
    ''' return detected numbers
    '''

    numbers = []
    ret,thresh = cv2.threshold(img,threshhold,255,0)

    _, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,\
                                              cv2.CHAIN_APPROX_SIMPLE)
    i = 0;
    for cnt in contours:
        rect = cv2.boundingRect(cnt)
        x, y, w, h = rect
        i = i + 1
        if isNumber(x, y, w, h):
            ret, numberThresh = cv2.threshold(img[y:y+h, x:x+w], threshhold, 255, 0)
            numbers.append((name + str(i), numberThresh, rect))

    return numbers;




def removeDuplicate(numbers):
    result = []

    def isMatch(rf, rb):
        fx, fy, fw, fh = rf
        bx, by, bw, bh = rb

        return abs(fx - bx) \
                + abs(fy - by)\
                + abs(fw - bw)\
                + abs(fh - bh) < RECTANGLE_DISTANCE

    def mergeImg(a, b):
        w = min(a.shape[0], b.shape[0]) - 1
        h = min(a.shape[1], b.shape[1]) - 1
        return (a[0:w, 0:h] << 1) + (b[0:w, 0:h] << 1)
        
    
    for num in numbers:
        for re in result:
            if (isMatch(num[2], re[2])):
                re =(re[0], mergeImg(re[1], num[1]), re[2])
                break
        else:
            result.append(num)
    return result



imageList = ['inp\\DSC_0012.JPG']

for imgPath in imageList:
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    dir, name = os.path.split(imgPath)


    numbers = []
    for threshold in range(MIN_THRESH_HOLD, MAX_THRESH_HOLD):
        numbers += getNumbers(img, name, threshold)
    
    result = removeDuplicate(numbers)
    i = 0
    
    for imgName, imgOut, _ in result:
        i+=1
        cv2.imwrite('out\\' + name[:-4] + str(i) + '.jpg', imgOut)
        #cv2.imwrite('out\\' + str(i) + '__.jpg', imgOut)
