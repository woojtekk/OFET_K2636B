import numpy as np
import cv2

img = cv2.imread('image2.png')
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy= cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# print(cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE))

print(contours)

#cv2.drawContours(img, contours, 3, (0,255,0), 3)


#cv2.imshow("Robust", img)
#cv2.waitKey(0),


