# OpenCV
Repository for image detection with OpenCV library

Barrel detection python code:

Detects green and red objects by using color filter:
- Take either green or red channel and convert it into HSV to create a mask
- Contour fonction to detect the contours of the objects 
- Calculate the area of the contour - minimum area tolerance
- Get the x,y coordinates upper left corner + width and height
- Get the x,y coordinates of the center of the detected contour
- Draw a rectangle with the size of the contour (width, height)
- Display the result

  Results :

  - Green mask channel:
![image](https://github.com/Watt-Berry/OpenCV/assets/109072703/ca548e21-3c00-4dcf-87f1-22dfc8a6603b)


  - Object detection image result:
![image](https://github.com/Watt-Berry/OpenCV/assets/109072703/32d3e0bb-d66e-4182-b8b2-1f5367cded3e)
