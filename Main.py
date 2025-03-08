# Main program for Team 56 Project 3
from Imports56 import *
import Functions56 as F

def main():
    '''
    Settings
    '''

    mode ='point' # Options - objectAvoid, sourceAvoid, point, grid
    distance = 1 # How much the robot moves at a time, centimeters
    robotAngle = 0 # Initial angle of robot - Zero is +y, 90 is -x
    updateSpeed = 0.1 # How often the robot goes through control loop, seconds
    speed = 5 # The default speed of the robot, out of 100 (check?)
    sleepTime = 2 # How long do you want the vehicle to stop after turns?
    
    # object and source avoidance settings
    walldistance = 10 # determines appropriate distance from wall, centimeters
    IRdistance = 1 # Determines radius from IR source, centimeters
    hallDistance = 1 # Determines radius from hall source, centimeters
    deltaAngle = 5 # How many degrees the car should correct itself towards target per loop
    wave = 30 # How many degrees the source avoidance should start waving at
    waveMult = 1.5 # How much should the angle be multiplied each time?
    
    # point turn and grid settings
    pointTurns = [F.TurnObj('left', 90)] # List of Turn instances (direction, degrees)
    ObjectiveCoords = [F.coordinates(3, 4)] # List of coordinates instances (x, y)

    '''
    # End of settings
    '''
    
    '''
    # Multipliers and ports
    '''
    
    # determines appropriate distance multipliers
    walldistanceMult = 1 # It appears that we can keep this at one
    IRdistanceMult = 1
    hallDataMult = 1
    
    # ports of the Grove BuildHat ('A', 'B', 'C', 'D')
    leftPin = 'A'
    rightPin = 'B'
    controlPin = 'C'
    
    # Make sure to only plug in Ultrasonic Sensor to
    # digital ports of the Grove BaseHAT (D5, D16, D18, D22, D24, D26)
    ultraPin = 26 # Front
    ultraPin2 = 5 # Side
    IRpin = 6 # Name the first pin, the second should be right after it
    
    '''
    # Sensor and motor setup and initialization
    '''

    # Set up the motors

    motorLeft = Motor(leftPin) # create instances of Motor class
    motorRight = Motor(rightPin)
    motorControl = Motor(controlPin)
    F.motorSetup([motorLeft, motorRight, motorControl], speed) # Setup instances of the motor class
    wheels = F.Wheel(motorLeft, motorRight) # Create a list which is just both wheels

    # Set up the sensors
    IMU = IMUSensor() # IMU pin is setup automatically, but must be I2C
    ultraFront = UltrasonicSensor(ultraPin)
    ultraSide = UltrasonicSensor(ultraPin2) 
    IR = IRSensor(IRpin, IRpin + 1) # The two IR pins must be next to eachother numerically
    
    '''
    # Start of program logic
    '''
    
    coords = [F.coordinates(0, 0)] # A list of coordinate instances. Starts at zero, gets added to

    if (mode == 'point'):
        for turn in pointTurns: # For each turn we must complete
            # Turn the wheels the appropriate distance (this includes stopping wheels), and update the angle
            robotAngle = F.gyroRotate(IMU, wheels, turn.direction, turn.distance, updateSpeed, speed, robotAngle) 
            time.sleep(sleepTime)
                        
    elif (mode == 'grid'):
        for objective in ObjectiveCoordinates: # For each coordinate we must go to
            
            # Sets the correct orientation of the axes, although angle should really be a multiple of 90
            if ((angle + 45) % 180 < 90):
                axes = [x, y]
            else:
                axes = [y, x]
            
            for axis in axes: # For each axis we need to arrive at
                direction = F.findDirection(coords, objective, angle) # Find direction towards target
                robotAngle = F.gyroRotate(IMU, wheels, direction, 90, updateSpeed, speed, robotAngle) # Turn towards direction, update angle
                delta = objective.axis - coords.axis # find the distance between the points 
                coords = F.moveForward(IMU, wheels, delta, updateSpeed, speed, coords, robotAngle) # Move forward by the difference between the coordinates, update coordinates
                time.sleep(sleepTime)
                
    elif (mode == 'objectAvoid'):
        while(True):
            # Update sensor values
            ultraF = F.trying(ultraFront.getDist)
            ultraS = F.trying(ultraSide.getDist)
            
            if ((type(ultraS) is None) == 0 and (type(ultraF) is None) == 0): # If we have a side value and front value
                ultraValueSide = ultraS * walldistanceMult # Get side value
                ultraValueFront = ultraF * walldistanceMult
                print(ultraValueSide)
                print(ultraValueFront)
                if(ultraValueFront < walldistance): # If we are close to the wall
                    if (ultraValueSide > walldistance): # If the side value is good
                        print("Hi")
                        robotAngle = F.gyroRotate(IMU, wheels, 'right', 90, updateSpeed, speed, robotAngle) # Rotate toward side, update angle
                    else: # If the side value is bad
                        robotAngle = F.gyroRotate(IMU, wheels, 'left', 90, updateSpeed, speed, robotAngle) # Rotate away from side, update angle
                    #time.sleep(sleepTime)
                else: # If we are far from the wall or have no side value
                    coords = F.moveForward(IMU, wheels, distance, updateSpeed, speed, coords, robotAngle) # Move forward distance, update your coordinates
            else:
                print("NULL!!!!")

    elif (mode == 'sourceAvoid'):

        while (True):
            
            # Update sensor values
            IRdistance = F.trying(IRInfo) * IRdistanceMult
            hallData = F.magnitude(F.trying(IMU.getMag())) * hallDataMult
            
            direction = F.findDirection(coords, ObjectiveCoords, rototAngle) # Update best turning direction, probably needs editing
            robotAngle = F.gyroRotate(IMU, wheels, direction, deltaAngle, updateSpeed, robotAngle) # Change angle slightly to go toward objective
            
            # If we are too close to a source
            if ( (IRdata[0] > IRdistance) or (IRdata[1] > IRdistance) or (hallData  > hallDistance) ):
                robotAngle = F.gyroRotate(IMU, wheels, direction, wave, updateSpeed, robotAngle) # Updates the angle as you rotate, rotates 'wave' at a time
                wave = wave * (-waveMult -1)  # Waves in the opposite direction
            else: # If we are not too close to a source
                coords = F.moveForward(IMU, wheels, distance, updateSpeed, speed, coords, robotAngle) # Move forward distance, update your coordinates

if __name__ == '__main__':
    main()
