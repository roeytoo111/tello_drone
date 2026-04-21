import cv2
import numpy as np

# Callback function for trackbars (used for adjusting HSV color range)
def nothing(x):
    pass

# Initialize the camera
cap = cv2.VideoCapture(0)

# Create a window for the trackbars to adjust color ranges
cv2.namedWindow("Trackbars")

# Create trackbars for Hue, Saturation, and Value ranges (lower and upper bounds)
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

while True:
    # Read frame from the camera
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame.")
        break

    # Convert the frame from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get the current positions of the trackbars (color bounds)
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    # Define the lower and upper bounds for the color
    lower_bound = np.array([l_h, l_s, l_v])
    upper_bound = np.array([u_h, u_s, u_v])

    # Create a mask using the color bounds
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Apply the mask to the original frame
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the original and masked frames
    cv2.imshow("Original Frame", frame)
    cv2.imshow("Masked Frame", result)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
