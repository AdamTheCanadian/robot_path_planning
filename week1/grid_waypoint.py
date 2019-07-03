#!/usr/bin/env python

class GridWayPoint:

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
    def __eq__(self, rhs):
        return (self.x == rhs.x and self.y == rhs.y and self.z == rhs.z)

    def __ne__(self, rhs):
        return not (self == rhs)

    def __str__(self):
        return 'Grid Waypoint(%s, %s)' % (self.x, self.y)

    def __repr__(self):
        return str(self)
    
    def __lt__(self, value):
        dist = abs(self.x) + abs(self.y)
        dist2 = abs(value.x) + abs(value.y)
        return dist < dist2