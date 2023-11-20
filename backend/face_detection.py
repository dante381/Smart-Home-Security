import pandas as pd
from deepface import DeepFace
import cv2 as cv
import firebase_admin
from firebase_admin import credentials, messaging

firebase_cred = credentials.Certificate(
    "E:\\Projects\\yolov5surveillance-20230808T135321Z-001\\backend\\smarthomesecurity-3e445-firebase-adminsdk-5w238-9ab3a99e6e.json")
firebase_app = firebase_admin.initialize_app(firebase_cred)

message = messaging.Message(
    notification=messaging.Notification(
        title="SmartHomeSecurity",
        body="Unknown Person Detected"
    ),
    token="dgI5zjDyRjWGVgllHZ2lFP:APA91bF5ukohuMan3tLGE4nvgwPt8AUirajc0Xhldgt3WGBf32tabiRMvB-paydDoq13zJlFYEzws7MQ2aV714gHKFrPu6DeBul8yUOxq4zPvGhotsKOjPLUe3DHpsyGP-o617kQjy2I"
)

# from google.colab.patches import cv2_imshow


face_cascade = cv.CascadeClassifier(
    cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

# cap = video.VideoStream('rtsp://192.168.1.30:8080/h264.sdp').start()
cap = cv.VideoCapture(0)
# cap.set(cv.CAP_PROP_FRAME_WIDTH, 160)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, 120)

count = 0

while True:
    (grabbed, frame) = cap.read()
    # frame = cap.read()
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    faces = face_cascade.detectMultiScale(rgb, scaleFactor=1.1, minNeighbors=5)
    # frame = cv.resize(frame, (640, 480))
    frame = cv.flip(frame, 1)
    # print(frame.shape)
    for (x, y, w, h) in faces:
        color = (0, 255, 255)
        strokes = 2

        cv.rectangle(frame, (x, y), (x+w, y+h), color, strokes)
        dfs = DeepFace.find(img_path=frame[y:y+h, x:x+w], db_path='E:\\Projects\\yolov5surveillance-20230808T135321Z-001\\backend\\Databases',
                            enforce_detection=False, detector_backend="opencv")
        # print(dfs)
        if (len(dfs[0]) == 0 or dfs[0].loc[0]['VGG-Face_cosine'] >= 0.1):
            print("ERROR")
            count += 1
            if (count > 10):
                print("UNKNOWN PERSON DETECTED")
                count = 0
                messaging.send(message)
        else:
            count = 0

    # frame=cv.resize(frame,(600,400))
    cv.imshow('Frame', frame)
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break
cap.release()
cv.waitKey(1)
cv.destroyAllWindows()
