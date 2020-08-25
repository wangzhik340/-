import os
import pygame
import sys
import time
import cv2

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN, 32)
screen.fill((255, 255, 255))
font = pygame.font.Font('D:\WORK\Python\OpenCV\想和你撞个满怀(非商用)_©字体视界.ttf', 50)
img = pygame.image.load('D:\WORK\Python\OpenCV\按钮.jpg')
pygame.display.set_caption('人脸验证')
color = (47, 79, 79)

text = font.render('人脸验证准备开始,请点击下方按钮', True, color)
text_1 = font.render('验证', True, color)
text_2 = font.render('正在初始化摄像头,请直面摄像头', True, color)
text_3 = font.render('初始化过程较慢,请耐心等待', True, color)
text_4 = font.render('验证失败,3S后自动退出', True, color)
text_5 = font.render('验证成功,3s后自动退出', True, color)
screen.blit(text, (550, 400))
screen.blit(img, (800, 500))
screen.blit(text_1, (874, 506))


def get_face():
    cap = cv2.VideoCapture(0)
    pygame.display.update()
    face_detect = cv2.CascadeClassifier(
        'D:\MAJOR\Python\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    pygame.display.update()
    recognizer.read('D:\WORK\Python\OpenCV\wzk.yml')
    font_text = cv2.FONT_HERSHEY_SIMPLEX
    time_first = time.time()
    xy = 0

    while True:
        pygame.display.update()
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
                    xy = xy + 1
                    print('相似度:{:.2f}%'.format(100 - abs(confidence - 50) * 2))
        time_second = time.time()
        print(xy)
        if xy >= 5:
            return True
        if time_second - time_first >= 3:
            return False


while True:
    for event in pygame.event.get():
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN and 800 <= event.pos[0] <= 1021 and 500 <= event.pos[1] <= 571:
            pygame.mouse.set_visible(False)
            screen.fill((255, 255, 255))
            screen.blit(text_2, (600, 450))
            screen.blit(text_3, (650, 500))
            pygame.display.flip()
            true_or_false = get_face()
            if true_or_false == int(True):
                screen.fill((255, 255, 255))
                screen.blit(text_5, (700, 500))
                pygame.display.flip()
                time.sleep(3)
                pygame.quit()
                sys.exit()
            elif true_or_false == int(False):
                screen.fill((255, 255, 255))
                screen.blit(text_4, (700, 500))
                pygame.display.flip()
                time.sleep(3)
                pygame.quit()
                sys.exit()
