'''
Matt Gurgiolo
Prof Bender
CS151 SP22

shapes.py
'''

import turtle_interpreter as ti

class Shape:

    def __init__(self, distance=100, angle=90, color=(0, 0, 0), lsysString=''):
        '''Shape constructor

        Parameters:
        -----------
        distance: float. Distance in pixels to go when moving the turtle forward
        angle: float. Angle in degrees to turn when turning the turtle left/right
        color: tuple of 3 floats. Default turtle pen color
        lsysString: str. The L-system string of drawing commands to draw the shape
            (e.g. made up of 'F', '+', '-', ...)
        '''

        # Create instance variables for all the parameters
        self.distance = distance
        self.angle = angle
        self.color = color
        self.lsysString = lsysString
        # Create an instance variable for a new TurtleInterpreter object
        self.terp = ti.TurtleInterpreter()

    def getTI(self):
        return self.terp
        
    def getString(self):
        return self.lsysString
    
    def setColor(self, c):
        self.terp.setColor(c)
    
    def setDistance(self, dist):
        self.distance = dist
    
    def setAngle(self, a):
        self.angle = a
    
    def setString(self, s):
        self.lsysString = s

    def draw(self, x_pos, y_pos, scale=1.0, heading=0):
        '''Draws the L-system string at the position `(x, y)` = `(x_pos, y_pos)` with the turtle
        facing the heading `heading`. The turtle drawing distance is scaled by `scale`.
        '''
        self.terp.goto(x_pos, y_pos, heading)
        self.terp.setColor(self.color)
        self.terp.drawString(self.lsysString, self.distance*scale, self.angle)

class Square(Shape):

    def __init__(self, distance=100, color=(0, 0, 0), fill=False):
        # Create a variable for the L-system string that would draw a square.
        self.distance = distance
        self.color = color
        self.fill = fill
        self.lsysString = 'F+F+F+F+'
        
        # if the fill parameter is true, concatenate the { and } characters
        # to the beginning and end of the L-system string,
        # updating the value of the L-system string.
        if fill == True:
            filling = '{' 
            filling += self.lsysString 
            filling += '}'
            self.lsysString = filling
        # Call the parent's constructor, passing along values for all its
        # parameters.

        Shape.__init__(self, distance, 90, self.color, self.lsysString)

class Triangle(Shape):

    def __init__(self, distance=100, color=(0, 0, 0), fill=False):
        # Create a variable for the L-system string that would draw a triangle.
        self.distance = distance
        self.color = color
        self.fill = fill
        self.lsysString = 'F+F+F+'
        
        # if the fill parameter is true, concatenate the { and } characters
        # to the beginning and end of the L-system string,
        # updating the value of the L-system string.
        if fill == True:
            filling = '{' 
            filling += self.lsysString 
            filling += '}'
            self.lsysString = filling
        # Call the parent's constructor, passing along values for all its
        # parameters.

        Shape.__init__(self, distance, 120, self.color, self.lsysString)
    
class Star(Shape):

    def __init__(self, distance=100, color=(0, 0, 0), fill=False):
        # Create a variable for the L-system string that would draw a star.
        self.distance = distance
        self.color = color
        self.fill = fill
        self.lsysString = 'F+F+F+F+F+'
        
        # if the fill parameter is true, concatenate the { and } characters
        # to the beginning and end of the L-system string,
        # updating the value of the L-system string.
        if fill == True:
            filling = '{' 
            filling += self.lsysString 
            filling += '}'
            self.lsysString = filling
        # Call the parent's constructor, passing along values for all its
        # parameters.

        Shape.__init__(self, distance, 144, self.color, self.lsysString)

def testShapes():
    square = Square(color='light blue', fill=True)
    triangle = Triangle(color='red', fill=True)
    star = Star(color='orange', fill=True)

    square.draw(-200, 0, 1, 0)
    triangle.draw(0, 200, 1, 0)
    star.draw(100, -200, .75, )

    square.getTI().hold()

if __name__ == '__main__':
    testShapes()