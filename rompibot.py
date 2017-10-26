

from breezyslam.robots import WheeledRobot


import math

class RompiBot(WheeledRobot):
    
    def __init__(self):
        
        WheeledRobot.__init__(self, 70,150)
        
        self.ticks_per_cycle = 1
                        
    def __str__(self):
        
        return '<%s ticks_per_cycle=%d>' % (WheeledRobot.__str__(self), self.ticks_per_cycle)
        
    def computeVelocities(self, odometry):
        
        return WheeledRobot.computeVelocities(self, odometry[0], odometry[1], odometry[2])

    def extractOdometry(self, timestamp, leftWheel, rightWheel):
                
        # Convert microseconds to seconds, ticks to angles        
        return timestamp, \
               self._ticks_to_degrees(leftWheel), \
               self._ticks_to_degrees(rightWheel)
               
    def odometryStr(self, odometry):
        
        return '<timestamp=%d usec leftWheelTicks=%d rightWheelTicks=%d>' % \
               (odometry[0], odometry[1], odometry[2])
               
    def _ticks_to_degrees(self, ticks):
        
        return ticks 

