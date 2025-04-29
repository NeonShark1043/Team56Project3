import MapTesting as mapFun
import MazeRobotFunctions as F

def main():
    numSpaces = F.coordinates(5, 5)
    mapping = mapFun.createMapBlank(numSpaces)
    position = F.coordinates(2,2)
    mapping[position.y][position.x] = 3
    retList = mapFun.findPath(mapping, position, 1, numSpaces)
    position.x += 1
    position.angle -= 90
    retList = mapFun.findPath(mapping, position, 1, numSpaces)
    print(retList)
    mapping[position.y][position.x] = 5
    print(mapping)
               
if __name__ == '__main__':
    main()
