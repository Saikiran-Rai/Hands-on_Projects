# IMPORTS
import cv2
import easyocr
from ultralytics import YOLO

# CAPTURING VIDEO
my_vid = cv2.VideoCapture("../Resources/sample_video.mp4")

# DEFINING YOLO-V8 MODEL
model = YOLO("../Projects/yolov8n.pt")


while True:
    success, vid = my_vid.read()
    if not success:
        print("Can't receive frame (stream end?). Exiting...")
        break

    # REDUCING THE RESOLUTION OF THE VIDEO
    resized_vid = cv2.resize(vid, (640, 480))

    # PROCESSING THE CAPTURED VIDEO BY YOLO MODEL
    yolo_results = model(resized_vid, stream=True)

    for result in yolo_results:

        # OBTAINING EVERY OBJECT IN THE VIDEO FRAME
        img = result.orig_img
        # img = cv2.resize(img, (256, 256))

        # Apply OCR to cropped_image
        reader = easyocr.Reader(['en'], gpu=False)
        ocr_result = reader.readtext(img)
        for r in ocr_result:
            bound_box, text, score = r

            cv2.rectangle(img, bound_box[0], bound_box[2], (0, 255, 0), 2)
            cv2.putText(img, text, bound_box[0], cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (255, 0, 0), 2)
    cv2.imshow("VIDEO", resized_vid)
    if cv2.waitKey(1) == ord('q'):
        break


