# -*- coding: utf-8 -*-\
import math as m
from Imports56 import *
import MazeRobotFunctions as F
"""
Created on Fri Apr 11 16:41:01 2025

@author: norwo
"""

def createMapBlank(numSpaces):
    #creates a blank map
    totalMapList = []
    for i in range (numSpaces.y):
        totalMapList.append([0]*numSpaces.x)
    return totalMapList
        
def exportMap (totalMapList, mapNum, origin):
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
    
def mapCreation(currentSpot, totalMapList, numSpaces, squareSize, end):
    
    # Converts the actual coordinates to the map square system
    coords = F.coordinates(0, 0)
    coords.y = m.floor(currentSpot.y/squareSize)
    coords.x = m.floor(currentSpot.x/squareSize)
    
    if (numSpaces.y > coords.y and numSpaces.x > coords.x and coords.y >= 0 and coords.x >= 0):
        if(end == 1):
            totalMapList[coords.y][coords.x] = 4
        elif (totalMapList[coords.y][coords.x] == 0):
            totalMapList[coords.y][coords.x] = 1

    return totalMapList

def printHazards(IRthreshold, IRCoords, magthreshold, magCoords,mapNum):
                
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
        mapFile.write(str(IRthreshold))
        mapFile.write(", ")
        mapFile.write(str(IRCoords.x))
        mapFile.write(", ")
        mapFile.write(str(IRCoords.y))
        mapFile.write("\n")