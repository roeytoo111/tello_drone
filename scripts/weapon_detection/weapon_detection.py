import numpy as np
import cv2
from djitellopy import Tello
import imutils
from pathlib import Path

cascade_path = (
    Path(__file__).resolve().parents[2] / "assets" / "cascades" / "weapon_cascade.xml"
)
gun_cascade = cv2.CascadeClassifier(str(cascade_path))
if gun_cascade.empty():
    print(f"Error: weapon cascade not found/invalid at {cascade_path}")
    exit()

drone = Tello()
drone.connect()

print(f"Battery: {drone.get_battery()}%")

drone.streamon()

gun_exist = False

try:
    while True:
        frame = drone.get_frame_read().frame
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        guns = gun_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))
        if len(guns) > 0:
            gun_exist = True
            for (x, y, w, h) in guns:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            print("ALERT: Gun detected!")

        cv2.imshow("Tello Camera Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program interrupted.")

finally:
    drone.streamoff()
    drone.end()
    cv2.destroyAllWindows()
    if gun_exist:
        print("Gun was detected during the session.")
    else:
        print("No guns were detected during the session.")





















# import numpy as np
# import cv2
# import imutils

# # Load the Haar cascade for gun detection
# gun_cascade = cv2.CascadeClassifier('cascade.xml')
# if gun_cascade.empty():
#     print("Error: cascade.xml not found or invalid.")
#     exit()

# # Initialize video capture
# camera = cv2.VideoCapture(0)
# if not camera.isOpened():
#     print("Error: Unable to access the camera.")
#     exit()

# firstFrame = None
# gun_exist = False

# try:
#     while True:
#         ret, frame = camera.read()
#         if not ret:
#             print("Error: Unable to read from the camera.")
#             break

#         frame = imutils.resize(frame, width=500)
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # Detect guns in the frame
#         guns = gun_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))
#         if len(guns) > 0:
#             gun_exist = True
#             for (x, y, w, h) in guns:
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
#             print("ALERT: Gun detected!")

#         # Display the video feed
#         cv2.imshow("Security Feed", frame)

#         # Exit loop if 'q' is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# except KeyboardInterrupt:
#     print("Program interrupted.")

# finally:
#     # Release resources and clean up
#     camera.release()
#     cv2.destroyAllWindows()
#     if gun_exist:
#         print("Gun was detected during the session.")
#     else:
#         print("No guns were detected during the session.")
