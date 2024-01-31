'''
Matt Gurgiolo
Prof Bender
CS151 SP22

turtle_interpreter.py
'''
import turtle

class TurtleInterpreter:

    turt = turtle.Turtle()
    screen = turtle.Screen()

    def __init__(self, width=800, height=800, bgColor='white'):
        '''TurtleInterpreter constructor.
        Creates instance variables for a Turtle object and a Screen object with a particular window
        `width`, `height`, and background color `bgColor`.
        '''

        # Create a Screen object, set it as an instance variable.
        # Set the screen's height, width, and color based on the parameters
        self.width = width
        self.height = height
        TurtleInterpreter.screen = turtle.Screen()
        TurtleInterpreter.screen.setup(width, height)
        TurtleInterpreter.screen.bgcolor(bgColor)

        # Turn the screen's tracer off.
        TurtleInterpreter.screen.tracer(False)

    def setColor(self, c):
        #sets the turtles pen color to c
            TurtleInterpreter.turt.color(c)

    def setWidth(self, w):
        #sets the turtles pen width to w
        TurtleInterpreter.turt.pensize(w)
    
    def goto(self, x, y, heading=None):
        #moves and directs the turtle
        TurtleInterpreter.turt.pu()
        TurtleInterpreter.turt.goto(x, y)
        if heading is not None:
            TurtleInterpreter.turt.setheading(heading)
        TurtleInterpreter.turt.pd()
    
    def getScreenWidth(self):
        return self.width
    
    def getScreenHeight(self):
        return self.height
    
    def hold(self):
        '''Holds the screen open until user clicks or presses 'q' key'''

        # Hide the turtle cursor and update the screen
        TurtleInterpreter.turt.hideturtle()
        TurtleInterpreter.screen.update()

        # Close the window when users presses the 'q' key
        TurtleInterpreter.screen.onkey(TurtleInterpreter.screen.bye, 'q')

        # Listen for the q button press event
        TurtleInterpreter.screen.listen()

        # Have the turtle listen for a click
        TurtleInterpreter.screen.exitonclick()
    
    def drawString(self, lsysString, distance, angle):
        '''Interpret each character in an L-system string as a turtle command.
        Here is the starting L-system alphabet:
            F is forward by a certain distance
            + is left by an angle
            - is right by an angle

        Parameters:
        -----------
        lsysString: str. The L-system string with characters that will be interpreted as drawing
            commands.
        distance: distance to travel with F command.
        angle: turning angle (in deg) for each right/left command.
        '''

        # Walk through the lsysString character-by-character and
        # have the turtle object (instance variable) carry out the
        # appropriate commands
        #print(TurtleInterpreter.turt.color())
        turtPos = []
        turtCol = []
        for char in lsysString:
            if char == "F":
                TurtleInterpreter.turt.fd(distance)
            if char == "+":
                TurtleInterpreter.turt.lt(angle)
            if char == "-":
                TurtleInterpreter.turt.rt(angle)
            if char == "[":
                turtPos.append(TurtleInterpreter.turt.xcor())
                turtPos.append(TurtleInterpreter.turt.ycor())
                turtPos.append(TurtleInterpreter.turt.heading())
            if char == "]":
                heading = turtPos.pop()
                ypos = turtPos.pop()
                xpos = turtPos.pop()
                TurtleInterpreter.turt.goto(xpos, ypos, heading)
            if char == '<':
                turtCol.append(TurtleInterpreter.turt.color()[0])
            if char == '>':
                TurtleInterpreter.turt.color(turtCol[0])
            if char == 'g':
                TurtleInterpreter.turt.pencolor((0.15, 0.5, 0.2))
                TurtleInterpreter.turt.fillcolor((0.15, 0.5, 0.2))
            if char == 'y':
                TurtleInterpreter.turt.pencolor((0.8, 0.8, 0.3))
                TurtleInterpreter.turt.fillcolor((0.8, 0.8, 0.3))
            if char == 'r':
                TurtleInterpreter.turt.pencolor((0.7, 0.2, 0.3))
                TurtleInterpreter.turt.fillcolor((0.7, 0.2, 0.3))
            if char == 'L':
                TurtleInterpreter.turt.circle(distance/2, 150)
            if char == 'B':
                TurtleInterpreter.turt.begin_fill()
                TurtleInterpreter.turt.circle(distance/6, 360)
                TurtleInterpreter.turt.end_fill()
            if char == '{':
                TurtleInterpreter.turt.begin_fill()
            if char == '}':
                TurtleInterpreter.turt.end_fill()

        # Call the update method on the screen object to make sure
        # everything drawn shows up at the very end of the method
        # (remember: you turned off animations in the constructor)
        TurtleInterpreter.turt.hideturtle()
        TurtleInterpreter.screen.update()
        # self.hold()