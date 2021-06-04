import turtle 
import random
import time
    
def setWorld():
    global gridState, existObj, visitedGrid, wumpusObj
    while True:
        gridState = []
        existObj = []
        visitedGrid = []
        wumpusObj = []
        w, p, g = 0, 0, 0
        for i in range(36):
            gridState.append([False, False, False, False])
            existObj.append([False, False, False, False])
            if not i in world:
                gridState[i][3] = True
                existObj[i][3] = True
            visitedGrid.append(False)
            wumpusObj.append(0)
        for i in world:
            if i == 19 or i == 25 or i == 26:
                continue
            wumpus = random.randint(1, 100) 
            pit = random.randint(1, 100)
            gold = random.randint(1, 100)
            if wumpus >= 1 and wumpus <= 15:
                wumpusObj[i] = turtle.Turtle()
                wumpusObj[i].hideturtle()
                wumpusObj[i].up()
                setPercepts(i, 0)
                w += 1
            elif pit >= 1 and pit <= 15:
                setPercepts(i, 1)
                p += 1
            elif gold >= 1 and gold <= 15:
                setPercepts(i, 2)
                g += 1
        if w != 0 and p != 0 and g != 0:
            break
 
def setPercepts(i, j):
    gridState[i][j] = True
    existObj[i][j] = True
    if j == 0 or j == 1:
            if (i - 6) in world:
                gridState[i - 6][j] = True
            if (i + 6) in world:
                gridState[i + 6][j] = True
            if (i + 1) in world:
                gridState[i + 1][j] = True
            if (i - 1) in world:
                gridState[i - 1][j] = True

def resetPercepts(i):
    existObj[i][0] = False
    if checkAdjGrid(i):
        gridState[i][0] = False
    if (i - 6) in world and checkAdjGrid(i - 6):
        gridState[i - 6][0] = False
    if (i + 6) in world and checkAdjGrid(i + 6):
        gridState[i + 6][0] = False
    if (i + 1) in world and checkAdjGrid(i + 1):
        gridState[i + 1][0] = False
    if (i - 1) in world and checkAdjGrid(i - 1):
        gridState[i - 1][0] = False

def checkAdjGrid(i):
    if existObj[i][0] == False and existObj[i - 6][0] == False and existObj[i + 6][0] == False and existObj[i + 1][0] == False and existObj[i - 1][0] == False:
        return 1
    else:
        return 0

def reset():
    global row, column, index, visitedFlag, agentChoice
    msg.clear()
    agent.hideturtle()
    agent.setheading(0)
    agent.shape("traveler0.gif")
    agent.goto(-150, -150)
    row, column, index = 4, 1, 25
    agent.showturtle()
    agent.speed(1)
    visitedFlag = []
    agentChoice = []
    for i in range(36):
        visitedFlag.append(0)
    visitedFlag[index] += 1
    visitedGrid[index] = True
    agentChoice.append([4, 1])
    printPercept()
        
def nextStep(x, y):
    if (x > 200 and x < 300) and (y < -200 and y > -300):
        nextRow, nextColumn, nextIndex = nextLoc(row, column, index)

        r, c, i = checkLine() 
        if i != -1 and arrowNum > 0: 
            shoot(r, c, i)
        elif visitedGrid[nextIndex] == False: 
            goforward(nextRow, nextColumn, nextIndex)
        elif existObj[nextIndex][0] == True or existObj[nextIndex][1] == True or existObj[nextIndex][3] == True: 
            turnleft()
        elif visitedFlag[nextIndex] >= 1 and unvisitedAdjGrid(): 
            turnleft()
        elif knowWumpus() and arrowNum > 0:
            turnleft()
        else:
            goforward(nextRow, nextColumn, nextIndex)
        
def nextLoc(r, c, i):
    nextRow, nextColumn, nextIndex = r, c, i
    
    if agent.heading() == 0:
        nextColumn += 1
    elif agent.heading() == 90:
        nextRow -= 1
    elif agent.heading() == 180:
        nextColumn -= 1
    elif agent.heading() == 270:
        nextRow += 1
    nextIndex = nextRow * 6 + nextColumn

    return nextRow, nextColumn, nextIndex
            
def unvisitedAdjGrid():
    left = index - 1
    right = index + 1
    up = index - 6
    down = index + 6
    checklist = [right, left, up, down]

    for i in checklist:
        if i in world and visitedFlag[i] == 0:
            if visitedGrid[i] == False or (visitedGrid[i] == True and (existObj[i][0] == False and existObj[i][1] == False)):
                return 1
    return 0

def knowWumpus():
    left = index - 1
    right = index + 1
    up = index - 6
    down = index + 6
    checklist = [right, left, up, down]

    for i in checklist:
        if i in world and visitedGrid[i] == True and existObj[i][0] == True:
            return 1
    return 0
        
def goforward(r, c, i):
    global row, column, index
    x, y = agent.position()
    nextX, nextY = x, y
    if agent.heading() == 0:
        nextX += 100
    elif agent.heading() == 90:
        nextY += 100
    elif agent.heading() == 180:
        nextX -= 100
    elif agent.heading() == 270:
        nextY -= 100

    if not bump(i):
        msg.clear()
        agent.goto(nextX, nextY)
        row, column, index = r, c, i
        printPercept()
        agentChoice.append([row, column])
        visitedGrid[index] = True
        visitedFlag[index] += 1
        i = column * 100 - 250
        j = row * (-100) + 250
        if existObj[index][0] == True:
            wumpusObj[index].goto(i, j)
            wumpusObj[index].shape("wumpus.gif")
            wumpusObj[index].showturtle()
        elif existObj[index][1] == True:
            obj.goto(i, j)
            obj.shape("pit.gif")
            obj.stamp()
        elif existObj[index][2] == True:
            obj.goto(i, j)
            obj.shape("gold.gif")
            obj.showturtle()

        if existObj[index][0] == True or existObj[index][1] == True:
            msg.write("You died!", False, "center", ("", 30, "bold"))
            time.sleep(2)
            reset()
        elif existObj[index][2] == True:
            grab()
    else:
        agent.goto(nextX, nextY)
        agent.goto(x, y)
        msg.write("BUMP!", False, "center", ("", 30, "bold"))

