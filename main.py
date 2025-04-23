from Imports56 import *
import MazeRobotFunctions as F
import MapTesting as mapFun
import math as m
import random

def main():
    
    wallDistance = 18 # What is the distance between the walls? (cm)
    IRthreshold = 700 # When should we say that there is clearly an IR source?
    Magthreshold = 700 # When should we say that there is clearly a magnetic source?
    nullDist = 10000 # Must be far greater than how far the sensor can see
    sensorSum = 12 # How many sensor values are averaged out
    originX = 20 # What is our initial X coordinate?
    originY = 15 # What is our initial Y coordinate?
        
    mapNum = 1 # Name the map
    numSpacesX = 55 # x dimension of map, 55
    numSpacesY = 30 # y dimension of map, 30
    squareSize = 120 # Size of each square
    numSpaces = F.coordinates(numSpacesX, numSpacesY) # numSpaces is a coordinate system of map dimensions
    mapFile = open("theMap",'w') # Open the map file to write
    totalMapList = mapFun.createMapBlank(numSpaces)
    origin = F.coordinates(originX,originY) # origin is a coordinate system of the origin 
    currentSpot = F.coordinates(originX * squareSize, originY * squareSize)
    totalMapList[origin.y][origin.x] = 5
    
    # create instances of Motor class
    motorL = Motor('A') 
    motorR = Motor('B')
    motorC = Motor('C')
    wheels = F.Wheel(motorL, motorR)
    
    # Zero out the sensor lists
    frontList = []
    sideList = []
    magList = []
    IRList = []
    for i in range(sensorSum):
        frontList.append(0)
        sideList.append(0)
        magList.append(0)
        IRList.append(0)
        
    # Get frontUltra, sideUltra, magVal, and IRVal
    ultraPin = 26 # Front
    ultraPin2 = 5 # Side
    IRpin = 6 # Name the first pin, the second should be right after it
        
    # Set up the sensors
    IMU = IMUSensor() # IMU pin is setup automatically, but must be I2C
    ultraFront = UltrasonicSensor(ultraPin)
    ultraSide = UltrasonicSensor(ultraPin2) 
    IR = IRSensor(IRpin, IRpin + 1) # The two IR pins must be next to eachother numerically
        
    # Get all of the setupt before the main loop - whether to go into a loop and the change in coordinates
    fillingSensorVals = 0 
    recentChoice = 0
    dCoords = F.coordinates(0,0) # dCoords represents the coordinates relative to the previous ones and the absolute angle

    while(True):
        time.sleep(0.01) # This is to prevent things from going too fast...
        dCoords.resetDisplacement() # reset the position and the angle
        
        for i in range(sensorSum + 1):
            # Get the values
            ultraF = F.nullDefault(ultraFront.getDist, nullDist)
            ultraS = F.nullDefault(ultraSide.getDist, nullDist)
            IRval = ( F.nullDefault(IR.value1) + F.nullDefault(IR.value2) ) / 2
            IMUval = F.magnitude(F.nullDefaultList(IMU.getMag()))

            # Update the list of sensor values
            sumFront, frontList = F.pushNpopAvg(ultraF, frontList, sensorSum)
            sumSide, sideList = F.pushNpopAvg(ultraS, sideList, sensorSum)
            sumIR, IRList = F.pushNpopAvg(IRval, IRList, sensorSum)
            sumMag, magList = F.pushNpopAvg(IMUval, magList, sensorSum)
        
            flag = ""
            # Are we too close to something?
            # The way that this was programmed prioritizes the hazards over null values / end of map           
            if (sumFront < wallDistance or sumIR > IRthreshold or sumMag > Magthreshold):
                sumFront = 0
            if (sumSide < wallDistance):
                sumSide = 0
            if (sumMag > Magthreshold):
                sumMag = 0
                flag = "isMag"
            if (sumIR > IRthreshold):
                sumIR = 0
                flag = "isIR"
            
            # sumFront is used to check for nulls / end of map, front is used for everything else
            front = sumFront and sumIR and sumMag
         # We probably want to add something that prioritizes going towards the path we have not seen yet
        #print(currentSpot.x, currentSpot.y)
        if(sumFront == nullDist and sumSide == nullDist): # If we are outside of the maze (cannot see anything), do ending instructions
            print("Done!")
            motorC.run_for_degrees(480)
            time.sleep(1)
            motorC.run_for_degrees(-480)
            time.sleep(2)
            wheels.forward(360)
            motorC.run_for_degrees(540)
            wheels.turn(-320)
            wheels.forward(360)
            mapFun.mapCreation(currentSpot, totalMapList, numSpaces, squareSize, 'isEnd')
            mapFun.exportMap(totalMapList, mapFile, mapNum, origin)
            time.sleep(10000) # end program
            # If the thing on the right is on the outside of the maze or we can go right but not forwards
        elif( (sumFront != nullDist and sumSide == nullDist) or (not front and sumSide) ): 
            wheels.turn(-90) # turn right
            dCoords.angle -= 90
            # If the thing in front of us is the outside of the maze or we can go forwards but not sideways
        elif( (sumFront == nullDist and sumSide != nullDist) or (front and not sumSide) ):
            wheels.forward(30) # go forward
            dCoords.y += 30
        elif(front and sumSide): # If both going forward and right are valid options
            if (recentChoice): # If we have recently decided on one option 
                wheels.forward(30)
                dCoords.y += 30
            else:
                recentChoice = sensorSum + 1 # We need to prevent ourselves from choosing again
                if(random.choice([0,1])): # 50/50 odds
                    wheels.forward(30) # go forward
                    dCoords.y += 30
                    print("Forward")
                else:
                    wheels.turn(-90) # go right
                    dCoords.angle -= 90
                    print("Right") 
        elif(not front and not sumSide):
            wheels.turn(90) # go left
            dCoords.angle += 90
        else:
            print("There was an error in the navigation system")
                
        currentSpot.updateCoords(dCoords) # use the displacement coordinates to update the current spot
        print(currentSpot.x, currentSpot.y)
        mapFun.mapCreation(currentSpot, totalMapList, numSpaces, squareSize, flag) # Use this information to update the map
            
        if(recentChoice > 0): # One less loop until a new choice can be made 
            recentChoice -= 1
        fillingSensorVals = sensorSum + 1 # Get a new batch of sensor values
        
        '''
        deltaCoordinates = 0 # Coordinate system can be update to include angle - why not? 
        (Note - these average out over past N values)
        get frontUltra sensor value + pushnpop
        get sideUltra sensor value + pushnpop
        get magnetic sensor value + pushnpop
        get IR sensor value (front) + pushnpop
        front = !frontUltra and !IR and !magnetic
        side = sideUltra
        if (side and front undefined):
            move forward for 3 seconds
            drop cargo
            assure safety of cargo
            break;
        elif (side undefined and front defined):
            turn right
            move forward
        elif (front undefined and side defined):
            move forward
        elif (side and front): 
            if(random.choice([0,1] and cooldown):
                move forward
            else:
                turn right
                set cooldown to zero
        elif (side and not front):
            move forward
            set cooldown to one
        elif(not front and side):
            turn right
            set cooldown to one
        elif(not front and not side):
            turn left
            set cooldown to one
        update coordinates and map1 and map2
        '''

               
if __name__ == '__main__':
    main()