import cv2
import numpy as np

class BarrelDetection:
    def __init__(self):
        self.flag = 1
        self.center_coordinates = [480/2,640/2]
        # Load an image
        self.video = cv2.VideoCapture(0)

        # Define the HSV range for red color
        self.lower_red = np.array([0, 100, 100])  # Lower range for red in HSV
        self.upper_red = np.array([10, 255, 255])  # Upper range for red in HSV

        # Define the HSV range for green color
        self.lower_green = np.array([35, 100, 100])  # Lower range for green in HSV
        self.upper_green = np.array([85, 255, 255])  # Upper range for green in HSV

        print("Barrel detection class initialised")

    def calibration(self, hsv_image, hue_range):
        h, w, c = hsv_image.shape
        x = int(w/2)
        y = int(h/2)
        hue, saturation, value = hsv_image[y][x]

        hue_lower = hue-hue_range
        if hue_lower < 0:
            hue_lower = 0
        saturation_lower = saturation-50
        if saturation_lower < 0:
            saturation_lower = 0
        value_lower = value-50
        if value_lower < 0:
            value_lower = 0

        lower = np.array([hue_lower, saturation_lower, value_lower])

        hue_upper = hue+hue_range
        if hue_upper > 360:
            hue_upper = 360
        saturation_upper = saturation+50
        if saturation_upper>255:
            saturation_upper = 255
        value_upper = value+50
        if value_upper > 255:
            value_upper = 255

        upper = np.array([hue_upper, saturation_upper, value_upper])

        return lower, upper

    def get_center_coordinates(self):
        ret, image = self.video.read()

        if not ret:
            self.flag = 0

        # Convert the image to the HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Create a mask to isolate green regions
        green_mask = cv2.inRange(hsv_image, self.lower_green, self.upper_green)

        # Create a mask to isolate red regions
        red_mask = cv2.inRange(hsv_image, self.lower_red, self.upper_red)

        mask = red_mask + green_mask

        # Find contours in the green mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image, contours, -1, (0, 255, 255))  # draw contours on image

        # Filter contours based on shape (assumes a cube)
        detected_cubes = []
        min_cube_area = areaTmp = 500
        largest_contour = []
        center_coordinates = []

        # Calculate and store the areas of each contour in the dictionary
        for idx, contour in enumerate(contours):
            area = cv2.contourArea(contour)

            if area >= min_cube_area:
                # Approximate the contour to reduce points
                epsilon = 0.04 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                # Check if the shape is approximately a cube
                if len(approx) == 4:
                    detected_cubes.append(approx)
                    if area > areaTmp:
                        areaTmp = area
                        largest_contour = contour

        # Draw coordinates of the center of the biggest object
        if len(largest_contour) > 0:
            x, y, w, h = cv2.boundingRect(largest_contour)
            x_center = int(x + w / 2)
            y_center = int(y + h / 2)
            self.center_coordinates = [x_center, y_center]
            cv2.circle(image, (x_center, y_center), 3, (255, 0, 0), 3)

        # Draw rectangles around detected cubes
        for cube in detected_cubes:
            x, y, w, h = cv2.boundingRect(cube)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Show the image with rectangles around detected cubes
        cv2.imshow('Object Cube Detection', image)
        cv2.imshow('Green+Red mask', mask)

        if cv2.waitKey(1) & 0xFF == ord('r'):
            self.lower_red, self.upper_red = self.calibration(hsv_image, 10)

        if cv2.waitKey(1) & 0xFF == ord('g'):
            self.lower_green, self.upper_green = self.calibration(hsv_image, 5)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            self.flag=0

        print(self.center_coordinates)

if __name__ == '__main__':
    myBarrelDetection = BarrelDetection()
while myBarrelDetection.flag == 1:
    myBarrelDetection.get_center_coordinates()

# Release the VideoCapture and close all OpenCV windows
myBarrelDetection.video.release()
cv2.destroyAllWindows()



