# IMPORTING LIBRARIES
import cv2
import numpy as np
import time
import HandTrackingModule as htm
import pyautogui as pg
import tkinter as tk

# CAPTURING WEBCAM
cap = cv2.VideoCapture(0)

# DECLARING VARIABLES
pTime = 0
frameR = 50  # frame reduction
smoothening = 2
cLocX, pLocX, cLocY, pLocY = 0, 0, 0, 0

# SETTING SIZE OF CAM AND FINDING SIZE OF SCREEN
wcam, hcam = 640, 480
cap.set(3, wcam)
cap.set(4, hcam)

root = tk.Tk()
wscr = root.winfo_screenwidth()
hscr = root.winfo_screenheight()

detector = htm.HandDetector(detection_con=0.7, tracking_con=0.7, max_hands=1)

while True:
    success, cam = cap.read()

    # FINDING HAND LANDMARKS
    cam = detector.find_hands(cam)
    lm_list, boundbox = detector.find_position(cam)

    # GETTING THE TIP OF INDEX AND MIDDLE FINGERS
    if len(lm_list) != 0:
        area = ((bound_box[2]-bound_box[0])*(bound_box[3]-bound_box[1]))//100
        if (area > 300) and (area < 1400):
            x1, y1 = lm_list[8][1:]
            x2, y2 = lm_list[12][1:]
            cv2.rectangle(cam, (frameR, frameR), (wcam-frameR, hcam-frameR), (0, 255, 0), 2)
    
            # CONVERTING COORDINATES FROM CAM SIZE TO SCREEN SIZE
            fingers = detector.fingersUp()
            if fingers[1] == 1 and fingers[2] == 0:
                x3 = np.interp(x1, (frameR, wcam-frameR), (0, wscr))
                y3 = np.interp(y1, (frameR, hcam-frameR), (0, hscr))
    
                # SMOOTHENING MOVEMENT
                cLocX = pLocX + (x3 - pLocX) / smoothening
                cLocY = pLocY + (y3 - pLocY) / smoothening
    
                # MOVING MOUSE
                pg.moveTo(wscr-cLocX, cLocY)
                cv2.circle(cam, (x1, y1), 10, (0, 255, 0), 3, cv2.FILLED)
                pLocX, pLocY = cLocX, cLocY
    
            # FOR LEFT CLICK
            if fingers[1] == 1 and fingers[2] == 1:
                length, cam, fd_info = detector.findDistance(8, 12, cam)
                if length < 40:
                    cv2.circle(cam, (fd_info[4], fd_info[5]), 10, (0, 255, 0), 3, cv2.FILLED)
                    pg.click(button="left", interval=0.5)
    
            # FOR RIGHT CLICK
            '''
            if fingers[1] == 1 and fingers[4] == 1:
                length, cam, fd_info = detector.findDistance(8, 4, cam)
                if length < 30:
                    cv2.circle(cam, (fd_info[4], fd_info[5]), 10, (0, 255, 0), 3, cv2.FILLED)
                    pg.rightClick(interval=0.5)'''

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(cam, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255, 0, 0), 3)

    cv2.imshow("WEBCAM", cam)

    if cv2.waitKey(1) == ord('q'):
        break
