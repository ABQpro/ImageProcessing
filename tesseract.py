from PIL import Image
import pytesseract
import glob
import os

imageList = glob.glob("out\\*.tiff")

for imgPath in imageList:
	print imgPath, ':'
	print pytesseract.image_to_string( Image.open( imgPath ), config = "-psm 6 config" )