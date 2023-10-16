import cv2 as cv
from deepface import DeepFace

import firebase_admin
from firebase_admin import credentials, messaging

face_cascade= cv.CascadeClassifier('haar')