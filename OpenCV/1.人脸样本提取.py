import cv2

cap = cv2.VideoCapture(0)
face_detect = cv2.CascadeClassifier(
    'D:\MAJOR\Python\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
i = 0

while True:
    x, img = cap.read()
    if x == False:
        break
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_zone = face_detect.detectMultiScale(gray, 1.1, 5)
    for x, y, w, h in face_zone:
        cv2.rectangle(img, (x, y), (x + w, y + h), [127, 255, 170], 2)
        cv2.imwrite('D:\PICTURE\\faces\\' + str(i) + '.jpg', gray[y:y + h, x:x + w])
        i = i + 1
    print(i)
    cv2.imshow('face', img)
    if cv2.waitKey(1) == 27:
        break
    if i >= 800:
        break

cap.release()
cv2.destroyAllWindows()
