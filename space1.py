import cv2
import cvzone
import pickle
import tkinter as tk
from my_functions import *
import subprocess
import threading

width = 227
height = 120

# Check if there's already a pickle object    
try:
    with open('CarParkPos1', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:  # Adding
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:  # Deleting
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
    
    # Writing in file f with pickle object
    with open('CarParkPos1', 'wb') as f:
        pickle.dump(posList, f)

def show_image():
    
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", mouseClick)
    while True:
        img = cv2.imread('car4.jpg')
        cvzone.putTextRect(img, 'Press q to see result', (300, 100), scale=1.3, thickness=2, offset=20) 
        for pos in posList:
            draw_rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 255, 255), 2)

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    cv2.destroyAllWindows()
    subprocess.run(["python", "main1.py"])

# Run the OpenCV image display in a separate thread
thread = threading.Thread(target=show_image)
thread.start()

# Start the Tkinter main loop
#root = tk.Tk()
#root.title("Image Selection")

# Start the Tkinter main loop
#root.mainloop()

# Ensure the thread stops when Tkinter window closes
thread.join()
