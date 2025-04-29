# Function definitions for Team 56 Project 3
from Imports56 import *
import math as m

# A class which contains three fields: an x coordinate, a y coordinate, and (optionally) an angle
class coordinates():
    def __init__(self, x, y, angle = 0): # call class like this: myCoord = coordinates(). 
        self.x = x
        self.y = y
        self.angle = angle
        self.fixAngle()
    
    def resetDisplacement(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        
    def copyCoordinate(self, coordinate):
        self.x = coordinate.x
        self.y = coordinate.y
        self.angle = coordinate.angle
    
    def updateCoords(self, delta):
    
        self.angle += delta.angle
        self.fixAngle()
        
        # Delta y stores the amount the robot
        # went forward. The angle of the robot
        # is used to update the angle
        if self.angle == 0:    
            self.y += delta.y
        elif self.angle == 90:
            self.x += delta.y
        elif self.angle == 180:
            self.y -= delta.y
        elif self.angle == 270:
            self.x -= delta.y
        else:
            print("oops!")
    
    def fixAngle(self):
        # This makes the angle always between 0 and 360
        while(self.angle >= 360):
            self.angle -= 360
        while(self.angle < 0):
            self.angle += 360
        
class Wheel:
    def __init__(self, left, right):
        """
        :param left - instance of motor class, the left motor
        :param right - instance of motor class, the right motor
        """
        self.left = left
        self.right = right
        
    def forward(self, degree):
        """
        :param degree - how much you want the robot to move forward
        """
        self.left.run_for_degrees(-degree, blocking=False)
        self.right.run_for_degrees(degree,blocking=True)
        
    def forwardForSpeed(self, speed):
        """
        :param speed - how fast you want the motors to go
        """
        self.left.start(-speed)
        self.right.start(speed)
    
    def turn(self, angle):
        """
        :param angle - how much you want the robot to turn
        """
        self.left.run_for_degrees(angle * 2.58, blocking=False)
        self.right.run_for_degrees(angle * 2.58, blocking=True)
        # 2.58 is based on the size of the wehels
        
    def turnRight(self, speed):
        """
        :param speed - how fast you want the motors to go
        """
        self.right.start(speed)
        
    def turnLeft(self, speed):
         """
        :param speed - how fast you want the motors to go
        """
        self.left.start(-speed)
        
def pushNpopAvg(sensorVal, sensorList, sensorSum):
    """
    :param sensorVal - the new sensor value
    :param sensorList - the list of sensor values
    :param sensorSum - the average of the new sensor list
    """
    # This removes the oldest sensor value from
    # the list, adds the new value to the list,
    # and finds the average of the list
    
    sensorList.pop()
    sensorList.insert(0, sensorVal)
    summation = 0
    for value in sensorList:
        summation += value
    summation /= sensorSum
    return summation, sensorList

def nullDefault(sensorVal, default = 0):
    """
    :param sensorVal - the new sensor value
    :param default - if there is a null, what should it be set to?
    """
    if (sensorVal == None):
        sensorVal = default
    return sensorVal

def nullDefaultList(sensorList, default = 0):
    """
    :param sensorVal - the new sensor value
    :param default - if there is a null, what should it be set to?
    """
    ret = []
    for sensorVal in sensorList:
        ret.append(nullDefault(sensorVal, default))
    return ret

def magnitude(somelist):
    """
    :param somelist - any list of numbers
    """
    summation = 0.00
    for i in somelist:
        summation = summation + pow(i,2)
    return m.sqrt(summation)

def forwardCommand(wheels, dCoords, increment):
    """
    :param wheels - a class of motors
    :param dCoords - the displacement coordinates
    :param increment - how much the robot moves at once
    """
    wheels.forward(increment) # go forward
    dCoords.y += (increment / 360) * m.pi * 21.99
    
def turnCommand(wheels, dCoords, angle):
    """
    :param wheels - a class of motors
    :param dCoords - the displacement coordinates
    :param increment - how much the robot moves at once
    """
    wheels.turn(angle) 
    dCoords.angle += 90

def chooseCommand(wheels, dCoords, increment, listvals, directionList):
    """
    :param wheels - a class of motors
    :param dCoords - the displacement coordinates
    :param increment - how much the robot moves at once
    :param listvals - the list of nulls or valids
    :param directionList - the list of directions showing whether we have gone there
    """
    choices = []    
        
    # First check if one is valid
    if (listvals[0] == True and listvals[1] == False):
        choices.append("Forward")
    elif (listvals[0] == False and listvals[1] == True):
        choices.append("Right")
    # If both is valid, check whether we have gone in a directoin
    elif (listvals[0] == True and listvals[1] == True): 
        if (directionList[0] == 0 and directionList[1] != 0):
            choices.append("Forward")
        elif (directionList[0] != 0 and directionList[1] == 0):
            choices.append("Right")
        else:
            # If all options are equally valid, make it random
            choices.append("Forward")
            choices.append("Right")
                
    choice = random.choice(choices)
    
    if (choice == "Forward"):
        forwardCommand(wheels, dCoords, increment)
        print("Forward")
    elif (choice == "Right"):
        print("Right")
        turnCommand(wheels, dCoords, -90)
    else: print("Error in chooseCommand")

    