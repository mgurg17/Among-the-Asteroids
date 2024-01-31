'''
Matt Gurgiolo
Prof Bender
CS151 SP22

asteroids.py
rocketship.gif acquired from Biran Marks at https://blog.trinket.io/using-images-in-turtle-programs/ and the Roketship0 to Rocketship 350 were provided by Prof Bender
asteroid.gif
enemy.gif
'''
import turtle
import random
import shapes
import time

#calling this class runs the game
class Game:

    screen = turtle.Screen()

    def __init__(self, level, lives, enemiesKilled):
        # this creates the screen
        Game.screen = turtle.Screen()
        Game.screen.setup(800, 800)
        Game.screen.mode('logo')
        self.drawbackground()
        Game.screen.bgcolor('blue')
        self.playing = True

        highscoreFile = open("highscore.txt", "r")
        self.rawtext = highscoreFile.read()
        self.scorenplayer = self.rawtext.split()
        self.highscore = int(self.scorenplayer[1])
        self.bestplayer = self.scorenplayer[0]
        
        highscoreFile.close()

        #this sets all the variables needed for the game
        self.level = level
        self.lives = lives
        self.invincibility = 0
        self.enemiesKilled = enemiesKilled
        self.speed = 20
        self.turnRate = 10
        self.rocketsList = []
        self.minxenemy = -350
        self.minyenemy = 0
        self.maxxenemy = 350
        self.maxyenemy = 350
        self.enemies = []
        self.asteroids = []
        self.collisionRadius = 30
        self.score = 0 + self.enemiesKilled
        self.numberOfAsteroids = 4*self.level
        self.speedOfAsteroids = 3+self.level
        self.n = 5*self.level

        self.play()

    #the loop of the game, sets the screen to listen for inputs and to update regularly
    def play(self):
        '''Turns the tracer animations on (but speeds up animations) and starts the main game loop.
        '''
        self.showControls()
        self.player = self.makePlayer()
        self.makeEnemies(self.n-self.enemiesKilled)
        self.makeAsteroids(self.numberOfAsteroids)
        #this creates the score board, sets up the movement, and starts the game loop
        self.createScoreBoard()
        self.setupEvents()
        Game.screen.update()
        # Call the tracer method on your `Screen` class variable,
        # passing in True as the parameter to turn animations on.
        Game.screen.tracer(False)

        # Call the listen method on your `Screen` class variable
        # so that keyboard presses are not registered as events
        Game.screen.listen()

        # Call the mainloop method on your `Screen` class variable.
        Game.screen.mainloop()

    #this creates the player, and registers all the possible orientations of the ship
    def makePlayer(self):
        turt = turtle.Turtle()
        # for file in os.listdir('/Users/mgurg/OneDrive/Desktop/CS151/Lab10'):
        #     if file.endswith('.gif'):
        #         print(file)
        for i in range(0, 370, 10):
            filename = "imgs\Rocketship"+str(i%360)+".gif"
            Game.screen.register_shape(filename)
            self.rocketsList.append(filename)
        #print(self.rocketsList)

        turt.shape(self.rocketsList[0])
        turt.penup()
        turt.goto(0, -200)
        turt.setheading(0)
        return turt
    
    # the next four code the movements of the player, up/down and turning
    def up(self):
        self.player.forward(self.speed)
        Game.screen.update()

    def down(self):
        self.player.back(self.speed)
        Game.screen.update()
    
    def left(self):
        self.player.left(self.turnRate)
        self.player.shape(self.rocketsList[int((360-self.player.heading())/10)])
        Game.screen.update()

    def right(self):
        self.player.right(self.turnRate)
        self.player.shape(self.rocketsList[int((360-self.player.heading())/10)])
        Game.screen.update()



    #this sets up the controls by mapping the keys to the above functions
    def setupEvents(self):
        Game.screen.onkeypress(self.up, "Up")
        Game.screen.onkeypress(self.down, "Down")
        Game.screen.onkeypress(self.right, "Right")
        Game.screen.onkeypress(self.left, "Left")
        Game.screen.onkeypress(self.endGame, "q")
        Game.screen.onkeypress(self.beatLevel, "b")

        Game.screen.ontimer(self.moveAsteroids, 50)
        Game.screen.ontimer(self.checkForCollision, 50)
        Game.screen.ontimer(self.moveEnemiesRandomly, 50)

    #this is what randomly moves the enemies to the top 3rd of the screen
    def placeEnemyRandomly(self, turt: turtle.Turtle):
        randx = random.randint(self.minxenemy, self.maxxenemy)
        randy = random.randint(self.minyenemy, self.maxyenemy)
        turt.penup()
        turt.goto(randx, randy)
        Game.screen.update()

    def placeAsteroid(self, turt: turtle.Turtle):
        randx = random.randint(self.minxenemy, self.maxxenemy)
        randy = random.randint(200, self.maxyenemy)
        turt.penup()
        turt.goto(randx, randy)
        Game.screen.update()

    def resetAsteroid(self, turt: turtle.Turtle):
        randx = random.randint(self.minxenemy, self.maxxenemy)
        y = random.randint(390, 450)
        turt.penup()
        turt.goto(randx, y)
        Game.screen.update()

    #this makes the enemies depending on the input
    def makeEnemies(self, n):
        for i in range(n):
            turt = turtle.Turtle()
            turt.hideturtle()
            turt.speed(10)
            turt.penup()
            self.placeEnemyRandomly(turt)
            enemyImage = 'imgs\Enemy.gif'
            Game.screen.register_shape(enemyImage)
            turt.shape(enemyImage)
            turt.color('red')
            turt.showturtle()
            self.enemies.append(turt)
        Game.screen.update()

    def makeAsteroids(self, numberOfAsteroids):
        for i in range(numberOfAsteroids):
            turt = turtle.Turtle()
            turt.hideturtle()
            turt.speed(10)
            turt.penup()
            self.placeAsteroid(turt)
            asteroidImage = 'imgs\Asteroid.gif'
            Game.screen.register_shape(asteroidImage)
            turt.shape(asteroidImage)
            turt.showturtle()
            self.asteroids.append(turt)
        Game.screen.update()

    #this is what makes the enemeies appear to move back and forth a bit 
    def moveEnemiesRandomly(self):
        if self.playing:
            for enemy in self.enemies:
                enemy: turtle.Turtle
                xmove = random.randint(-5, 5)
                ymove = random.randint(-5, 5)
                if enemy.pos()[0] > 350:
                    xmove = -5
                if enemy.pos()[0] < -350:
                    xmove = 5
                if enemy.pos()[1] > 350:
                    ymove = -5
                if enemy.pos()[1] < 200:
                    ymove = 5
                enemy.penup()
                enemy.goto(int(enemy.xcor()+xmove), int(enemy.ycor()+ymove))
                enemy.pendown()
            Game.screen.update()
            Game.screen.ontimer(self.moveEnemiesRandomly, 50)

    def moveAsteroids(self):
        if self.playing: 
            for asteroid in self.asteroids:
                asteroid: turtle.Turtle
                asteroid.penup()
                asteroid.goto(int(asteroid.xcor()), int(asteroid.ycor()-self.speedOfAsteroids))
                if asteroid.pos()[1] < -380:
                    self.resetAsteroid(asteroid)
                asteroid.pendown()
            Game.screen.update()
            Game.screen.ontimer(self.moveAsteroids, 50)

    #this checks to see if the player is too close to an enemy, and it prints boom!, adds to the score, and moves the enemy randomly if they are
    def checkForCollision(self):
        if self.playing:
            for enemy in self.enemies: 
                if self.player.distance(enemy.pos()) < self.collisionRadius:
                    print('Blam!')
                    enemy.penup()
                    enemy.goto(10000, 100000)
                    enemy.pendown()
                    self.score += 1
                    self.scoreBoard.clear()
                    self.scoreBoard.write(str(self.score)+"/"+str(self.n), font=("Verdana", 25, "bold"))
            if self.invincibility == 0:
                for asteroid in self.asteroids:
                    if self.player.distance(asteroid.pos()) < self.collisionRadius:
                        print('BOOM!')
                        self.loseLife()
            if self.score == self.n:
                self.beatLevel()
            Game.screen.update()
            Game.screen.ontimer(self.checkForCollision, 50)

    #this ends the game on press q, and shows the score and clears the screen
    def endGame(self):
        Game.screen.clear()
        Game.screen.tracer(False)
        self.playing = False
        self.highScore()
        self.drawbackground()
        Game.screen.bgcolor('light blue')
        turtleDrawer = turtle.Turtle()
        turtleDrawer.hideturtle()
        turtleDrawer.penup()
        turtleDrawer.goto(0, 0)
        turtleDrawer.write("           You Lose!\nYou have no more lives!\n     You beat " + str(self.level-1) + " levels", False, "center", font=("Verdana", 25, "bold"))
        Game.screen.update()
        time.sleep(5)
        Game.screen.bye()

    def loseLife(self):
        self.lives += -1
        if self.lives == 0:
            self.endGame()
        else:
            Game.screen.clear()
            Game.screen.tracer(False)
            self.playing = False
            self.drawbackground()
            Game.screen.bgcolor('light blue')
            turtleDrawer = turtle.Turtle()
            turtleDrawer.hideturtle()
            turtleDrawer.penup()
            turtleDrawer.goto(0, 0)
            turtleDrawer.write("   You hit an asteroid!\nYou only have " + str(self.lives) + " lives left.", False, "center", font=("Verdana", 25, "bold"))
            Game.screen.update()
            time.sleep(2)
            Game.screen.clear()
            Start(self.level, self.lives, self.score)
        Game.screen.update()

        #self.screen.ontimer(Game.screen.bye, 2000)


    def beatLevel(self):
        Game.screen.clear()
        Game.screen.tracer(False)
        self.drawbackground()
        Game.screen.bgcolor('light blue')
        turtleDrawer = turtle.Turtle()
        turtleDrawer.hideturtle()
        turtleDrawer.penup()
        turtleDrawer.goto(0, 0)
        turtleDrawer.write("       You Beat Level " + str(self.level) + "\nYou killed " + str(self.score) + " crewmates!", False, "center", font=("Verdana", 25, "bold"))
        Game.screen.update() 
        print("Begin")
        time.sleep(2)
        print("end")
        Game.screen.clear()
        self.level += 1
        if self.level%2 != 0:
            self.lives += 1
        Start(self.level, self.lives, 0)

    #this draws the stars using shapes.py and randomizes their size and position
    def drawbackground(self):
        for i in range (50):
            star = shapes.Star(random.randint(5, 15), 'yellow', True)
            star.draw(random.randint(-380, 380), random.randint(-380, 380), 1, random.randint(0, 180))
        border = turtle.Turtle()
        border.hideturtle()
        border.pensize(10)
        border.color('dark gray')
        border.penup()
        border.goto(-400, -390)
        border.pendown()
        border.goto(-400, 390)
        border.goto(400, 390)
        border.goto(400, -390)
        border.goto(-400, -390)
        Game.screen.update()
    
    #this draws and updates the score board 
    def createScoreBoard(self):
        self.scoreBoard = turtle.Turtle()
        self.scoreBoard.hideturtle()
        self.scoreBoard.penup()
        self.scoreBoard.goto(0, -300)
        self.scoreBoard.write(str(self.score)+"/"+str(self.n), align='center',  font=("Verdana", 25, "bold"))
        self.highScoreBoard = turtle.Turtle()
        self.highScoreBoard.hideturtle()
        self.highScoreBoard.penup()
        self.highScoreBoard.goto(450, 0)
        self.highScoreBoard.write("High Score: " + self.bestplayer + " " +str(self.highscore), font=("Verdana", 15, "bold"))
        Game.screen.update()

    #this displays the keys for the controls
    def showControls(self):
        self.controls = turtle.Turtle()
        self.controls.hideturtle()
        self.controls.penup()
        self.controls.goto(-750, -50)
        self.controls.write("Lives = " + str(self.lives) + "\nMove = Arrow Keys\nEndGame = Q", font=("Verdana", 20, "bold"))
        self.controls.goto(0, -380)
        self.controls.color('red', 'yellow')
        self.controls.write(" A S T E R O I D S  L E V E L " + str(self.level), False, 'center', ("Verdana", 37, "bold"))
        self.controls.color('yellow')
        self.controls.goto(-750, 265)
        self.controls.write("Instructions:\nRun over all the crewmates\nwith the ship you just stole!\nLeave no survivors, but watch\nout for the asteroids!", False, 'left',  ("Verdana", 15, "bold"))
        Game.screen.update()

    def highScore(self):
        if self.level > self.highscore:
            self.highscore = self.level
            self.bestplayer = Game.screen.textinput("High Score!", 'Input 3 characters to save your score!')
            highscoreFile = open("highscore.txt", "w")
            highscoreFile.write(self.bestplayer + " " + str(self.highscore))
            highscoreFile.close()

