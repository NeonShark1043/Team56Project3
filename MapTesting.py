# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 16:41:01 2025

@author: norwo
"""

'''
Team: 56
Map: #
Unit length: 40
Unit: cm
origin: (0,0)
example list

'''
mapNum = int(input("Input a map number: "))
numSpacesX = int(input("Enter the length of the x grid: "))
numSpacesY = int(input("Enter the length of the y grid: "))
mapListSmall = []
totalMapList = []
mapFile = open("theMap",'w')
currentSpot = [0,0]

''' Most likely entered in another function'''
xcord = 1
ycord = 1
intendedPoint = [xcord,ycord]

def createMapBlank(numSpacesX,numSpacesY,mapListSmall,totalMapList):
    '''creates a blank map'''
    for i in range (numSpacesY):
        while numSpacesX > 0:
            mapListSmall.append(0)
            numSpacesX = numSpacesX -1
        totalMapList.append(mapListSmall)

def mapCreation(distance, angle, currentspot,totalMapList):
    
    perivousSpot = currentspot
    
    if angle == 0:    
        if distance % 40 == 0:
            currentSpot[1] =  currentSpot[1] + 1
    if angle == 90:
        if distance % 40 == 0:
            currentSpot[0] =  currentSpot[0] + 1
    if angle == -90:
        if distance % 40 == 0:
            currentSpot[0] =  currentSpot[0] - 1
    if angle == 180:
        if distance % 40 == 0:
            currentSpot[1] =  currentSpot[1] - 1
    #if perivousSpot[0] != currentspot[0] or perivousSpot[1] != currentspot[1]:
        # Addes the current spot of the robot to the list
        # currentSpot[1] is the y coordinate
        # currentSpot[0] is the x coordinate
    #updates the current spot
    totalMapList[currentSpot[1]][currentSpot[0]] = 1
    
createMapBlank(numSpacesX,numSpacesY,mapListSmall,totalMapList)
mapCreation(40,0,currentSpot,totalMapList)
print(currentSpot)
print(totalMapList)
print(totalMapList[currentSpot[1]][currentSpot[0]])

