
import cv2
import numpy as np
from djitellopy import tello
from time import sleep
from handD import handDetector

# connecting tello drone
cap = cv2.VideoCapture(0)
me = tello.Tello()
me.connect()
print(me.get_battery())

# me.streamon()
# me.takeoff()
#me.send_rc_control(0, 0, 20, 0)


detector = handDetector(maxHands=1, detectionCon=0)

###########################
# w, h = 360, 240
fb =0
###########################


# def findFace(img):
#     faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#     imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)
#
#     myFaceListC = []
#     myFaceListArea = []
#
#     for (x, y, w, h) in faces:
#         cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
#         cx = x + w // 2
#         cy = y + h // 2
#         area = w * h
#         cv2.circle(img ,(cx, cy), 5, (0,255,0), cv2.FILLED)
#         myFaceListC.append([cx,cy])
#         myFaceListArea.append(area)
#
#     if len(myFaceListArea) != 0:
#         i = myFaceListArea.index(max(myFaceListArea))
#         return img, [myFaceListC[i], myFaceListArea[i]]
#     else:
#         return img, [[0,0], 0]



while True:

    img = me.get_frame_read().frame
    #success, img = cap.read()

    img = detector.findHands(img)
    bbox, lmList = detector.findPosition(img)



    if lmList:
        fingers = detector.fingersUp()
        print(fingers)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            me.land()
            print(me.get_battery())
        #     break
        if fingers == [0, 1, 0, 0, 0]:  # go up
            me.send_rc_control(0, 0, 25, 0)
            sleep(2)
        elif fingers == [0,1 , 1, 0, 0]:  # go foreward
            me.send_rc_control(0, 25, 0, 0)
            sleep(2)

        elif fingers == [1,1 , 0, 0, 0]:   # left
            me.send_rc_control(-15, 0, 0, 0)
            sleep(2)

        elif fingers == [1, 0, 0, 0, 1]:  # right
            me.send_rc_control(15, 0, 0, 0)
            sleep(2)
        # elif fingers == [1, 1, 1, 1, 1]:   # land
        #     me.land()
        # elif fingers == [1, 1, 0 , 0, 1]: # scanninning the left
        #     me.send_rc_control(0, -35, 0, 0)
        #     sleep(2)
        #     me.send_rc_control(0, 0, 0, 25)
        #     sleep(2)
        #     me.send_rc_control(0, 20, 0, 0)
        #     sleep(2)
        elif fingers == [1, 1, 1, 1, 1]:  # back
            me.send_rc_control(0, -20, 0, 0)

        elif fingers == [0, 0, 0, 0, 1]:  # flip
            me.flip_left()
            sleep(2)

        elif fingers == [1, 1, 0, 0, 1]:  # flip
            me.flip_right()
            sleep(2)

        elif fingers == [1, 1, 0, 0, 1]:
            me.land()
        elif fingers == [0, 0, 0, 0, 0]:
            me.send_rc_control(0, 0, 0, 0)



    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        print(me.get_battery())
        break