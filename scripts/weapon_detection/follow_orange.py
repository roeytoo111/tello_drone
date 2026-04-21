import cv2
import numpy as np
from djitellopy import Tello
import time

me = Tello()
me.connect()
print(f"Battery: {me.get_battery()}%")

me.streamon()
# me.takeoff()

# me.send_rc_control(0, 0, 25, 0)  
time.sleep(2.2)

w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0

# Create window for trackbars
cv2.namedWindow("Trackbars")

# Create trackbars for lower and upper HSV values for orange
cv2.createTrackbar("Lower H", "Trackbars", 8, 179, lambda x: None)
cv2.createTrackbar("Lower S", "Trackbars", 42, 255, lambda x: None)
cv2.createTrackbar("Lower V", "Trackbars", 125, 255, lambda x: None)
cv2.createTrackbar("Upper H", "Trackbars", 14, 179, lambda x: None)
cv2.createTrackbar("Upper S", "Trackbars", 142, 255, lambda x: None)
cv2.createTrackbar("Upper V", "Trackbars", 187, 255, lambda x: None)

def findOrangeObject(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Get the current values from the trackbars
    lower_h = cv2.getTrackbarPos("Lower H", "Trackbars")
    lower_s = cv2.getTrackbarPos("Lower S", "Trackbars")
    lower_v = cv2.getTrackbarPos("Lower V", "Trackbars")
    upper_h = cv2.getTrackbarPos("Upper H", "Trackbars")
    upper_s = cv2.getTrackbarPos("Upper S", "Trackbars")
    upper_v = cv2.getTrackbarPos("Upper V", "Trackbars")

    # Update the lower and upper bounds based on trackbar values
    lower_orange = np.array([lower_h, lower_s, lower_v])
    upper_orange = np.array([upper_h, upper_s, upper_v])

    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    myObjectListC = []
    myObjectListArea = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h

        if area > 500:  
            cx = x + w // 2
            cy = y + h // 2
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)  
            myObjectListC.append([cx, cy])
            myObjectListArea.append(area)

    if len(myObjectListArea) != 0:
        i = myObjectListArea.index(max(myObjectListArea))
        return img, [myObjectListC[i], myObjectListArea[i]]  
    else:
        return img, [[0, 0], 0]  

def trackObject(info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20  
    elif area < fbRange[0] and area != 0:
        fb = 20  

    if x == 0:  
        speed = 0
        error = 0

    print(f"Speed: {speed}, Forward/Backward: {fb}")
    me.send_rc_control(0, fb, 0, speed)

    return error

while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w, h))

    img, info = findOrangeObject(img)

    pError = trackObject(info, w, pid, pError)

    cv2.imshow("Orange Object Detection & Tracking", img)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        print(f"Battery: {me.get_battery()}%")
        break















# import cv2
# import numpy as np
# from djitellopy import Tello
# import time

# me = Tello()
# me.connect()
# print(f"Battery: {me.get_battery()}%")

# me.streamon()
# me.takeoff()

# me.send_rc_control(0, 0, 25, 0)  
# time.sleep(2.2)

# w, h = 360, 240
# fbRange = [6200, 6800]
# pid = [0.4, 0.4, 0]
# pError = 0

# def findOrangeObject(img):
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#     lower_orange = np.array([8, 42, 125])  # Lower bound for orange
#     upper_orange = np.array([14, 142, 187])  # Upper bound for orange

#     mask = cv2.inRange(hsv, lower_orange, upper_orange)

#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     myObjectListC = []
#     myObjectListArea = []

#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         area = w * h

#         if area > 500:  
#             cx = x + w // 2
#             cy = y + h // 2
#             cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  
#             cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)  
#             myObjectListC.append([cx, cy])
#             myObjectListArea.append(area)

#     if len(myObjectListArea) != 0:
#         i = myObjectListArea.index(max(myObjectListArea))
#         return img, [myObjectListC[i], myObjectListArea[i]]  
#     else:
#         return img, [[0, 0], 0]  

# def trackObject(info, w, pid, pError):
#     area = info[1]
#     x, y = info[0]
#     fb = 0

#     error = x - w // 2
#     speed = pid[0] * error + pid[1] * (error - pError)
#     speed = int(np.clip(speed, -100, 100))

#     if area > fbRange[0] and area < fbRange[1]:
#         fb = 0
#     elif area > fbRange[1]:
#         fb = -20  
#     elif area < fbRange[0] and area != 0:
#         fb = 20  

#     if x == 0:  
#         speed = 0
#         error = 0

#     print(f"Speed: {speed}, Forward/Backward: {fb}")
#     me.send_rc_control(0, fb, 0, speed)

#     return error

# while True:
#     img = me.get_frame_read().frame
#     img = cv2.resize(img, (w, h))

#     img, info = findOrangeObject(img)

#     pError = trackObject(info, w, pid, pError)

#     cv2.imshow("Orange Object Detection & Tracking", img)

#     # Exit loop if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         me.land()
#         print(f"Battery: {me.get_battery()}%")
#         break
