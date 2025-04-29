# -*- coding: utf-8 -*-\
import math as m
from Imports56 import *
import MazeRobotFunctions as F
"""
Created on Fri Apr 11 16:41:01 2025

@author: norwo
"""

def createMapBlank(numSpaces):
    """
    :param numSpaces - a coordinate that shows the size of the map
    """
    #creates a blank map
    totalMapList = []
    for i in range (numSpaces.y):
        totalMapList.append([0]*numSpaces.x)
    return totalMapList
        
def exportMap (totalMapList, mapNum, origin):
    """
    :param totalMapList - a 2D array of the map
    :mapNum mapNum - the map number for documentation
    :origin - a coordinate of the position that we started
    """
    mapFile = open("theMap",'w') # Open the map file to write
    mapFile.write("Team: 56\n")
    mapFile.write("Map: ")
    mapFile.write(str(mapNum))
    mapFile.write("\n")
    mapFile.write("Unit Length: 40\n")
    mapFile.write("Unit: cm\n")
    mapFile.write("Origin: (")
    mapFile.write(str(origin.x))
    mapFile.write(",")
    mapFile.write(str(origin.y))
    mapFile.write(")\n")
    mapFile.write("Notes: \n")
    for i in reversed(totalMapList):
        smallList = i
        for n in smallList:
            cord = str(n)
            mapFile.write(cord)
            mapFile.write(", ")
        mapFile.write("\n")
    mapFile.flush()
    mapFile.close
    
def mapCreation(currentSpot, totalMapList, numSpaces, squareSize):
    """
    :param currentSpot - a coordinate of the position of the robot on the map
    :param totalMapList - a 2D array of the map
    :param numSpaces - a coordinate that shows the size of the map
    :param squareSize - the size of a square on the map
    """
    
    # Converts the actual coordinates to the map square system
    coords = F.coordinates(0, 0)
    coords.y = m.floor(currentSpot.y/squareSize)
    coords.x = m.floor(currentSpot.x/squareSize)
    
    if (numSpaces.y > coords.y and numSpaces.x > coords.x and coords.y >= 0 and coords.x >= 0):
        # If we went on an unexplored space, we explored it
        if (totalMapList[coords.y][coords.x] == 0):
            totalMapList[coords.y][coords.x] = 1

    return totalMapList

def printHazards(IRthreshold, IRCoords, magthreshold, magCoords, mapNum):
    """
    :param IRthreshold - the IR value
    :param IRCoords - the coordinates of the IR beacon
    :param magthreshold - the magnet value
    :param magCoords - the coordinates of the magnet
    """
                
    mapFile = open("theHazards",'w') # Open the map file to write
    mapFile.write("Team: 56\n")
    mapFile.write("Map: ")
    mapFile.write(str(mapNum))
    mapFile.write("\n")
    mapFile.write("Notes:\n\n")
    mapFile.write("Hazard Type, Parameter of Interest, Parameter Value, ")
    mapFile.write("Hazard X Coordinate (cm), Hazard Y Coordinate (cm)\n")
    mapFile.write("Electrical/Magnetic Activity Source, Field Strength (uT), ")
    if (magCoords.x == -1):
        mapFile.write("None Found \n")
    else:
        mapFile.write(str(magthreshold))
        mapFile.write(", ")
        mapFile.write(str(magCoords.x))
        mapFile.write(", ")
        mapFile.write(str(magCoords.y))
        mapFile.write("\n")
    mapFile.write("High Temperature Heat Source, Radiated Power (W), ")
    if (IRCoords.y == -1):
        mapFile.write("None Found \n")
    else:
        mapFile.write(str(24))
        mapFile.write(", ")
        mapFile.write(str(IRCoords.x))
        mapFile.write(", ")
        mapFile.write(str(IRCoords.y))
        mapFile.write("\n")
        
def findPath(totalMapList, currentSpot, squareSize, numSpaces):
    """
    :param totalMapList - a 2D array of the map
    :param currentSpot - a coordinate of the position of the robot on the map
    :param squareSize - the size of a square on the map
    :param numSpaces - a coordinate that shows the size of the map
    """
    delta = F.coordinates(0, 1)
    newDirection = F.coordinates(m.floor(currentSpot.x/squareSize), m.floor(currentSpot.y/squareSize))
    direction = F.coordinates(0, 0)
    retList = []
    
    # This looks at each direction that is adjacent to the current square
    # and inserts the value into retList
    # It is front, right, back, left
    for i in range(4):
        direction.copyCoordinate(newDirection)
        turn = i * -90
        delta.angle = currentSpot.angle - turn
        direction.updateCoords(delta)
        if (numSpaces.y >= direction.y and numSpaces.x >= direction.x):
            retList.append(totalMapList[direction.y][direction.x])
        else:
            retList.append(-1)

    return retList
    
    
    
    
    
    
    
    