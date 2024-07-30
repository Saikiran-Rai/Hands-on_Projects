# IMPORTING REQUIRED LIBRARIES
import cv2
import time
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import HandTrackingModule as htm

# CAPTURING WEBCAM
cap = cv2.VideoCapture(0)
# cap.set(3, 1920)
# cap.set(4, 1080)
detector = htm.HandDetector(max_hands=1)
ptime = 0

# SETTING AUDIO FUNCTIONALITIES
device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volRange = volume.GetVolumeRange()
vol = 0
vol_bar = 400
vol_per = 0
area = 0

while True:
    success, cam = cap.read()
    cam = detector.find_hands(cam)

    # FINDING POSITION OF THE HAND AND MAKING BOUNDING BOX
    lm_list, bound_box = detector.find_position(cam, draw=True)
    if len(lm_list) != 0:
        area = ((bound_box[2]-bound_box[0])*(bound_box[3]-bound_box[1]))//100
        if (area > 300) and (area < 1400):

            # FINDING DISTANCE BETWEEN THUMB AND INDEX FINGERS
            length, cam, fd_info = detector.findDistance(4, 8, cam)

            # CONVERTING DISTANCE BETWEEN TWO FINGERS TO VOLUME
            # my hand range is 25 to 175
            vol_bar = np.interp(length, [25, 175], [400, 150])
            vol_per = np.interp(length, [25, 175], [0, 100])

            # REDUCING RESOLUTION TO MAKE IT SMOOTHER
            smoothness = 10
            vol_per = smoothness * round(vol_per/smoothness)

            # SETTING VOLUME IF PINKY FINGER IS DOWN
            fingers = detector.fingersUp()
            if fingers[4] == 0:
                volume.SetMasterVolumeLevelScalar(vol_per/100, None)
                cv2.circle(cam, (fd_info[4], fd_info[5]), 10, (0, 255, 0), cv2.FILLED)

    # DRAWINGS
    cv2.rectangle(cam, (50, 150), (80, 400), (0, 255, 0), 3)
    cv2.rectangle(cam, (50, int(vol_bar)), (80, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(cam, f'{int(vol_per)}%', (50, 130), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)
    curr_vol = int(volume.GetMasterVolumeLevelScalar()*100)
    cv2.putText(cam, f'Volume Set:{curr_vol}', (400, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)

    # FRAME RATE
    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime
    cv2.putText(cam, f'FPS:{int(fps)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)

    if not success:
        print("Can't receive frame (stream end?) Exiting...")
        break
    cv2.imshow("WEBCAM", cam)
    if cv2.waitKey(1) == ord('q'):
        break
