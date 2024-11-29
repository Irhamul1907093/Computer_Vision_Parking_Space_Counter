import cv2
import pickle
from my_functions import *
#for picture car2.jpg
#width=282-43
#height=180-44

#for carparkimg.png
width = 107
height = 48
#check if there's already a pickle object    
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN: #adding
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:  #delete
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
    
    #writing in file f with pickle object
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)
   

#while True:
    #cv2.rectangle(img, (43,44), (282, 180), (0, 255, 255), 2)  #(pathailla,upure niche)

    #cv2.imshow("Image", img)
    #cv2.waitKey(1)
    #----------------
while True:
    img = cv2.imread('carparkimg.png') 
    for pos in posList:
        draw_rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 255, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image",mouseClick)
    cv2.waitKey(1)
   # cv2.destroyAllWindows()