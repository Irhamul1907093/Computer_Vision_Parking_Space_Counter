import cv2
import pickle
import cvzone
import numpy as np
from my_functions import *
#from practice import *

# Load the image
#img = cv2.imread('carParkImg.png', cv2.IMREAD_GRAYSCALE)
'''why not work on reading this line'''
width = 227
height = 120

#no need for try there's at least a file
with open('CarParkPos1', 'rb') as f:
        posList = pickle.load(f)

def checkBlankSpace(imgcheck):
    spaceCounter = 0
    for pos in posList:
        x,y =pos
        
        imgCrop = imgcheck[y:y + height, x:x + width]
        #cv2.imshow(str(x * y), imgCrop) #imgname should be unique so doesn't overlap
        count = my_count_nonzero(imgCrop)

        if count < 900:
            color = (255, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2
        
        draw_rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=2, offset=0)
        cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                           thickness=5, offset=20, )

img = cv2.imread('car4.jpg')

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = my_gaussian_blur(imgGray, 3, 1) #kernel size,sigma size check

# Parameters for adaptive thresholding
max_value = 255
adaptive_method = 'gaussian'  
threshold_type = 'binary_inv'   
block_size = 25
C = 16

img_threshold = my_adaptive_threshold(imgBlur, max_value, adaptive_method, threshold_type, block_size, C)
imgMedian = my_median_filter(img_threshold, 5) #remove salt pepper noise
kernel = np.ones((3, 3), np.uint8)
imgDilate = my_dilate(imgMedian, kernel, iterations=1) #to make thicker to count easy
         
checkBlankSpace(imgDilate)

for pos in posList:
    draw_rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 255, 255), 2)
cv2.imshow("Image", img)
cv2.imshow("ImageBlur", imgBlur)
cv2.imshow("ImageThresholded", img_threshold)
cv2.imshow("ImageMedian", imgMedian)
cv2.imshow("ImageDialet", imgDilate)
cv2.waitKey()
