# Function definitions for Team 56 Project 3
from Imports56 import *
import math as m

# A class which contains two fields: an x coordinate and a y coordinate 
class coordinates():
    def __init__(self, x, y): # call class like this: myCoord = coordinates()
        self.x = x
        self.y = y

# A class which contains two fields: a direction to turn and the distance to turn
class TurnObj:
    def __init__(self, direction, distance):
        self.direction = direction
        self.distance = distance
        
# A class which contains two fields: a left wheel class and a right wheel class
# The class has functions for starting, turning, and stopping using the motor class functions
class Wheel:
    def __init__(self, left, right):
        """
        :param left - instance of motor class, the left motor
        :param right - instance of motor class, the right motor
        """
        self.left = left
        self.right = right
        
    def startWheels(self, speed):
        """
        :param speed - the speed you want to go at
        """
        self.left.start(speed)
        self.right.start(speed)
    
    def turnWheels(self, speed):
        """
        :param speed - the speed you want to go at
        """
        self.left.start(speed)
        self.right.start(speed)
        
    def turnWheelsDeg(self, degree):
        self.left.run_for_degrees(-degree, blocking=False)
        self.right.run_for_degrees(degree,blocking=False)
        time.sleep(0.3)

    # This is a problem
    def stopWheels(self):
        self.left.stop()
        self.right.stop()
    
# A function which sets all of the motors in motorList to the default desired
def motorSetup(motorList, default):

    for motor in motorList:
        motor.set_default_speed(default)

# Returns the two IR values (it is like this due to the the trying function)_
def IRInfo(IR):
    """
    :param IR - an instance of IRSensor
    """
    return [IR.value1, IR.value2]

# Meant to make the wheels of the robot start rotating depending on the direction
def rotate(wheels, direction, speed):
    """
    :param wheels - a class of two motor classes 
    :param direction - the direction you are going. Left, right, or stop
    :param speed - the desired speed of the wheel motors
    """
    if (direction == 'left'):
        wheels.turnWheels(speed)
    elif (direction == 'right'):
        wheels.turnWheels(-speed)
    elif (direction == 'stop'):
        return 0
    else:
        return IOError

# Stops, rotates wheels the desired degrees, then stops
# It should be noted that there may be some lag with this setup (going over)
def gyroRotate(IMU, wheels, direction, degrees, updateSpeed, speed, robotAngle):
    """
    :param IMU - a class that represents the IMU sensor
    :param wheels - a class that consists of the two wheel motors
    :param direction - the desired direction to turn the motors
    :param degrees - how much you want to turn the robot
    :param updateSpeed - how often you want to update the data (go through loop)
    :param speed - the desired speed of the motors
    :param robotAngle - the current angle of the robot
    """
    '''Werid degree corrections'''
    if abs(degrees) >= 180:
        degrees = degrees + 15
    if abs(degrees) >= 200:
        degrees = degrees + 18
    if abs(degrees) > 270:
        degrees = degrees + 18
        
    ''' This try loop has to stay here for the feedback loop to work'''
    try:

        gain = 0.1 # User can change this value to see how the behavior of the controller changes
        angle_delta = degrees # User can change this value to see how the behavior of the controller changes
        gyroVals = ['N/A', 'N/A'] # We start with no gyro values
        tempAngle = 0

        while abs(tempAngle) <= abs(degrees):
            
            print(tempAngle)
            current_offset = angle_delta - tempAngle
        
            if current_offset * gain > 100:
                speed = 100
            elif current_offset * gain < -100:
                speed = -100
            else:
                speed = current_offset * gain

            rotate(wheels, direction, speed)
            gyroVals[0] = gyroVals[1] # The new gyro value is now old
            gyroVals[1] = (IMU.getGyro())[2] # The new gyro value is created
            if ( (gyroVals[0] != 'N/A') and (gyroVals[1] != 'N/A') ): # If we have enough data
                # add to the angle we turned using trapeziodal sums  
                tempAngle = tempAngle + (trapSum(updateSpeed, gyroVals)*1.2)
            time.sleep(0.1)
    except TypeError:
        print("this is broken")
    robotAngle = robotAngle + tempAngle # update the robot angle
            
    '''
    tempAngle = 0 # Angle is relative to robotAngle, which it should be the same at the start
    gyroVals = ['N/A', 'N/A'] # We start with no gyro values
    print("goodbye!")
    gain = 0.2 # User can change this value to see how the behavior of the controller changes
    angle_delta = degrees
    #wheels.stopWheels() # Stop whatever the wheels are doing
    print("goodbye Sam!")
    # begin rotating
    while(abs(tempAngle) < abs(degrees)):
        time.sleep(updateSpeed) # rotate for updateSpeed before doing everything
        print("Angle:", tempAngle) 
        gyroVals[0] = gyroVals[1] # The new gyro value is now old
        gyroVals[1] = (IMU.getGyro())[2] # The new gyro value is created
        if ( (gyroVals[0] != 'N/A') and (gyroVals[1] != 'N/A') ): # If we have enough data
            # add to the angle we turned using trapeziodal sums  
            tempAngle = tempAngle + (trapSum(updateSpeed, gyroVals))
    wheels.stopWheels() # Stop any rotation of the wheels
    robotAngle = robotAngle + tempAngle # update the robot angle
    '''
    return robotAngle
    
