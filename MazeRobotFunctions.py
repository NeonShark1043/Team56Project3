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
    
    def updateCoords(self, delta):
    
        self.angle += delta.angle
        self.fixAngle()
        
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
        self.left.run_for_degrees(-degree, blocking=False)
        self.right.run_for_degrees(degree,blocking=True)
        #time.sleep(0.3)
    
    def turn(self, angle):
        """
        :param speed - the speed you want to go at
        """
        self.left.run_for_degrees(angle * 233.5 / 90, blocking=False)
        self.right.run_for_degrees(angle * 233.5 / 90,blocking=True)
        time.sleep(0.3)
        
def pushNpopAvg(sensorVal, sensorList, sensorSum):
    sensorList.pop()
    sensorList.insert(0, sensorVal)
    summation = 0
    for value in sensorList:
        summation += value
    summation /= sensorSum
    return summation, sensorList

def nullDefault(sensorVal, default = 0):
    if (sensorVal == None):
        sensorVal = default
    return sensorVal

def nullDefaultList(sensorList, default = 0):
    ret = []
    for sensorVal in sensorList:
        ret.append(nullDefault(sensorVal, default))
    return ret

def magnitude(somelist):
    """
    :param list - any list of numbers
    """
    summation = 0.00
    for i in somelist:
        summation = summation + pow(i,2)
    return m.sqrt(summation)