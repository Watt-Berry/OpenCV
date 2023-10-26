import cv2
import numpy as np

# Load an image
video = cv2.VideoCapture(0)  # Replace 'your_image.jpg' with your image file

while True:
    ret, image = video.read()

    if not ret:
        break

    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the HSV range for green color
    lower_green = np.array([35, 100, 100])  # Lower range for green in HSV
    upper_green = np.array([85, 255, 255])  # Upper range for green in HSV

    # Create a mask to isolate green regions
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Define the HSV range for red color
    lower_red = np.array([0, 100, 100])  # Lower range for red in HSV
    upper_red = np.array([10, 255, 255])  # Upper range for red in HSV

    # Create a mask to isolate red regions
    red_mask = cv2.inRange(hsv_image, lower_red, upper_red)

    # Find contours in the green mask
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (0,255,255)) #draw contours on image

    # Filter contours based on shape (assumes a cube)
    detected_cubes=[]
    min_cube_area = 500
    for contour in contours:
        area = cv2.contourArea(contour)

        if area >= min_cube_area:
            # Approximate the contour to reduce points
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Check if the shape is approximately a cube
            if len(approx) == 4:
                detected_cubes.append(approx)

    # Draw rectangles around detected cubes
    for cube in detected_cubes:
        x, y, w, h = cv2.boundingRect(cube)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        #Coordinate of the center
        x_center = int(x + w/2)
        y_center = int(y + h/2)
        cv2.circle(image, (x_center, y_center), 3, (255,0,0), 3)

    # Show the image with rectangles around detected cubes
    cv2.imshow('Green Cube Detection', image)
    cv2.imshow('Green mask', green_mask)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Release the VideoCapture and close all OpenCV windows
video.release()
cv2.destroyAllWindows()