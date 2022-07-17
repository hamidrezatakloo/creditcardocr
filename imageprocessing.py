import cv2
import pytesseract
import imutils
from imutils import contours
import numpy as np
import re
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
img = cv2.imread('T.jpeg')
img = imutils.resize(img, width=600)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(20,6))
rectKernel1 = cv2.getStructuringElement(cv2.MORPH_RECT,(8,8))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
Blackhat = cv2.morphologyEx(img,cv2.MORPH_BLACKHAT,rectKernel)
gradX = cv2.Sobel(Blackhat, ddepth=cv2.CV_32F, dx=1, dy=0,
	ksize=-1)
gradX = np.absolute(gradX)
(minVal, maxVal) = (np.min(gradX), np.max(gradX))
gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
gradX = gradX.astype("uint8")
gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel1)
thresh = cv2.threshold(gradX, 0, 255,cv2.THRESH_BINARY |cv2.THRESH_OTSU)[1]
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, sqKernel)
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
locs = []


for (i, c) in enumerate(cnts):
    (x, y, w, h) = cv2.boundingRect(c)
    ar = w / float(h)
    if ar > 2 :
        if (w > 50 ) and (w < 130 ) and (h > 10 ):
            locs.append((x, y, w, h))

locs = sorted(locs, key=lambda x:x[0])
output = []
H = []
for (i, (gX, gY, gW, gH)) in enumerate(locs):
	group = Blackhat[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]
	group = cv2.threshold(group, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	H.append(group)
text = pytesseract.image_to_string(img)
print(text)

cardnumber = ''
cv2 = None
for x in range(len(H)):
    t = pytesseract.image_to_string(H[x],config='--psm 7')
    if t!='' and t.lower()[0] == 'c':
        cv2=t
    if re.match(r'\d\d\d\d',t)!=None:   
        cardnumber += str(t).rstrip()
        cardnumber += '\t'
print('cardnumber :\n',cardnumber)

print(cv2 )


