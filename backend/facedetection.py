import cv2 as cv
from deepface import DeepFace
import pandas as pd
import asyncio
import random
# from google.colab.patches import cv2_imshow

face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap=cv.VideoCapture(0)
# cap.set(cv.CAP_PROP_FRAME_WIDTH, 160)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, 120)

async def click(count):
    if(count<600):
        cv.imwrite(r'E:\\Projects\\yolov5surveillance-20230808T135321Z-001\\backend\\Databases\\'+str(count)+'.jpg',frame[y:y+h, x:x+w])
        asyncio.sleep(2)
        print(count)
count=300
loop=asyncio.get_event_loop()
while True:
    (grabbed,frame)= cap.read()
    rgb=cv.cvtColor(frame,cv.COLOR_BGR2RGB)

    faces=face_cascade.detectMultiScale(rgb,scaleFactor=1.1, minNeighbors=5)
    for(x,y,w,h) in faces:
        loop.run_until_complete(click(count))
        count+=1
        color=(0,255,255)
        strokes=2

        cv.rectangle(frame,(x,y),(x+w,y+h),color,strokes)
    frame=cv.flip(frame,1)
    # frame=cv.resize(frame,(600,400))
    cv.imshow('Frame',frame)
    key=cv.waitKey(1) & 0xFF
    if key==ord('q'):
        break
cap.release()
cv.waitKey(1)
cv.destroyAllWindows()