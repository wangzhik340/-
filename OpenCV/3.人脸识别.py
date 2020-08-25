import cv2
import time

cap = cv2.VideoCapture(0)
face_detect = cv2.CascadeClassifier(
    'D:\MAJOR\Python\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('D:\WORK\Python\OpenCV\wzk.yml')
font_text = cv2.FONT_HERSHEY_SIMPLEX


while True:
    x, imge = cap.read()
    if x == 0:
        break
    gray = cv2.cvtColor(imge, cv2.COLOR_BGR2GRAY)
    face_zone = face_detect.detectMultiScale(gray, 1.1, 5)
    for x, y, w, h in face_zone:
        if w >= 150:
            cv2.rectangle(imge, (x, y), (x + w, y + h), [127, 255, 170], 2)
            i, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if 40 <= int(confidence) <= 60:
                cv2.putText(imge, 'wzk', (x, y - 5), font_text, 1, [127, 255, 170], 2)
                print('相似度:{:.2f}%'.format(100 - abs(confidence - 50) * 2))
    cv2.imshow("人脸识别",imge)
    if cv2.waitKey(1)==27:
        break


cap.release()
cv2.destroyAllWindows()
