from tkinter import Tk, Canvas
import csv
import math
import sys


CenterlinePoints = []
OutsidePoints = []
InsidePoints = []
Min_X = math.inf
Max_X = -math.inf
Min_Y = math.inf
Max_Y = -math.inf
X_Offset = 0.0
Y_Offset = 0.0
Scale = 1.0
WindowWidth = 1920
WindowHeight = 1080
TrackWidth = 0.64
m_Window = Tk()
m_Canvas = Canvas()


def DrawLine(pt1_x, pt1_y, pt2_x, pt2_y, thickness, colour):
    global X_Offset, Y_Offset, Scale, m_Canvas

    m_Canvas.create_line(
        (pt1_x - X_Offset) * Scale,
        (pt1_y + Y_Offset) * Scale * -1,
        (pt2_x - X_Offset) * Scale,
        (pt2_y + Y_Offset) * Scale * -1,
        fill=colour,
        width=thickness
    )


def DrawDashedLine(pt1_x, pt1_y, pt2_x, pt2_y, thickness, colour, dashSize):
    global X_Offset, Y_Offset, Scale, m_Canvas

    m_Canvas.create_line(
        (pt1_x - X_Offset) * Scale,
        (pt1_y + Y_Offset) * Scale * -1,
        (pt2_x - X_Offset) * Scale,
        (pt2_y + Y_Offset) * Scale * -1,
        fill=colour,
        width=thickness,
        dash=dashSize
    )


def SizeTrack():
    global Min_X, Max_X, Max_Y, Min_Y, WindowWidth, WindowHeight, X_Offset, Y_Offset, Scale, TrackWidth
    for point in InsidePoints:
        # Find Minumum X Value
        if(point[0] < Min_X):
            Min_X = point[0]
        # Find Maxumum X Value
        if(point[0] > Max_X):
            Max_X = point[0]
        # Find Minumum Y Value
        if(point[1] < Min_Y):
            Min_Y = point[1]
        # Find Maxumum X Value
        if(point[1] > Max_Y):
            Max_Y = point[1]
    for point in OutsidePoints:
        # Find Minumum X Value
        if(point[0] < Min_X):
            Min_X = point[0]
        # Find Maxumum X Value
        if(point[0] > Max_X):
            Max_X = point[0]
        # Find Minumum Y Value
        if(point[1] < Min_Y):
            Min_Y = point[1]
        # Find Maxumum X Value
        if(point[1] > Max_Y):
            Max_Y = point[1]
    Min_X = Min_X - TrackWidth * 1.5
    Max_X = Max_X + TrackWidth * 1.5
    Min_Y = Min_Y - TrackWidth * 1.5
    Max_Y = Max_Y + TrackWidth * 1.5
    # Find Height
    width = Max_X - Min_X
    # Find Width
    height = Max_Y - Min_Y
    # Set Scale
    x_scale = WindowWidth / width
    y_scale = WindowHeight / height
    if(x_scale < y_scale):
        Scale = x_scale
    else:
        Scale = y_scale
    # Set Offset
    X_Offset = Min_X
    Y_Offset = Min_Y


def UnitVector(pt1_x, pt1_y, pt2_x, pt2_y):
    dx = pt2_x - pt1_x
    dy = pt2_y - pt1_y
    length = math.sqrt(dx * dx + dy * dy)
    x = dx / length
    y = dy / length
    #print("Unit Vector: (%s, %s)" % (x,y))
    return [x, y]


def PerpendicularUnitVector(inputVector):
    x = inputVector[0] * math.cos(math.pi / 2) - inputVector[1] * math.sin(math.pi / 2)
    y = inputVector[0] * math.sin(math.pi / 2) + inputVector[1] * math.cos(math.pi / 2)
    #print("Perpendicular Vector: (%s, %s)" % (x,y))
    return [x, y]


def OffsetVector(pt1, pt2):
    return PerpendicularUnitVector(UnitVector(pt1[0], pt1[1], pt2[0], pt2[1]))


def Offset():
    global TrackWidth
    beforeZero = len(CenterlinePoints) - 1
    if(CenterlinePoints[beforeZero] == CenterlinePoints[0]):
        beforeZero -= 1
    
    for i, pt in enumerate(CenterlinePoints):
        if(i == 0):
            pt1 = CenterlinePoints[beforeZero]
            pt2 = CenterlinePoints[i + 1]
        elif(i == len(CenterlinePoints) - 1):
            pt1 = CenterlinePoints[i - 1]
            pt2 = CenterlinePoints[1]
        else:
            pt1 = [ CenterlinePoints[i - 1][0], CenterlinePoints[i - 1][1] ]
            pt2 = CenterlinePoints[i + 1]
        unitVector = UnitVector(pt1[0], pt1[1], pt2[0], pt2[1])
        offsetVector = PerpendicularUnitVector(unitVector)
        offsetVector = OffsetVector(pt1, pt2)
        insideX = CenterlinePoints[i][0] + offsetVector[0] * TrackWidth * -0.5
        insideY = CenterlinePoints[i][1] + offsetVector[1] * TrackWidth * -0.5
        InsidePoints.append([insideX, insideY])
        outsideX = CenterlinePoints[i][0] + offsetVector[0] * TrackWidth * 0.5
        outsideY = CenterlinePoints[i][1] + offsetVector[1] * TrackWidth * 0.5
        OutsidePoints.append([outsideX, outsideY])


def main():
    global CenterlinePoints, InsidePoints, OutsidePoints
    global m_Window, m_Canvas, WindowWidth, WindowHeight

    m_Window.title("DeepRacer - Track Simulator")
    m_Canvas = Canvas(m_Window, width=WindowWidth, height=WindowHeight, background='white')
    m_Canvas.grid(row=0, column=0)
    i = 0
    while(i < len(CenterlinePoints) - 1):
        DrawDashedLine(CenterlinePoints[i][0],CenterlinePoints[i][1], CenterlinePoints[i+1][0], CenterlinePoints[i+1][1], 3, 'yellow', (255, 5))
        DrawLine(InsidePoints[i][0],InsidePoints[i][1], InsidePoints[i+1][0], InsidePoints[i+1][1], 3, 'black')
        DrawLine(OutsidePoints[i][0],OutsidePoints[i][1], OutsidePoints[i+1][0], OutsidePoints[i+1][1], 3, 'black')
        i += 1
    DrawDashedLine(OutsidePoints[0][0],OutsidePoints[0][1], InsidePoints[0][0], InsidePoints[0][1], 5, 'red', (255, 255))
    m_Window.mainloop()


#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
#TrackFile = "../tracks/China_track.csv"
#TrackFile = "../tracks/Mexico_track.csv"
TrackFile = ""

if(len(sys.argv) >= 2):
    if(str(sys.argv[1]).endswith('.csv')):
        TrackFile = str(sys.argv[1])

if(len(sys.argv) == 3):
    if(type(sys.argv[2]) == str):
        WindowWidth = int(sys.argv[2])
        WindowHeight = int(sys.argv[2])

if(len(sys.argv) == 4):
    if(type(sys.argv[2]) == str and type(sys.argv[3]) == str):
        WindowWidth = int(sys.argv[2])
        WindowHeight = int(sys.argv[3])

with open(TrackFile) as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        CenterlinePoints.append([float(line[0]), float(line[1])])

Offset()
SizeTrack()
main()