def bump(index):
    visitedGrid[index] = True
    if gridState[index][3] == False:
        return 0
    else:
        return 1

def turnleft():
    msg.clear()
    agent.left(90)
    setAgent()

def turnright():
    msg.clear()
    agent.right(90)
    setAgent()

def setAgent():
    head = agent.heading()
    if head == 0:
        agent.shape("traveler0.gif")
    elif head == 90:
        agent.shape("traveler90.gif")
    elif head == 180:
        agent.shape("traveler180.gif")
    elif head == 270:
        agent.shape("traveler270.gif")

def checkLine(): 
    nextRow, nextColumn, nextIndex = nextLoc(row, column, index)
    while nextIndex in world:
        if visitedGrid[nextIndex] == True and existObj[nextIndex][0] == True:
            return nextRow, nextColumn, nextIndex
        nextRow, nextColumn, nextIndex = nextLoc(nextRow, nextColumn, nextIndex)
    return -1, -1, -1

def shoot(r, c, i):
    global arrowNum
    arrowNum -= 1
    screen.bgpic("world" + str(arrowNum) + ".gif")
    p = c * 100 - 250
    q = r * (-100) + 250
    x, y = agent.position()
    if x < p:
        arrow.shape("arrow0.gif")
    elif y < q:
        arrow.shape("arrow90.gif")
    elif x > p:
        arrow.shape("arrow180.gif")
    elif y > q:
        arrow.shape("arrow270.gif")
    arrow.goto(x, y)
    arrow.showturtle()
    arrow.goto(p, q)
    arrow.hideturtle()
    wumpusObj[i].hideturtle()
    msg.write("SCREAM!", False, "center", ("", 30, "bold"))
    resetPercepts(i)
    printPercept()
    
def grab():
    msg.write("I got GOLD!", False, "center", ("", 30, "bold"))
    time.sleep(2)
    obj.hideturtle()
    pmsg.clear()
    back()

def back():
    global row, column, index
    choiceNum = len(agentChoice) - 2                                                                                                                                                                                                                                                       
    while choiceNum >= 0:
        r, c = agentChoice[choiceNum]
        while True:
            nextRow, nextColumn, nextIndex = nextLoc(row, column, index)
            if nextRow != r or nextColumn != c:
                turnright()
            else:
                break
        x = c * 100 - 250
        y = r * (-100) + 250
        agent.goto(x, y)
        row, column, index = nextRow, nextColumn, nextIndex
        choiceNum -= 1
        if row == 4 and column == 1:
            break
    agent.shape("traveler180.gif")
    agent.goto(-250, -150)
    climb()

def climb():
    agent.shape("climber.gif")
    agent.goto(-250, 500)
    screen.exitonclick()

def printPercept():
    r, c, i = row * (-1) + 5, column, index
    pmsg.clear()
    percept = "["+str(c)+","+str(r)+"]: "

    if gridState[i][0] == True and gridState[i][1] == True and gridState[i][2] == True:
        percept += "\n"
    if gridState[i][0] == True:
        percept += "Stench "
    if gridState[i][1] == True:
        percept += "Breeze "
    if gridState[i][2] == True:
        percept += "Glitter"
    if gridState[i][0] == False and gridState[i][1] == False and gridState[i][2] == False:
        percept += "None"
    pmsg.write(percept, False, "center", ("", 15, "bold"))


    
        
screen = turtle.Screen()
screen.title("Wumpus World")
screen.setup(600, 600)
screen.bgpic("world3.gif")
screen.addshape("traveler0.gif")
screen.addshape("traveler90.gif")
screen.addshape("traveler180.gif")
screen.addshape("traveler270.gif")
screen.addshape("climber.gif")
screen.addshape("wumpus.gif")
screen.addshape("pit.gif")
screen.addshape("gold.gif")
screen.addshape("arrow0.gif")
screen.addshape("arrow90.gif")
screen.addshape("arrow180.gif")
screen.addshape("arrow270.gif")

agent = turtle.Turtle()
agent.hideturtle()
agent.up()
agent.shape("traveler0.gif")

msg = turtle.Turtle()
msg.hideturtle()
msg.up()
msg.goto(0, -250)

pmsg = turtle.Turtle()
pmsg.hideturtle()
pmsg.up()
pmsg.goto(100, 215)

obj = turtle.Turtle()
obj.hideturtle()
obj.up()

arrow = turtle.Turtle()
arrow.hideturtle()
arrow.up()
arrow.speed(1)

world = [7, 8, 9, 10,
         13, 14, 15, 16,
         19, 20, 21, 22,
         25, 26, 27, 28]
gridState = []
existObj = []
wumpusObj = []
visitedGrid = []
visitedFlag = []
agentChoice = []
setWorld()

arrowNum = 3
row, column, index = 0, 0, 0
reset()

screen.onscreenclick(nextStep)
screen.listen()
    
turtle.mainloop()
