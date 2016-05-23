import cv2
import numpy as np
from PIL import Image

import glob, os 
import getopt
import sys
import pytesseract

THRESH_HOLD = 81
THRESH_HOLD_BOX = 99

def isNumber(x, y, w, h, shape):
    ''' return True if a rect bounds a number
    '''    
    result = True
    result &= (x > 30) and (shape[1] - x > w + 150)
    result &= (y > 10) and (shape[0] - y > h + 20)

    result &= ( w > 80 ) and ( h > 300 ) and ( w < 400 ) and ( h < 1000 )

    ratio = float(h) / float(w)
    result &= ratio == sorted((1, ratio, 5))[1]
    return result

def preThreshHold(img, name):
    ''' a little process before threshholding
    '''
    img = cv2.equalizeHist(img)
    return img

def getNumbers(img, name, threshhold):
    # normal threshHold
    #ret1, thresh = cv2.threshold(img, threshhold, 255, cv2.THRESH_BINARY)
    # adaptive threshHold
    thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, THRESH_HOLD_BOX,8)
    cv2.imwrite('threshHold/' + name + '.tiff', thresh)

    _, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    imT = thresh.copy()
    outImg = np.zeros(img.shape, np.uint8)
    outImg += 255

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if isNumber(x, y, w, h, img.shape):
            cv2.rectangle(imT,(x,y),(x+w,y+h),(0,255,0),5)
            outImg[y:y + h, x:x + w] = thresh[y:y + h, x:x + w]
            cv2.drawContours(outImg, [cnt], 0, (125, 125, 125), 5 )

    cv2.imwrite('out/' + name + '.tiff', outImg)
    cv2.imwrite( 'contour/' + name + '.tiff', imT )

    height, width = outImg.shape
    outImg = cv2.resize( outImg, ( 400, 400 * height / width ) )

    image = Image.fromarray( outImg )
    print pytesseract.image_to_string( image, config = "-psm 6 config" )

def crop(inp, out):
    imageList = glob.glob(inp)
    for imgPath in imageList:
        print imgPath, ' : '
        img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize( img, ( 2048, 1536 ) )
        dir, name = os.path.split(imgPath)
        img = preThreshHold(img, name)
        cv2.imwrite('equalizeHist/' + name[:-4] + '.tiff', img )
        getNumbers(img, name[:-4], THRESH_HOLD)


def showHelp():
    ''' Show help of the module
    '''
    print '\n',\
        'USAGE : python Tesseract.py [-i INPUT_FILE(S)] [-o OUTPUT_DIRECTORY]\n', \
        '   -i INPUT_FILES\n', \
        '       set input files, may be (*.jpg *.tiff *.png)\n', \
        '   -o OUTPUT_DIRECTORY\n', \
        '       set output directory (will be created if not exists)\n\n', \
        'EXAMPLE :\n', \
        '    python Tesseract.py -i inp/*.jpg -o out/\n\n', \
        'INPUT_FILE(s) is a list of license plate images( should have the same name extension ).\n\n',\
        'OUTPUT_DIRECTORY should be images of readable numbers and character, which are forward\n',\
        '    to Tesseract OCR to get the plates.\n\n',\
        'The accuracy of our detection is equivalent to how clear the input is.\n\n',


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
            showHelp()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFile = arg
        elif opt in ("-o", "--ofile"):
            outputDir = arg
    if ( inputFile == '' ):
        inputFile = 'inp/*.jpg'
    if ( outputDir == '' ):
        outputDir = 'out/'
    crop(inputFile, outputDir)
    pass

if __name__ == "__main__":    
    main(sys.argv[1:])