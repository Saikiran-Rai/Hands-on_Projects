import cv2
import mediapipe as mp
import time
import math


class HandDetector:
    def __init__(self, mode=False, max_hands=2, model_comp=1, detection_con=0.5, tracking_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.model_comp = model_comp
        self.detection_con = detection_con
        self.tracking_con = tracking_con

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.model_comp, self.detection_con, self.tracking_con)
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, cam, draw=True):
        cam_rgb = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(cam_rgb)
        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(cam, handLMS, self.mp_hands.HAND_CONNECTIONS)
        return cam

    def find_position(self, cam, hand_no=0, draw=True):
        self.lm_list = []
        xList = []
        yList = []
        bound_box = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for pt, lm in enumerate(my_hand.landmark):
                h, w, c = cam.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                xList.append(cx)
                yList.append(cy)
                self.lm_list.append([pt, cx, cy])
                if draw:
                    cv2.circle(cam, (cx, cy), 7, (255, 0, 0), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bound_box = xmin, ymin, xmax, ymax
            if draw:
                cv2.rectangle(cam, (bound_box[0]-20, bound_box[1]-20), (bound_box[2]+20, bound_box[3]+20), (0, 255, 0), 2)
        return self.lm_list, bound_box

    def findDistance(self, id1, id2, cam, draw=True):
        x1, y1 = self.lm_list[id1][1], self.lm_list[id1][2]
        x2, y2 = self.lm_list[id2][1], self.lm_list[id2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        length = math.hypot(x2 - x1, y2 - y1)

        if draw:
            cv2.circle(cam, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(cam, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.line(cam, (x1, y1), (x2, y2), (255, 0, 0), 3)
            cv2.circle(cam, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
        return length, cam, [x1, y1, x2, y2, cx, cy]

    def fingersUp(self):
        fingers = []
        self.tipIds = [4, 8, 12, 16, 20]
        if self.lm_list[self.tipIds[0]][1] > self.lm_list[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1, 5):
            if self.lm_list[self.tipIds[id]][2] < self.lm_list[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

def main():
    p_time = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, cam = cap.read()
        cam = detector.find_hands(cam)
        lm_list, bound_box = detector.find_position(cam)
        if len(lm_list) != 0:
            print(lm_list[4])
        if not success:
            print("Can't receive frame (stream end?) Exiting...")
            break

        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time

        cv2.putText(cam, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (0, 255, 0), 3)

        cv2.imshow("WEBCAM", cam)
        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == "__main__":
    main()
