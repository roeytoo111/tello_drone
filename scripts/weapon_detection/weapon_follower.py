import cv2
import numpy as np
from djitellopy import Tello
import time
from pathlib import Path

# Initialize Tello drone
me = Tello()
me.connect()
print(f"Battery: {me.get_battery()}%")

# Start video stream
me.streamon()
me.takeoff()

# Drone controls initialization
me.send_rc_control(0, 0, 25, 0)  # Initial movement to ensure drone starts flying
time.sleep(2.2)

# Define frame width, height, and PID control
w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0

# Load the Haar cascade for weapon detection
cascade_path = (
    Path(__file__).resolve().parents[2] / "assets" / "cascades" / "weapon_cascade.xml"
)
gun_cascade = cv2.CascadeClassifier(str(cascade_path))
if gun_cascade.empty():
    print(f"Error: weapon cascade not found/invalid at {cascade_path}")
    exit()

# Function to find weapon in the image
def findWeapon(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    guns = gun_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(100, 100))

    myWeaponListC = []
    myWeaponListArea = []

    for (x, y, w, h) in guns:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Draw bounding box
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)  # Draw center of the weapon
        myWeaponListC.append([cx, cy])
        myWeaponListArea.append(area)

    if len(myWeaponListArea) != 0:
        i = myWeaponListArea.index(max(myWeaponListArea))
        return img, [myWeaponListC[i], myWeaponListArea[i]]  # Return image and weapon position
    else:
        return img, [[0, 0], 0]  # No weapon detected

# Function to control drone based on weapon position
def trackWeapon(info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0

    # Calculate error in x direction (left/right)
    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    # Control forward/backward speed based on weapon area
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20  # Move backward if the weapon is too close
    elif area < fbRange[0] and area != 0:
        fb = 20  # Move forward if the weapon is too far away

    if x == 0:  # No weapon detected
        speed = 0
        error = 0

    # Send control commands to drone
    print(f"Speed: {speed}, Forward/Backward: {fb}")
    me.send_rc_control(0, fb, 0, speed)

    return error

# Main loop
while True:
    # Get video frame from the Tello drone
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w, h))

    # Detect weapon in the frame
    img, info = findWeapon(img)

    # Track the weapon's position and control the drone
    pError = trackWeapon(info, w, pid, pError)

    # Display the video feed
    cv2.imshow("Weapon Detection & Tracking", img)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        print(f"Battery: {me.get_battery()}%")
        break
