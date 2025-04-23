# -*- coding: utf-8 -*-\
import math as m
from Imports56 import *
import Functions56 as F
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
        
def exportMap (totalMapList, mapFile, mapNum, origin):
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
    mapFile.write("Notes \n")
    for i in reversed(totalMapList):
        smallList = i
        for n in smallList:
            cord = str(n)
            mapFile.write(cord)
            mapFile.write(", ")
        mapFile.write("\n")
    mapFile.flush()
    mapFile.close
    
def mapCreation(currentSpot, totalMapList, numSpaces, squareSize, flag):
    
    # Converts the actual coordinates to the map square system
    coords = F.coordinates(0, 0)
    coords.y = m.floor(currentSpot.y/squareSize)
    coords.x = m.floor(currentSpot.x/squareSize)
    
    if (numSpaces.y > coords.y and numSpaces.x > coords.x and coords.y >= 0 and coords.x >= 0):
        if(flag == 'isEnd'):
            totalMapList[coords.y][coords.x] = 4
        elif (flag == 'isIR'):
            totalMapList[coords.y][coords.x] = 2
        elif (flag == 'isMag'):
            totalMapList[coords.y][coords.x] = 3
        elif (totalMapList[coords.y][coords.x] == 0):
            totalMapList[coords.y][coords.x] = 1

    return totalMapList

#def createObstacleOutput()
        
