from cmu_graphics import *
import time
import math
import time

app.setMaxShapeCount(10000)
app.background = rgb(120, 15, 170)
app.width = 1000
app.height = 1000

# App Variables
app.clocks = Group()
app.hourHands = Group()
app.minuteHands = Group()

app.clockCols = 8  # X
app.clockRows = 3  # Y

app.clockRadius = app.width / 20
app.minuteLength = app.clockRadius - 3
app.hourLength = app.clockRadius * (3 / 5)

app.lastHour = 0
app.lastMinute = 0
app.steps = 0

app.gap = app.width / 125  # Gap between each clock

app.clockPosX = makeList(app.clockCols, app.clockRows)
app.clockPosY = makeList(app.clockCols, app.clockRows)

app.clockHours = makeList(app.clockCols, app.clockRows)  # Formula is 6 * (15 - minutes)  to get degrees  and (6 * pi * (15 - minutes))/180  for radians
app.clockMinutes = makeList(app.clockCols, app.clockRows)    # Formula is 30 * (3 - hours)    to get degrees  and (30 * pi * (3 - hours))/180    for radians

app.hoursAngle = makeList(app.clockCols, app.clockRows)
app.minutesAngle = makeList(app.clockCols, app.clockRows)

app.hoursEndX = makeList(app.clockCols, app.clockRows)
app.hoursEndY = makeList(app.clockCols, app.clockRows)
app.minutesEndX = makeList(app.clockCols, app.clockRows)
app.minutesEndY = makeList(app.clockCols, app.clockRows)

app.counter = 0
app.up = True

def initClocks():
    for x in range (app.clockCols):
        for y in range (app.clockRows):
            app.clockPosX[x][y] = app.width / (13 + 8/9) + app.clockRadius*(2*x + 1) + app.gap*x
            app.clockPosY[x][y] = app.height / 2 + app.clockRadius*(2*y - 1) + app.gap*(2*y - 1) - app.height / (17 + 9/23)
            #app.width / (11 + 4/11) + app.clockRadius*(2*y + 1) + app.gap*y

            app.clockHours[x][y] = 12
            app.clockMinutes[x][y] = 15

            app.hoursAngle[x][y] = (math.pi * app.clockHours[x][y] / 6) - (math.pi / 2)   # https://www.w3schools.com/graphics/canvas_clock_hands.asp is how I figured out the angles
            app.minutesAngle[x][y] = (math.pi * app.clockMinutes[x][y] / 30) - (math.pi / 2)

def printClocks():
    app.clocks.clear()
    app.hourHands.clear()
    app.minuteHands.clear()
    for x in range (app.clockCols):
        for y in range (app.clockRows):
            app.clocks.add(Circle(app.clockPosX[x][y], app.clockPosY[x][y], app.clockRadius, fill = rgb(200, 200, 200)))

            # Calculates where they would end just before printing so that each function can find the angle itself and then the place itself is handled here
            if(app.hoursAngle[x][y] == 1000 or app.minutesAngle[x][y] == 1000):
                pass
            else:
                app.hoursEndX[x][y] = app.clockPosX[x][y] + (app.hourLength * math.cos(app.hoursAngle[x][y]))
                app.hoursEndY[x][y] = app.clockPosY[x][y] + (app.hourLength * math.sin(app.hoursAngle[x][y]))
                app.minutesEndX[x][y] = app.clockPosX[x][y] + (app.minuteLength * math.cos(app.minutesAngle[x][y]))
                app.minutesEndY[x][y] = app.clockPosY[x][y] + (app.minuteLength * math.sin(app.minutesAngle[x][y]))

                app.hourHands.add(Line(app.clockPosX[x][y], app.clockPosY[x][y], app.hoursEndX[x][y], app.hoursEndY[x][y]))
                app.minuteHands.add(Line(app.clockPosX[x][y], app.clockPosY[x][y], app.minutesEndX[x][y], app.minutesEndY[x][y]))

def makeOne(position):  # Position will be either 0, 2, 4, or 6 to represent the 1s or 10s place of the hours or the 1s or 10s place of the minutes
    # Row 1
    app.hoursAngle[position][0] = 1000
    app.minutesAngle[position][0] = 1000

    app.hoursAngle[position + 1][0] = (math.pi * 5 / 6) # (math.pi * 8 / 6) - (math.pi / 2) simplified
    app.minutesAngle[position + 1][0] = math.pi / 2
    # Row 2
    app.hoursAngle[position][1] = 1000
    app.minutesAngle[position][1] = 1000

    app.hoursAngle[position + 1][1] = math.pi * 3 / 2
    app.minutesAngle[position + 1][1] = math.pi / 2

    # Row 3
    app.hoursAngle[position][2] = 1000
    app.minutesAngle[position][2] = 1000

    app.hoursAngle[position + 1][2] = math.pi * 3 / 2 
    app.minutesAngle[position + 1][2] = math.pi * 3 / 2

