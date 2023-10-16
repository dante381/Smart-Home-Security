import time
import numpy as np
import cv2
import torch
import torch.backends.cudnn as cudnn
from models.experimental import attempt_load
from utils.general import non_max_suppression
import telepot
import os

from deepface import DeepFace
import pandas as pd

import requests



token = '6316374614:AAECL4R-v29roy30tvFUlJ1dhwS15A5Ku0I' # telegram token
receiver_id = 1741911777 # https://api.telegram.org/bot<TOKEN>/getUpdates
weights = 'yolov5surveillance/best_face.pt'
camera = 0 # webcam
width, height = (352, 288) # quality 
display = True

# bot = telepot.Bot(token)
# bot.sendMessage(receiver_id, 'Your camera is active now.') # send a activation message to telegram receiver id

device = torch.device('cpu')

model = attempt_load(weights, map_location=device)  
stride = int(model.stride.max())  
cudnn.benchmark = True


cap = cv2.VideoCapture(camera) 
while(cap.isOpened()):
    time.sleep(0.2) # wait for 0.2 second 
    ret, frame_ = cap.read()
    frame = cv2.resize(frame_, (width, height), interpolation = cv2.INTER_AREA)
    
    if display:
        cv2.imshow("frame", frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    if ret ==True:
        img = torch.from_numpy(frame).float().to(device).permute(2, 0, 1)
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        pred = model(img, augment=False)[0]
        pred = non_max_suppression(pred, 0.39, 0.45, agnostic=True) # img, conf, iou, ...

        for det in pred:
            if len(det):
                conf_, class_ = det[0][4], int(det[0][5])
                print(conf_)
                if class_ == 0  and conf_ > 0.8 :

                    df=DeepFace.find(img_path=frame,db_path='.\\yolov5surveillance\\detected',enforce_detection=False, distance_metric="euclidean_l2",detector_backend = "mtcnn")
                    print(df[0].head())
                    # if df[0].loc[0]["VGG-Face_cosine"]>=0.03:
                    #     time_stamp = int(time.time())
                    #     fcm_photo = f'yolov5surveillance/detected/{time_stamp}.png'
                    #     cv2.imwrite(fcm_photo, frame_) # notification photo
                    #     # bot.sendPhoto(receiver_id, photo=open(fcm_photo, 'rb')) # send message to telegram
                    #     # print(f'{time_stamp}.png has sent.')
                    #     if(os.path.exists('./yolov5surveillance/detected/representations_vgg_face.pkl')):
                    #         os.remove('./yolov5surveillance/detected/representations_vgg_face.pkl')
                    # else:
                    #     print(df[0].loc[0].identity)

                else:
                    break
    
cap.release()
cv2.destroyAllWindows()


