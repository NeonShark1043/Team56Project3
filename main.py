from Imports56 import *
import MazeRobotFunctions as F
import MapTesting as mapFun
import math as m

def main():
    
    wallDistance = 18 # What is the distance between the walls? (cm)
    IRthreshold = 160 # When should we say that there is clearly an IR source?
    Magthreshold = 125 # When should we say that there is clearly a magnetic source?
    IRmax = IRthreshold
    magMax = Magthreshold
    nullDist = 10000 # Must be far greater than how far the sensor can see
    sensorSum = 2 # How many sensor values are averaged out
    originX = 2 # What is our initial X coordinate?
    originY = 2 # What is our initial Y coordinate?
    increment = 90
        
    mapNum = 1 # Name the map
    numSpacesX = 18 # x dimension of map
    numSpacesY = 11 # y dimension of map
    squareSize = 0.4 # Size of each square
    numSpaces = F.coordinates(numSpacesX, numSpacesY) # numSpaces is a coordinate system of map dimensions
    totalMapList = mapFun.createMapBlank(numSpaces)
    origin = F.coordinates(originX,originY) # origin is a coordinate system of the origin 
    currentSpot = F.coordinates(originX * squareSize, originY * squareSize) # Current spot, in real terms
    totalMapList[origin.y][origin.x] = 5 # Set the origin to "5"
    magCoords = F.coordinates(-1, -1) # Set the magnet and IR coordinates to an invalid state
    IRCoords = F.coordinates(-1, -1) # This shows that they have not been found
    
    # create instances of Motor class
    motorL = Motor('A') 
    motorR = Motor('B')
    motorC = Motor('C')
    wheels = F.Wheel(motorL, motorR)
    
    # Zero out the sensor lists
    frontList = []
    sideListRight2 = []
    sideListRight1 = []
    magList = []
    IRList = []
    for i in range(sensorSum):
        frontList.append(0)
        sideListRight2.append(0)
        sideListRight1.append(0)
        magList.append(0)
        IRList.append(0)
        
    # Get frontUltra, sideUltra, magVal, and IRVal
    ultraPin = 26 # Front
    ultraPin2 = 5 # Side Right
    ultraPin3 = 18 # side left
    IRpin = 6 # Name the first pin, the second should be right after it
        
    # Set up the sensors
    IMU = IMUSensor() # IMU pin is setup automatically, but must be I2C
    ultraFront = UltrasonicSensor(ultraPin)
    ultraRight1 = UltrasonicSensor(ultraPin3) # 1st is in front
    ultraRight2 = UltrasonicSensor(ultraPin2) # 2nd is in back
    IR = IRSensor(IRpin, IRpin + 1) # The two IR pins must be next to eachother numerically
        
    # Get all of the setupt before the main loop - whether to go into a loop and the change in coordinates
    fillingSensorVals = 0 
    recentChoice = 0
    dCoords = F.coordinates(0,0) # dCoords represents the coordinates relative to the previous ones and the absolute angle
    
    gain = 0.2 # gain of the wall correction

    try:
        while(True):
            time.sleep(0.01) # This is to prevent things from going too fast...
            dCoords.resetDisplacement() # reset the position and the angle
        
            for i in range(sensorSum):
                # Get the values
                time.sleep(0.35)
                ultraF = F.nullDefault(ultraFront.getDist, nullDist)
                time.sleep(0.01)
                ultraR2 = F.nullDefault(ultraRight2.getDist, nullDist)
                time.sleep(0.01)
                ultraR1 = F.nullDefault(ultraRight1.getDist, nullDist)
                time.sleep(0.01)
                IRval = ( F.nullDefault(IR.value1) + F.nullDefault(IR.value2) ) / 2
                time.sleep(0.01)
                IMUval = F.magnitude(F.nullDefaultList(IMU.getMag()))

                # Update the list of sensor values
                sumFront, frontList = F.pushNpopAvg(ultraF, frontList, sensorSum)
                sumSideRight2, sideRightList2 = F.pushNpopAvg(ultraR2, sideListRight2, sensorSum)
                sumSideRight1, sideRightList1 = F.pushNpopAvg(ultraR1, sideListRight1, sensorSum)
                sumIR, IRList = F.pushNpopAvg(IRval, IRList, sensorSum)
                sumMag, magList = F.pushNpopAvg(IMUval, magList, sensorSum)
        
                if (sumIR > IRmax):
                    IRmax = sumIR  # Make the IR value your new maximum
                    # Set your current positon equal to the new IR coordinates
                    IRCoords.x = m.floor(currentSpot.x/squareSize)
                    IRCoords.y = m.floor(currentSpot.y/squareSize)
                elif (sumMag > magMax):
                    magMax = sumMag # Make the magnetic field your new maximum
                    # Set your current positon equal to the new mag coordinates
                    magCoords.x = m.floor(currentSpot.x/squareSize)
                    magCoords.y = m.floor(currentSpot.y/squareSize)
                
            # Are we too close to something?
            # The way that this was programmed prioritizes the hazards over null values / end of map           
            currentWallDistanceFront = sumFront
            currentWallDistanceRight2 = sumSideRight2
            currentWallDistanceRight1 = sumSideRight1
            print(frontList, sideRightList1, sideRightList2)

            if (sumFront < wallDistance or sumIR > IRthreshold or sumMag > Magthreshold):
                sumFront = 0
            if (sumSideRight2 < wallDistance * 1.5):
                sumSideRight2 = 0
            if (sumSideRight1 < wallDistance * 1.5):
                sumSideRight1 = 0
            if (sumMag > Magthreshold):
                sumMag = 0
                print("Mag")
            else:
               sumMag = 1
            if (sumIR > IRthreshold):
                sumIR = 0
                print("IR")
            else:
                sumIR = 1
            
            # Set up the lists of indicators used for pathfinding
            sumFront = (sumIR and sumMag) * sumFront
            
            critical = nullDist/2 + 100
            nulls = [sumFront >= critical, sumSideRight2 >= critical, sumSideRight1 >= critical, 0]
            valid = [sumFront != 0, sumSideRight2 != 0, sumSideRight1 != 0, 0]
            
            i = 0
            if nulls[0] == True:
                i += 1
            if nulls[1] == True:
                i += 1
            nulls[3] = i
        
            i = 0
            if valid[0] == True:
                i += 1
            if valid[1] == True:
                i += 1
            valid[3] = i
            
            print(nulls)
        
            if(sumMag == 0 or sumIR == 0):
                F.turnCommand(wheels, dCoords, -90)
                time.sleep(0.5)
                F.turnCommand(wheels, dCoords, -90)
            elif (nulls[3] == 2 and nulls[2] == True): # If we are outside of the maze (cannot see anything), do ending instructions
            
                print("Done!")
                # Move forward a LOT
                motorC.run_for_degrees(-480) # Open hatch
                time.sleep(2)
                wheels.forward(360) # Move forward so that you don't close on the object
                motorC.run_for_degrees(540) # Close hatch
                wheels.turn(-320) # Do a wheelie (to avoid seeming threatening)
                wheels.forward(360) # Move away from box
            
                # Add the IR position
                if (numSpaces.y > IRCoords.y and numSpaces.x > IRCoords.x and IRCoords.y >= 0 and IRCoords.x >= 0):
                    totalMapList[IRCoords.y][IRCoords.x] = 2
                # Add the Mag position
                if (numSpaces.y > magCoords.y and numSpaces.x > magCoords.x and magCoords.y >= 0 and magCoords.x >= 0):
                    totalMapList[magCoords.y][magCoords.x] = 3
                    
                totalMapList[m.floor(currentSpot.x/squareSize)][m.floor(currentSpot.y/squareSize)] = 4
                        
                mapFun.printHazards(IRthreshold, IRCoords, Magthreshold, magCoords, mapNum)
            
                mapFun.mapCreation(currentSpot, totalMapList, numSpaces, squareSize, 'isEnd')
                mapFun.exportMap(totalMapList, mapNum, origin)
                time.sleep(10000) # end program
            
            elif(nulls[0] == True): # If the forward direction is null, go forward
            
                print("Forward is null")
                F.forwardCommand(wheels, dCoords, increment)
            
            elif(nulls[1] == True): # If there are nulls other than the forward direction, choose a direction
            
                print("There are non forward nulls")
                F.turnCommand(wheels, dCoords, -90)
            
            elif(valid[0] == True or valid[1] == True): # If there is a valid direction, choose a direction
            
                print("There is a valid direction")
                if (recentChoice and valid[0] != 0): # If we have recently decided on one option 
                    F.forwardCommand(wheels, dCoords, increment)
                else:
                    recentChoice = sensorSum + 20 # We need to prevent ourselves from choosing again
                    F.chooseCommand(wheels, dCoords, increment, valid)
                
            elif(valid[3] == 0): # If there is no valid direction, turn around
                print("There is no valid direction")
                F.turnCommand(wheels, dCoords, 90)
            else:
                print("There was an error in the central control system")
            
            status = 0

            for i in sideRightList1:
                if i == nullDist:
                    status = 1
            for i in sideRightList2:
                if i == nullDist:
                    status = 1
               
            print(currentWallDistanceRight2, currentWallDistanceRight1)
            deltaH = currentWallDistanceRight2 - currentWallDistanceRight1 - 0.1
        
        
            if (deltaH < 19.5 and deltaH > -19.5 and currentWallDistanceFront > 40):
                print ("the distance is high enough")
                angle = m.atan2(deltaH, 7)
                if (status == 0):
                    wheels.turn(angle*180/m.pi)
                
            # Correct
            if (currentWallDistanceRight1 > 9.5 + 1.5 and status == 0 and currentWallDistanceFront > 40 and deltaH < 19.5 and deltaH > -19.5):
                wheels.turn(-30)
                wheels.forward(40)
                wheels.turn(30)
            if (currentWallDistanceRight1 < 9.5 + 1.5 and status == 0 and currentWallDistanceFront > 40 and deltaH < 19.5 and deltaH > -19.5):
                wheels.turn(30)
                wheels.forward(40)
                wheels.turn(-30)
                   
            currentSpot.updateCoords(dCoords) # use the displacement coordinates to update the current spot
            mapFun.mapCreation(currentSpot, totalMapList, numSpaces, squareSize, 0) # Use this information to update the map
            
            if(recentChoice > 0): # One less loop until a new choice can be made 
                recentChoice -= 1
            fillingSensorVals = sensorSum + 1 # Get a new batch of sensor values
        
    except KeyboardInterrupt:
        print("Escape")
        # Move forward a LOT
        time.sleep(10000) # end program
        
        motorC.run_for_degrees(-480) # Open hatch
        time.sleep(2)
        wheels.forward(360) # Move forward so that you don't close on the object
        motorC.run_for_degrees(540) # Close hatch
        wheels.turn(-320) # Do a wheelie (to avoid seeming threatening)
        wheels.forward(360) # Move away from box
            
        # Add the IR position
        if (numSpaces.y > IRCoords.y and numSpaces.x > IRCoords.x and IRCoords.y >= 0 and IRCoords.x >= 0):
            totalMapList[IRCoords.y][IRCoords.x] = 2
        # Add the Mag position
        if (numSpaces.y > magCoords.y and numSpaces.x > magCoords.x and magCoords.y >= 0 and magCoords.x >= 0):
            totalMapList[magCoords.y][magCoords.x] = 3
                        
        totalMapList[m.floor(currentSpot.x/squareSize)][m.floor(currentSpot.y/squareSize)] = 4
        mapFun.printHazards(IRthreshold, IRCoords, Magthreshold, magCoords, mapNum)
            
        mapFun.mapCreation(currentSpot, totalMapList, numSpaces, squareSize, 'isEnd')
        mapFun.exportMap(totalMapList, mapNum, origin)
        time.sleep(10000) # end program
        

            
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