def makeTwo(position):  # Either 0, 2, 4, or 6  just to keep it standard (so it knows where each set of clocks is since 2 will take up 2 columns)
    # Row 1, flat top of the two
    app.hoursAngle[position][0] = 0
    app.minutesAngle[position][0] = 0

    app.hoursAngle[position + 1][0] = math.pi / 2
    app.minutesAngle[position + 1][0] = math.pi

    # Row 2
    app.hoursAngle[position][1] = math.pi / 2
    app.minutesAngle[position][1] = 0

    app.hoursAngle[position + 1][1] = math.pi * 3 / 2
    app.minutesAngle[position + 1][1] = math.pi

    # Row 3
    app.hoursAngle[position][2] = math.pi * 3 / 2
    app.minutesAngle[position][2] = 0

    app.hoursAngle[position + 1][2] = math.pi
    app.minutesAngle[position + 1][2] = math.pi

def makeThree(position):
    # Row 1
    app.hoursAngle[position][0] = 0
    app.minutesAngle[position][0] = 0

    app.hoursAngle[position + 1][0] = math.pi / 2
    app.minutesAngle[position + 1][0] = math.pi

    # Row 2
    app.hoursAngle[position][1] = 0
    app.minutesAngle[position][1] = 0

    app.hoursAngle[position + 1][1] = math.pi * 3 / 2
    app.minutesAngle[position + 1][1] = math.pi

    # Row 3
    app.hoursAngle[position][2] = 0
    app.minutesAngle[position][2] = 0

    app.hoursAngle[position + 1][2] = math.pi
    app.minutesAngle[position + 1][2] = math.pi * 3 / 2

def makeFour(position):
    # Row 1
    app.hoursAngle[position][0] = math.pi / 2
    app.minutesAngle[position][0] = math.pi / 2

    app.hoursAngle[position + 1][0] = math.pi / 2
    app.minutesAngle[position + 1][0] = math.pi / 2

    # Row 2
    app.hoursAngle[position][1] = math.pi * 3 / 2
    app.minutesAngle[position][1] = 0

    app.hoursAngle[position + 1][1] = math.pi
    app.minutesAngle[position + 1][1] = math.pi / 2

    # Row 3
    app.hoursAngle[position][2] = 1000
    app.minutesAngle[position][2] = 1000

    app.hoursAngle[position + 1][2] = math.pi * 3 / 2
    app.minutesAngle[position + 1][2] = math.pi * 3 / 2

def makeFive(position):
    # Row 1
    app.hoursAngle[position][0] = math.pi / 2
    app.minutesAngle[position][0] = 0

    app.hoursAngle[position + 1][0] = math.pi
    app.minutesAngle[position + 1][0] = math.pi

    # Row 2
    app.hoursAngle[position][1] = math.pi * 3 / 2
    app.minutesAngle[position][1] = 0

    app.hoursAngle[position + 1][1] = math.pi / 2
    app.minutesAngle[position + 1][1] = math.pi

    # Row 3
    app.hoursAngle[position][2] = 0
    app.minutesAngle[position][2] = 0

    app.hoursAngle[position + 1][2] = math.pi * 3 / 2
    app.minutesAngle[position + 1][2] = math.pi

def makeSix(position):
    # Row 1
    app.hoursAngle[position][0] = math.pi / 2
    app.minutesAngle[position][0] = 0

    app.hoursAngle[position + 1][0] = math.pi
    app.minutesAngle[position + 1][0] = math.pi

    # Row 2
    app.hoursAngle[position][1] = math.pi * 3 / 2
    app.minutesAngle[position][1] = math.pi / 2 

    app.hoursAngle[position + 1][1] = math.pi / 2
    app.minutesAngle[position + 1][1] = math.pi

    # Row 3
    app.hoursAngle[position][2] = math.pi * 3 / 2
    app.minutesAngle[position][2] = 0

    app.hoursAngle[position + 1][2] = math.pi * 3 / 2
    app.minutesAngle[position + 1][2] = math.pi

