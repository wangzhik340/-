import os
import cv2
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()
face_detect = cv2.CascadeClassifier(
    'D:\MAJOR\Python\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')

image_paths = [os.path.join('D:\PICTURE\\faces\\', f) for f in os.listdir('D:\PICTURE\\faces')]
faces = []
ids = []
for image_path in image_paths:
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_np = np.array(gray, 'uint8')
    faces.append(img_np)
    ids.append(int(image_path[17:-4]))
recognizer.train(faces, np.array(ids))
