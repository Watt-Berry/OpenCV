from Barrel_detection import BarrelDetection
import PiMotor
import time
import RPi.GPIO as GPIO

#Name of Individual MOTORS
m1 = PiMotor.Motor("MOTOR1",1)
m2 = PiMotor.Motor("MOTOR2",1)
m3 = PiMotor.Motor("MOTOR3",1)
m4 = PiMotor.Motor("MOTOR4",1)

#To drive all motors together
motorLeft = PiMotor.LinkedMotors(m1,m2)
motorRight = PiMotor.LinkedMotors(m3,m4)
motorAll = PiMotor.LinkedMotors(m1,m2,m3,m4)

def remap(value, min, max, mapMin, mapMax):
    if value > max:
        value = max
    if value < min:
        value = min

    remappedValue = (value-min)/(mapMax-mapMin)
    return remappedValue

def get_error(current_value, goal):
    error = goal-current_value
    return error


if __name__ == '__main__':
    myBarrelDetector = BarrelDetection()
    myBarrelDetector.get_center_coordinates()
    y = 480/2
    x = 640/2
    error_x = get_error(myBarrelDetector.center_coordinates[1], x)

    while(abs(error_x)>1):
        speed = remap(abs(error_x), 0, x/2, 0, 100)

        if error_x > 0: #turn right
            motorLeft.backward(speed)
            motorRight.forward(speed)
        else: #turn left
            motorRight.backward(speed)
            motorLeft.forward(speed)

        #time.sleep ?
        myBarrelDetector.get_center_coordinates()
        error_x = get_error(myBarrelDetector.center_coordinates[1], x)

    error_y = get_error(myBarrelDetector.center_coordinates[0], y)

    while(abs(error_y)>1):
        speed = remap(abs(error_y), 0, y/2, 0, 100)

        if error_y > 0: #move backward
            motorAll.backward(speed)
        else: #move forward
            motorAll.forward(speed)

        # time.sleep ?
        myBarrelDetector.get_center_coordinates()
        error_y = get_error(myBarrelDetector.center_coordinates[0], y)

    error_x = get_error(myBarrelDetector.center_coordinates[1], x)

    print("error in x : " + error_x)
    print("error in y : " + error_y)
    print("object centered")