from djitellopy import Tello
import cv2
import numpy as np

def main():
    drone = Tello()
    drone.connect()
    print(f"Battery: {drone.get_battery()}%")

    drone.streamon()
    print("Camera stream started. Press 'q' to quit.")

    try:
        while True:
            frame_read = drone.get_frame_read()
            frame = frame_read.frame

            frame = cv2.resize(frame, (640, 480))

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lower_red = np.array([0, 120, 70])
            upper_red = np.array([10, 255, 255])
            mask1 = cv2.inRange(hsv, lower_red, upper_red)

            lower_red2 = np.array([170, 120, 70])
            upper_red2 = np.array([180, 255, 255])
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

            mask = mask1 + mask2

            result = cv2.bitwise_and(frame, frame, mask=mask)

            cv2.imshow("Tello Camera", frame)
            cv2.imshow("Detected Color", result)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        drone.streamoff()
        drone.end()
        cv2.destroyAllWindows()
        print("Disconnected from drone and closed camera stream.")

if __name__ == "__main__":
    main()
