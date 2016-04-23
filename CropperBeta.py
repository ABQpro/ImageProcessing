import cv2
import numpy as np

import glob, os 
import getopt
import sys


THRESH_HOLD = 100


def isNumber(x, y, w, h, shape):
    ''' return True if a rect bounds a number
    '''    
    result = True
    result &= w < shape[1] * .6
    result &= h < shape[0] * .6
    result &= (x > 5) and (shape[1] - x > w + 10)
    result &= (y > 5) and (shape[0] - y > h + 110)

    result &= (w > 150) and (h > 300)

    ratio = float(h) / float(w)
    result &= ratio == sorted((1.7, ratio, 4.0))[1]
    return result


def toOtherCor(x, y, w, h, shape):
    '''
    '''

    lx = shape[1] - (x + w)
    ly = shape[0] - (y + h)

    rx = lx + w
    ry = ly + h

    return str.format("{0} {1} {2} {3} 0\n", lx, ly, rx, ry)


def preThreshHold(img, name):
    ''' a little process before threshholding
    '''
    img = cv2.equalizeHist(img)

    clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(12, 12))

    img = clahe.apply(img)
    return img


def getNumbers(img, name, threshhold):
    '''
    '''
    ret1, thresh = cv2.threshold(img, threshhold, 255, cv2.THRESH_BINARY)

    contours, hierarchy = \
         cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    outImg = np.zeros(img.shape, np.uint8)
    outImg += 255
    fo = open('out/' + name + '.txt', 'w')

    for cnt in contours:
        rect = cv2.boundingRect(cnt)
        x, y, w, h = rect
        if isNumber(x, y, w, h, img.shape):
            outImg[y:y + h, x:x + w] = thresh[y:y + h, x:x + w]

            cv2.drawContours(outImg, [cnt], 0, (125, 125, 125), 5)
            fo.write(toOtherCor(x, y, w, h, img.shape))
    fo.close()
    cv2.imwrite('out/' + name + '.tiff', outImg)


#imageList = ['inp\\DSC_0002.JPG']
#imageList = glob.glob("inp\\*.JPG")

def crop(inp, out):
    '''
    '''
    imageList = glob.glob(inp)
    for imgPath in imageList:
        #glbCount = 0
        print imgPath, ' : '
        img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)

        dir, name = os.path.split(imgPath)
        img = preThreshHold(img, name)
        getNumbers(img, name[:-4], THRESH_HOLD)


def showHelp():
    ''' Show help of the module
    '''
    print '\n\n',\
        'USAGE : python CropperBeta.py [-i INPUT_FILE(S)] [-o OUTPUT_DIRECTORY]\n\n', \
        '    -i INPUT_FILES\n', \
        '        set input files, may be (*.jpg *.tiff *.png)\n\n', \
        '    -o OUTPUT_DIRECTORY\n', \
        '        set output directory (will be created if not exists)\n\n', \
        'example :\n', \
        '    python CropperBeta.py -i inp/*.jpg -o out/', \
        '\n\n'


def main(argv):
    inputFile = ''
    outputDir = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFile = arg
        elif opt in ("-o", "--ofile"):
            outputDir = arg
  
    #if (inputFile == '' or outputDir == ''):
     #   showHelp()
    #else:
    #crop(inputFile, outputDir)
    crop('inp/*.JPG', 'out/')
    pass

if __name__ == "__main__":    
    main(sys.argv[1:])