class Start:

    screen = turtle.Screen()
    
    def __init__(self, level = 1, lives = 3, enemiesKilled = 0):
        self.level = level
        self.lives = lives

        self.enemiesKilled = enemiesKilled
        Start.screen.setup(width=1.0, height=1.0)
        Start.screen.tracer(False)
        self.drawdecoration()
        self.rocketturt = self.rocket()
        Start.screen.bgcolor('light blue')
        self.turtleDrawer = turtle.Turtle()
        self.turtleDrawer.hideturtle()
        if self.level > 1:
            self.turtleDrawer.write("A S T E R O I D S\n        Level " + str(self.level), False, 'center', ("Verdana", 40, "bold"))
        else:
            self.turtleDrawer.write("A S T E R O I D S", False, 'center', ("Verdana", 50, "bold"))
        self.turtleDrawer.penup()
        self.turtleDrawer.goto(0, -50)
        self.turtleDrawer.write("To play the game, press space!", False, "center", ("Verdana", 18, "bold"))
        self.turtleDrawer.hideturtle()
        
        Start.screen.update()

        Start.screen.onkey(self.startGame, "space")
        Start.screen.listen()
        Start.screen.mainloop()
 
    def startGame(self):
        Start.screen.clear()
        Game(self.level, self.lives, self.enemiesKilled)

    def drawdecoration(self):
        Start.screen.tracer(False)
        for i in range (50):
            star = shapes.Star(random.randint(5, 15), 'yellow', True)
            star.draw(random.randint(-380, 380), random.randint(-380, 380), 1, random.randint(0, 180))
        border = turtle.Turtle()
        border.hideturtle()
        border.pensize(10)
        border.color('dark gray')
        border.penup()
        border.goto(-400, -390)
        border.pendown()
        border.goto(-400, 390)
        border.goto(400, 390)
        border.goto(400, -390)
        border.goto(-400, -390)
    
    def rocket(self):
        turt = turtle.Turtle()
        filename = "imgs\Rocketship90.gif"
        Start.screen.register_shape(filename)
        turt.shape(filename)
        turt.goto(0, -10)
        return turt

if __name__ == '__main__':
    #this starts the game
    game = Start()

    # how to make the screen start fullscreen
    # glitch after level 4 and sometimes in between levels
    # the turtle in the middle of the screen