def makeSeven(position):
    # Row 1
    app.hoursAngle[position][0] = 0
    app.minutesAngle[position][0] = 0

    app.hoursAngle[position + 1][0] = math.pi
    app.minutesAngle[position + 1][0] = math.pi / 2
    # Row 2
    app.hoursAngle[position][1] = 1000
    app.minutesAngle[position][1] = 1000

    app.hoursAngle[position + 1][1] = math.pi * 3 / 2
    app.minutesAngle[position + 1][1] = math.pi / 2

    # Row 3
    app.hoursAngle[position][2] = 1000
    app.minutesAngle[position][2] = 1000

    app.hoursAngle[position + 1][2] = math.pi * 3 / 2 
    app.minutesAngle[position + 1][2] = math.pi * 3 / 2

def makeEight(position):
    # Row 1
    app.hoursAngle[position][0] = math.pi / 2
    app.minutesAngle[position][0] = 0

    app.hoursAngle[position + 1][0] = math.pi / 2
    app.minutesAngle[position + 1][0] = math.pi

    # Row 2
    app.hoursAngle[position][1] = math.pi * 3 / 2
    app.minutesAngle[position][1] = 0

    app.hoursAngle[position + 1][1] = math.pi / 2
    app.minutesAngle[position + 1][1] = math.pi

    # Row 3
    app.hoursAngle[position][2] = math.pi * 3 / 2
    app.minutesAngle[position][2] = 0

    app.hoursAngle[position + 1][2] = math.pi * 3 / 2
    app.minutesAngle[position + 1][2] = math.pi

def makeNine(position):
    # Row 1
    app.hoursAngle[position][0] = math.pi / 2
    app.minutesAngle[position][0] = 0

    app.hoursAngle[position + 1][0] = math.pi / 2
    app.minutesAngle[position + 1][0] = math.pi

    # Row 2
    app.hoursAngle[position][1] = math.pi * 3 / 2
    app.minutesAngle[position][1] = 0

    app.hoursAngle[position + 1][1] = math.pi * 3 / 2
    app.minutesAngle[position + 1][1] = math.pi / 2

    # Row 3
    app.hoursAngle[position][2] = 0
    app.minutesAngle[position][2] = 0

    app.hoursAngle[position + 1][2] = math.pi * 3 / 2
    app.minutesAngle[position + 1][2] = math.pi

def makeZero(position):
    # Row 1
    app.hoursAngle[position][0] = math.pi / 2
    app.minutesAngle[position][0] = 0

    app.hoursAngle[position + 1][0] = math.pi / 2
    app.minutesAngle[position + 1][0] = math.pi

    # Row 2
    app.hoursAngle[position][1] = math.pi * 3 / 2
    app.minutesAngle[position][1] = math.pi / 2

    app.hoursAngle[position + 1][1] = math.pi * 3 / 2
    app.minutesAngle[position + 1][1] = math.pi / 2

    # Row 3
    app.hoursAngle[position][2] = math.pi * 3 / 2
    app.minutesAngle[position][2] = 0

    app.hoursAngle[position + 1][2] = math.pi * 3 / 2
    app.minutesAngle[position + 1][2] = math.pi

def makeNumbers(hours, minutes):
    if(app.lastHour == hours - 1 or app.lastMinute == minutes - 1 or 45 > app.steps > 0):
        spin(app.counter)
        app.steps += 1
    else:
        app.steps = 0
        if(hours == 1):
            makeZero(0) 
            makeOne(2)
        elif(hours == 2):
            makeZero(0) 
            makeTwo(2)
        elif(hours == 3):
            makeZero(0) 
            makeThree(2)
        elif(hours == 4):
            makeZero(0) 
            makeFour(2)
        elif(hours == 5):
            makeZero(0) 
            makeThree(2)
        elif(hours == 6):
            makeZero(0) 
            makeSix(2)
        elif(hours == 7):
            makeZero(0) 
            makeSeven(2)
        elif(hours == 8):
            makeZero(0) 
            makeEight(2)
        elif(hours == 9):
            makeZero(0) 
            makeNine(2)
        elif(hours == 10):
            makeOne(0)
            makeZero(2)
        elif(hours == 11):
            makeOne(0)
            makeOne(2)
        elif(hours == 0 or hours == 12):
            makeOne(0)
            makeTwo(2)

        if(int(minutes / 10) == 0):
            makeZero(4)
        elif(int(minutes / 10) == 1):
            makeOne(4)
        elif(int(minutes / 10) == 2):
            makeTwo(4)
        elif(int(minutes / 10) == 3):
            makeThree(4)
        elif(int(minutes / 10) == 4):
            makeFour(4)
        elif(int(minutes / 10) == 5):
            makeFive(4)
        
        if(minutes % 10 == 0):
            makeZero(6)
        elif(minutes % 10 == 1):
            makeOne(6)
        elif(minutes % 10 == 2):
            makeTwo(6)
        elif(minutes % 10 == 3):
            makeThree(6)
        elif(minutes % 10 == 4):
            makeFour(6)
        elif(minutes % 10 == 5):
            makeFive(6)
        elif(minutes % 10 == 6):
            makeSix(6)
        elif(minutes % 10 == 7):
            makeSeven(6)
        elif(minutes % 10 == 8):
            makeEight(6)
        elif(minutes % 10 == 9):
            makeNine(6)
    
    app.lastHour = hours
    app.lastMinute = minutes

