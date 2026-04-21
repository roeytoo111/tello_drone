import numpy as np
import cv2
from djitellopy import Tello
import imutils
import time
from pathlib import Path

# Load the Haar cascade for weapon detection
cascade_path = (
    Path(__file__).resolve().parents[2] / "assets" / "cascades" / "weapon_cascade.xml"
)
gun_cascade = cv2.CascadeClassifier(str(cascade_path))
if gun_cascade.empty():
    print(f"Error: weapon cascade not found/invalid at {cascade_path}")
    exit()

# Initialize the Tello drone
drone = Tello()
drone.connect()

# Print battery level
print(f"Battery: {drone.get_battery()}%")

# Start the drone and video stream
drone.takeoff()
drone.streamon()

# Fly to a height of 50 cm (half a meter)
drone.move_up(50)

FRAME_CENTER_TOLERANCE = 50  # Tolerance in pixels for centering the weapon
MOVE_STEP = 20  # Distance to move in cm for each adjustment

try:
    while True:
        # Get the video frame from the Tello drone
        frame = drone.get_frame_read().frame
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect guns in the frame
        guns = gun_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1,  # Increased precision
            minNeighbors=8,   # Require stronger evidence
            minSize=(100, 100)
        )

        if len(guns) > 0:
            # Assume the first detected gun is the target
            x, y, w, h = guns[0]
            gun_center_x = x + w // 2
            gun_center_y = y + h // 2

            # Draw a rectangle around the detected weapon
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Calculate the frame's center
            frame_center_x = frame.shape[1] // 2
            frame_center_y = frame.shape[0] // 2

            # Determine horizontal and vertical adjustments
            if gun_center_x < frame_center_x - FRAME_CENTER_TOLERANCE:
                print("Moving left")
                drone.move_left(MOVE_STEP)
            elif gun_center_x > frame_center_x + FRAME_CENTER_TOLERANCE:
                print("Moving right")
                drone.move_right(MOVE_STEP)

            if gun_center_y < frame_center_y - FRAME_CENTER_TOLERANCE:
                print("Moving forward")
                drone.move_forward(MOVE_STEP)
            elif gun_center_y > frame_center_y + FRAME_CENTER_TOLERANCE:
                print("Moving backward")
                drone.move_back(MOVE_STEP)

        # Display the video feed
        cv2.imshow("Tello Camera Feed", frame)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program interrupted.")

finally:
    # Land the drone and release resources
    drone.streamoff()
    drone.land()
    cv2.destroyAllWindows()













# import numpy as np
# import cv2
# from djitellopy import Tello
# import imutils
# import time

# gun_cascade = cv2.CascadeClassifier('cascade.xml')
# if gun_cascade.empty():
#     print("Error: cascade.xml not found or invalid.")
#     exit()

# drone = Tello()
# drone.connect()

# print(f"Battery: {drone.get_battery()}%")

# drone.takeoff()
# drone.streamon()

# drone.move_up(50)

# gun_exist = False
# detection_start_time = None  

# try:
#     while True:
#         frame = drone.get_frame_read().frame
#         frame = imutils.resize(frame, width=500)
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         guns = gun_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))
#         if len(guns) > 0:
#             if detection_start_time is None:
#                 detection_start_time = time.time()  

            
#             elapsed_time = time.time() - detection_start_time
#             if elapsed_time >= 5:  
#                 gun_exist = True
#                 print("ALERT: Gun detected for 4 seconds! Performing a flip.")
#                 drone.flip_back()
#                 detection_start_time = None  
#         else:
#             detection_start_time = None  

      
#         for (x, y, w, h) in guns:
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

  
#         cv2.imshow("Tello Camera Feed", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# except KeyboardInterrupt:
#     print("Program interrupted.")

# finally:
#     drone.streamoff()
#     drone.land()
#     cv2.destroyAllWindows()
#     if gun_exist:
#         print("Gun was detected during the session.")
#     else:
#         print("No guns were detected during the session.")