# Stops, moves wheels the desired degrees, then stops
# It should be noted that there may be some lag with this setup (going over)
def moveForward(IMU, wheels, distance, updateSpeed, speed, coords, robotAngle, degree):
    """
    :param IMU - a class that represents the IMU sensor
    :param wheels - a class that consists of the two wheel motors
    :param distance - how much the robot should move forward
    :param updateSpeed - how often you want to update the data (go through loop)
    :param speed - the expected speed of the motors
    :param coords - the old coordinates before moving forward
    """
    currentDistance = 0 # We should not have moved yet
    speedVals = ['N/A', 'N/A'] # We start with no speed values
    # Start the wheels
    while(currentDistance < distance): # While we have not gone the required distance
        #Wait before doing anything
        #print("Current Distance", currentDistance)
         wheels.turnWheelsDeg(degree) # Turn the wheels for the amount of degrees and then stop
         
         currentDistance = currentDistance + degree / 360 * m.pi * 6.8 # Get the current distance in cm
    '''
        For when we used speed to get distance

        speedVals[0] = speedVals[1] # The new value is now old
        speedVals[1] = (wheels.left.get_speed() + wheels.right.get_speed()) * 2 # Multiplied by 4 due to wheel size, get new value
        if (speedVals[0] != 'N/A'): # If we have enough data 
            currentDistance = currentDistance + abs(trapSum(updateSpeed, speedVals)) #update the distance travelled
    '''
    coords = newCoords(coords, robotAngle, distance) # Get the new coordinates using trig
    return coords

# Need to work on this, maybe use the current angle to make an adjustment?
def findDirection(coords, objective, angle):
    """
    :param coords - A list of coordinates taken. The recent one is at the top of the list
    :param objective - the point that we want to go to
    :param angle - the angle of the robot at the moment (0 is +y, 90 is -x, ect)
    """
    # get the difference we have to go
    deltaX = objective.x - coords[-1].x
    deltaY = objective.y - coords[-1].y
    
    # Normalizes the angles. I use mod 315 so that the highest angles go back to being up
    while(angle < 0):
        angle = angle + 360
    angle = angle % 315
    
    # converts analog angles to digital direction
    if (angle <= 45):
        currentDirection = coordinates(0, 1) 
    elif (angle <= 135):
        currentDirection = coordinates(-1, 0)
    elif (angle <= 225):
        currentDirection = coordinates(0, -1)
    else:
        currentDirection = coordinates(1, 0)
        
    # converts digital direction to direction to turn
    # This means that if you were to turn, this would be the right direction
    yFactor = currentDirection.x * deltaY  
    xFactor = currentDirection.y * deltaX
    if (yFactor < 0 or xFactor > 0):
        direction = 'right'
    else:  # Is it even possible to get both factors to zero?
        direction = 'left'
    return direction

# takes a list of coords as input
def newCoords(coords, angle, distance):
    """
    :param coords - A list of coordinates taken. The recent one is at the top of the list
    :param angle - the angle of the robot at the moment (0 is +y, 90 is -x, ect)
    :param distance - the distance you have moved 
    """
    oldCoords = coords[-1] # Take the most recent coordinate
    # Use trig to find new coordinate
    newCoords = coordinates(oldCoords.x + distance * m.sin(angle), oldCoords.y + distance * m.cos(angle))
    coords.append(newCoords) # Add new coordinate to top of list
    return coords

# Returns the trapeziodal sum when given the width and two heights
def trapSum(updateSpeed, valList):
    """
    :param updateSpeed - The change in x
    :param valList - The two values you are interested in
    """
    sumZ = updateSpeed * (valList[0] + valList[1])/2 # perform a trap sum
    return sumZ -0.1 # Correction factor

#Takes a list and finds its magnitudes
def magnitude(list):
    """
    :param list - any list of numbers
    """
    summmation = 0
    for i in list:
        summation = summation + i^2
    return m.sqrt(summation)

# Try except stuff to make code cleaner
# Don't worry about it my dude
def trying(function):
    """
    :param function - Any function you want try except statements for
    """
    try: 
        while True: # Do I need this? eh?
            try:
                  a = function
                  return a
            except IOError:
                print ("\nError occurred")
                break

    except KeyboardInterrupt:
        print("\nCtrl+C detected. Exiting...")