def pivotTo(coordX, coordY):
    # Angle = math.atan(y / x)    atan = arctan

    app.clocks.add(Circle(coordX, coordY, 25))
    for x in range (app.clockCols):
        for y in range (app.clockRows):
            if(coordX - app.clockPosX[x][y] == 0 or coordY - app.clockPosY[x][y] == 0):
                app.hoursAngle[x][y] = math.atan((coordY - app.clockPosY[x][y] + 1) / (coordX - app.clockPosX[x][y] + 1)) 
                app.minutesAngle[x][y] = math.atan((coordY - app.clockPosY[x][y] + 1) / (coordX - app.clockPosX[x][y] + 1)) 

            elif(coordX - app.clockPosX[x][y] < 0):
                app.hoursAngle[x][y] = math.atan((coordY - app.clockPosY[x][y]) / (coordX - app.clockPosX[x][y])) + math.pi
                app.minutesAngle[x][y] = math.atan((coordY - app.clockPosY[x][y]) / (coordX - app.clockPosX[x][y])) + math.pi
            elif(coordX - app.clockPosX[x][y] >= 0):
                app.hoursAngle[x][y] = math.atan((coordY - app.clockPosY[x][y]) / (coordX - app.clockPosX[x][y])) 
                app.minutesAngle[x][y] = math.atan((coordY - app.clockPosY[x][y]) / (coordX - app.clockPosX[x][y])) 

def parabolicCurvePivot(i):
    if(i >= 500):
        app.up = False
    elif(i <= 0):
        app.up = True
    
    if(i < 250):
        pivotTo(i, 200 + i)
    elif(i >= 250):
        pivotTo(i, 449 + (250 - i))
    
    if(app.up == True):
        app.counter += 3
        i += 3
    elif(app.up == False):
        app.counter -= 3
        i -= 3

def realTime():
    realHour = time.localtime().tm_hour % 12
    realMinute = time.localtime().tm_min
    makeNumbers(realHour, realMinute)

def rotateToTime(rotateStep): 
    # Needs some work to get it to only change when necessary
    rotateStep = rotateStep % 60
    oldAngleHours = makeList(app.clockCols, app.clockRows)
    oldAngleMins = makeList(app.clockCols, app.clockRows)

    hoursChange = makeList(app.clockCols, app.clockRows)
    minutesChange = makeList(app.clockCols, app.clockRows)

    for x in range (app.clockCols):
        for y in range (app.clockRows):
            oldAngleHours[x][y] = app.hoursAngle[x][y]
            oldAngleMins[x][y] = app.minutesAngle[x][y]
    realTime()
    for x in range (app.clockCols):
        for y in range (app.clockRows):
            hoursChange[x][y] = (oldAngleHours[x][y] - app.hoursAngle[x][y]) / 60
            minutesChange[x][y] = (oldAngleMins[x][y] - app.minutesAngle[x][y]) / 60
            app.hoursAngle[x][y] = oldAngleHours[x][y] + hoursChange[x][y] * rotateStep
            app.minutesAngle[x][y] = oldAngleHours[x][y] + minutesChange[x][y] * rotateStep
    #printClocks()

def spin(rate):
    for x in range (app.clockCols):
        for y in range (app.clockRows):
            app.hoursAngle[x][y] = rate
            app.minutesAngle[x][y] = rate + math.pi
            # Adding math.pi to the minutes hand makes it a single line.
            # Making minutes have an angle of -rate makes the two converge at 3 and 9 o'clock, which is nice to look at

def onStep():
    # Options for what to do with it:
    # 1. Have it track some point with a certain trajectory
    # 2. Have it display the real time
    # 3. Have it display a time you input
    # 4. Have it move in a circle
    
    realTime()
    app.counter -= 6
    printClocks()

initClocks()


#printClocks()

cmu_graphics.run()


# Between time, make it spin

# Implement a way to change the time within a run, using the text box thingy (done)
# Have it track real time (done)
# Have it show movements
# Have it all pivot to one imaginary point (ex. (500, 500), just up somewhere) (done)