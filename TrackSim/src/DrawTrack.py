from tkinter import Tk, Canvas
import csv
import math
import sys


CenterlinePoints = []
OutsidePoints = []
InsidePoints = []
BaseChassisPoints = [
     0.040, -0.025,
     0.040,  0.125,
     0.025,  0.138,
     0.025,  0.188,
    -0.025,  0.188,
    -0.025,  0.138,
    -0.040,  0.125,
    -0.040, -0.025,
     0.040, -0.025
]
RightWheelPoints = [
     0.000,  0.000,
     0.000, -0.025,
     0.025, -0.025,
     0.025,  0.025,
     0.000,  0.025,
     0.000,  0.000
]
LeftWheelPoints = [
     0.000,  0.000,
     0.000, -0.025,
    -0.025, -0.025,
    -0.025,  0.025,
     0.000,  0.025,
     0.000,  0.000
]
RightFrontWheel = [ 0.050, 0.163]
LeftFrontWheel  = [-0.050, 0.163]
RightRearWheel  = [ 0.050, 0.000]
LeftRearWheel   = [-0.050, 0.000]

BaseRightFrontWheelPoints = []
BaseLeftFrontWheelPoints = []
BaseRightRearWheelPoints = []
BaseLeftRearWheelPoints = []

MoveableRightFrontWheelPoints = []
MoveableLeftFrontWheelPoints = []
MoveableRightRearWheelPoints = []
MoveableLeftRearWheelPoints = []

MoveableChassisPoints = []
m_Chassis = ""
m_RightFrontWheel = ""
m_LeftFrontWheel = ""
m_RightRearWheel = ""
m_LeftRearWheel = ""

PositionIndex = 0
Position = []
Heading = 0.0
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


def SetWheelPoints():
    global BaseRightFrontWheelPoints, BaseLeftFrontWheelPoints, BaseRightRearWheelPoints, BaseLeftRearWheelPoints
    # Right Front
    BaseRightFrontWheelPoints.append(RightWheelPoints[ 0] + RightFrontWheel[0])
    BaseRightFrontWheelPoints.append(RightWheelPoints[ 1] + RightFrontWheel[1])
    BaseRightFrontWheelPoints.append(RightWheelPoints[ 2] + RightFrontWheel[0])
    BaseRightFrontWheelPoints.append(RightWheelPoints[ 3] + RightFrontWheel[1])
    BaseRightFrontWheelPoints.append(RightWheelPoints[ 4] + RightFrontWheel[0])
    BaseRightFrontWheelPoints.append(RightWheelPoints[ 5] + RightFrontWheel[1])
    BaseRightFrontWheelPoints.append(RightWheelPoints[ 6] + RightFrontWheel[0])
    BaseRightFrontWheelPoints.append(RightWheelPoints[ 7] + RightFrontWheel[1])
    BaseRightFrontWheelPoints.append(RightWheelPoints[ 8] + RightFrontWheel[0])
    BaseRightFrontWheelPoints.append(RightWheelPoints[ 9] + RightFrontWheel[1])
    BaseRightFrontWheelPoints.append(RightWheelPoints[10] + RightFrontWheel[0])
    BaseRightFrontWheelPoints.append(RightWheelPoints[11] + RightFrontWheel[1])
    # Right Rear
    BaseRightRearWheelPoints.append(RightWheelPoints[ 0] + RightRearWheel[0])
    BaseRightRearWheelPoints.append(RightWheelPoints[ 1] + RightRearWheel[1])
    BaseRightRearWheelPoints.append(RightWheelPoints[ 2] + RightRearWheel[0])
    BaseRightRearWheelPoints.append(RightWheelPoints[ 3] + RightRearWheel[1])
    BaseRightRearWheelPoints.append(RightWheelPoints[ 4] + RightRearWheel[0])
    BaseRightRearWheelPoints.append(RightWheelPoints[ 5] + RightRearWheel[1])
    BaseRightRearWheelPoints.append(RightWheelPoints[ 6] + RightRearWheel[0])
    BaseRightRearWheelPoints.append(RightWheelPoints[ 7] + RightRearWheel[1])
    BaseRightRearWheelPoints.append(RightWheelPoints[ 8] + RightRearWheel[0])
    BaseRightRearWheelPoints.append(RightWheelPoints[ 9] + RightRearWheel[1])
    BaseRightRearWheelPoints.append(RightWheelPoints[10] + RightRearWheel[0])
    BaseRightRearWheelPoints.append(RightWheelPoints[11] + RightRearWheel[1])
    # Left Front
    BaseLeftFrontWheelPoints.append(LeftWheelPoints[ 0] + LeftFrontWheel[0])
    BaseLeftFrontWheelPoints.append(LeftWheelPoints[ 1] + LeftFrontWheel[1])
    BaseLeftFrontWheelPoints.append(LeftWheelPoints[ 2] + LeftFrontWheel[0])
    BaseLeftFrontWheelPoints.append(LeftWheelPoints[ 3] + LeftFrontWheel[1])
    BaseLeftFrontWheelPoints.append(LeftWheelPoints[ 4] + LeftFrontWheel[0])
    BaseLeftFrontWheelPoints.append(LeftWheelPoints[ 5] + LeftFrontWheel[1])
    BaseLeftFrontWheelPoints.append(LeftWheelPoints[ 6] + LeftFrontWheel[0])
    BaseLeftFrontWheelPoints.append(LeftWheelPoints[ 7] + LeftFrontWheel[1])
    BaseLeftFrontWheelPoints.append(LeftWheelPoints[ 8] + LeftFrontWheel[0])
    BaseLeftFrontWheelPoints.append(LeftWheelPoints[ 9] + LeftFrontWheel[1])
    BaseLeftFrontWheelPoints.append(LeftWheelPoints[10] + LeftFrontWheel[0])
    BaseLeftFrontWheelPoints.append(LeftWheelPoints[11] + LeftFrontWheel[1])
    # Left Rear
    BaseLeftRearWheelPoints.append(LeftWheelPoints[ 0] + LeftRearWheel[0])
    BaseLeftRearWheelPoints.append(LeftWheelPoints[ 1] + LeftRearWheel[1])
    BaseLeftRearWheelPoints.append(LeftWheelPoints[ 2] + LeftRearWheel[0])
    BaseLeftRearWheelPoints.append(LeftWheelPoints[ 3] + LeftRearWheel[1])
    BaseLeftRearWheelPoints.append(LeftWheelPoints[ 4] + LeftRearWheel[0])
    BaseLeftRearWheelPoints.append(LeftWheelPoints[ 5] + LeftRearWheel[1])
    BaseLeftRearWheelPoints.append(LeftWheelPoints[ 6] + LeftRearWheel[0])
    BaseLeftRearWheelPoints.append(LeftWheelPoints[ 7] + LeftRearWheel[1])
    BaseLeftRearWheelPoints.append(LeftWheelPoints[ 8] + LeftRearWheel[0])
    BaseLeftRearWheelPoints.append(LeftWheelPoints[ 9] + LeftRearWheel[1])
    BaseLeftRearWheelPoints.append(LeftWheelPoints[10] + LeftRearWheel[0])
    BaseLeftRearWheelPoints.append(LeftWheelPoints[11] + LeftRearWheel[1])


def DrawChassis():
    global MoveableChassisPoints, Heading
    # Draw the Race Car's Chassis
    # Set the Chassis's Heading
    _Temp = BaseChassisPoints.copy()

    _Temp[ 0] = BaseChassisPoints[ 0] * math.cos(Heading) - BaseChassisPoints[ 1] * math.sin(Heading)
    _Temp[ 2] = BaseChassisPoints[ 2] * math.cos(Heading) - BaseChassisPoints[ 3] * math.sin(Heading)
    _Temp[ 4] = BaseChassisPoints[ 4] * math.cos(Heading) - BaseChassisPoints[ 5] * math.sin(Heading)
    _Temp[ 6] = BaseChassisPoints[ 6] * math.cos(Heading) - BaseChassisPoints[ 7] * math.sin(Heading)
    _Temp[ 8] = BaseChassisPoints[ 8] * math.cos(Heading) - BaseChassisPoints[ 9] * math.sin(Heading)
    _Temp[10] = BaseChassisPoints[10] * math.cos(Heading) - BaseChassisPoints[11] * math.sin(Heading)
    _Temp[12] = BaseChassisPoints[12] * math.cos(Heading) - BaseChassisPoints[13] * math.sin(Heading)
    _Temp[14] = BaseChassisPoints[14] * math.cos(Heading) - BaseChassisPoints[15] * math.sin(Heading)
    _Temp[16] = BaseChassisPoints[16] * math.cos(Heading) - BaseChassisPoints[17] * math.sin(Heading)
    
    _Temp[ 1] = BaseChassisPoints[ 0] * math.sin(Heading) + BaseChassisPoints[ 1] * math.cos(Heading)
    _Temp[ 3] = BaseChassisPoints[ 2] * math.sin(Heading) + BaseChassisPoints[ 3] * math.cos(Heading)
    _Temp[ 5] = BaseChassisPoints[ 4] * math.sin(Heading) + BaseChassisPoints[ 5] * math.cos(Heading)
    _Temp[ 7] = BaseChassisPoints[ 6] * math.sin(Heading) + BaseChassisPoints[ 7] * math.cos(Heading)
    _Temp[ 9] = BaseChassisPoints[ 8] * math.sin(Heading) + BaseChassisPoints[ 9] * math.cos(Heading)
    _Temp[11] = BaseChassisPoints[10] * math.sin(Heading) + BaseChassisPoints[11] * math.cos(Heading)
    _Temp[13] = BaseChassisPoints[12] * math.sin(Heading) + BaseChassisPoints[13] * math.cos(Heading)
    _Temp[15] = BaseChassisPoints[14] * math.sin(Heading) + BaseChassisPoints[15] * math.cos(Heading)
    _Temp[17] = BaseChassisPoints[16] * math.sin(Heading) + BaseChassisPoints[17] * math.cos(Heading)

    MoveableChassisPoints = _Temp.copy()

    # Set the Chassis's Position
    MoveableChassisPoints[ 0] = (MoveableChassisPoints[ 0] + Position[0] - X_Offset) * Scale
    MoveableChassisPoints[ 2] = (MoveableChassisPoints[ 2] + Position[0] - X_Offset) * Scale
    MoveableChassisPoints[ 4] = (MoveableChassisPoints[ 4] + Position[0] - X_Offset) * Scale
    MoveableChassisPoints[ 6] = (MoveableChassisPoints[ 6] + Position[0] - X_Offset) * Scale
    MoveableChassisPoints[ 8] = (MoveableChassisPoints[ 8] + Position[0] - X_Offset) * Scale
    MoveableChassisPoints[10] = (MoveableChassisPoints[10] + Position[0] - X_Offset) * Scale
    MoveableChassisPoints[12] = (MoveableChassisPoints[12] + Position[0] - X_Offset) * Scale
    MoveableChassisPoints[14] = (MoveableChassisPoints[14] + Position[0] - X_Offset) * Scale
    MoveableChassisPoints[16] = (MoveableChassisPoints[16] + Position[0] - X_Offset) * Scale

    MoveableChassisPoints[ 1] = (MoveableChassisPoints[ 1] + Position[1] + Y_Offset) * Scale * -1
    MoveableChassisPoints[ 3] = (MoveableChassisPoints[ 3] + Position[1] + Y_Offset) * Scale * -1
    MoveableChassisPoints[ 5] = (MoveableChassisPoints[ 5] + Position[1] + Y_Offset) * Scale * -1
    MoveableChassisPoints[ 7] = (MoveableChassisPoints[ 7] + Position[1] + Y_Offset) * Scale * -1
    MoveableChassisPoints[ 9] = (MoveableChassisPoints[ 9] + Position[1] + Y_Offset) * Scale * -1
    MoveableChassisPoints[11] = (MoveableChassisPoints[11] + Position[1] + Y_Offset) * Scale * -1
    MoveableChassisPoints[13] = (MoveableChassisPoints[13] + Position[1] + Y_Offset) * Scale * -1
    MoveableChassisPoints[15] = (MoveableChassisPoints[15] + Position[1] + Y_Offset) * Scale * -1
    MoveableChassisPoints[17] = (MoveableChassisPoints[17] + Position[1] + Y_Offset) * Scale * -1


def DrawRightFrontWheel():
    global MoveableRightFrontWheelPoints
    # Draw the Race Car's Right Front Wheel
    # Set the Right Front Wheel's Chassis Heading
    _Temp = BaseRightFrontWheelPoints.copy()

    _Temp[ 0] = BaseRightFrontWheelPoints[ 0] * math.cos(Heading) - BaseRightFrontWheelPoints[ 1] * math.sin(Heading)
    _Temp[ 2] = BaseRightFrontWheelPoints[ 2] * math.cos(Heading) - BaseRightFrontWheelPoints[ 3] * math.sin(Heading)
    _Temp[ 4] = BaseRightFrontWheelPoints[ 4] * math.cos(Heading) - BaseRightFrontWheelPoints[ 5] * math.sin(Heading)
    _Temp[ 6] = BaseRightFrontWheelPoints[ 6] * math.cos(Heading) - BaseRightFrontWheelPoints[ 7] * math.sin(Heading)
    _Temp[ 8] = BaseRightFrontWheelPoints[ 8] * math.cos(Heading) - BaseRightFrontWheelPoints[ 9] * math.sin(Heading)
    _Temp[10] = BaseRightFrontWheelPoints[10] * math.cos(Heading) - BaseRightFrontWheelPoints[11] * math.sin(Heading)
    
    _Temp[ 1] = BaseRightFrontWheelPoints[ 0] * math.sin(Heading) + BaseRightFrontWheelPoints[ 1] * math.cos(Heading)
    _Temp[ 3] = BaseRightFrontWheelPoints[ 2] * math.sin(Heading) + BaseRightFrontWheelPoints[ 3] * math.cos(Heading)
    _Temp[ 5] = BaseRightFrontWheelPoints[ 4] * math.sin(Heading) + BaseRightFrontWheelPoints[ 5] * math.cos(Heading)
    _Temp[ 7] = BaseRightFrontWheelPoints[ 6] * math.sin(Heading) + BaseRightFrontWheelPoints[ 7] * math.cos(Heading)
    _Temp[ 9] = BaseRightFrontWheelPoints[ 8] * math.sin(Heading) + BaseRightFrontWheelPoints[ 9] * math.cos(Heading)
    _Temp[11] = BaseRightFrontWheelPoints[10] * math.sin(Heading) + BaseRightFrontWheelPoints[11] * math.cos(Heading)

    MoveableRightFrontWheelPoints = _Temp.copy()

    # Set the Right Front Wheel's Position
    MoveableRightFrontWheelPoints[ 0] = (MoveableRightFrontWheelPoints[ 0] + Position[0] - X_Offset) * Scale
    MoveableRightFrontWheelPoints[ 2] = (MoveableRightFrontWheelPoints[ 2] + Position[0] - X_Offset) * Scale
    MoveableRightFrontWheelPoints[ 4] = (MoveableRightFrontWheelPoints[ 4] + Position[0] - X_Offset) * Scale
    MoveableRightFrontWheelPoints[ 6] = (MoveableRightFrontWheelPoints[ 6] + Position[0] - X_Offset) * Scale
    MoveableRightFrontWheelPoints[ 8] = (MoveableRightFrontWheelPoints[ 8] + Position[0] - X_Offset) * Scale
    MoveableRightFrontWheelPoints[10] = (MoveableRightFrontWheelPoints[10] + Position[0] - X_Offset) * Scale

    MoveableRightFrontWheelPoints[ 1] = (MoveableRightFrontWheelPoints[ 1] + Position[1] + Y_Offset) * Scale * -1
    MoveableRightFrontWheelPoints[ 3] = (MoveableRightFrontWheelPoints[ 3] + Position[1] + Y_Offset) * Scale * -1
    MoveableRightFrontWheelPoints[ 5] = (MoveableRightFrontWheelPoints[ 5] + Position[1] + Y_Offset) * Scale * -1
    MoveableRightFrontWheelPoints[ 7] = (MoveableRightFrontWheelPoints[ 7] + Position[1] + Y_Offset) * Scale * -1
    MoveableRightFrontWheelPoints[ 9] = (MoveableRightFrontWheelPoints[ 9] + Position[1] + Y_Offset) * Scale * -1
    MoveableRightFrontWheelPoints[11] = (MoveableRightFrontWheelPoints[11] + Position[1] + Y_Offset) * Scale * -1


def DrawRightRearWheel():
    global MoveableRightRearWheelPoints
    # Draw the Race Car's Right Rear Wheel
    # Set the Right Rear Wheel's Chassis Heading
    _Temp = BaseRightRearWheelPoints.copy()

    _Temp[ 0] = BaseRightRearWheelPoints[ 0] * math.cos(Heading) - BaseRightRearWheelPoints[ 1] * math.sin(Heading)
    _Temp[ 2] = BaseRightRearWheelPoints[ 2] * math.cos(Heading) - BaseRightRearWheelPoints[ 3] * math.sin(Heading)
    _Temp[ 4] = BaseRightRearWheelPoints[ 4] * math.cos(Heading) - BaseRightRearWheelPoints[ 5] * math.sin(Heading)
    _Temp[ 6] = BaseRightRearWheelPoints[ 6] * math.cos(Heading) - BaseRightRearWheelPoints[ 7] * math.sin(Heading)
    _Temp[ 8] = BaseRightRearWheelPoints[ 8] * math.cos(Heading) - BaseRightRearWheelPoints[ 9] * math.sin(Heading)
    _Temp[10] = BaseRightRearWheelPoints[10] * math.cos(Heading) - BaseRightRearWheelPoints[11] * math.sin(Heading)
    
    _Temp[ 1] = BaseRightRearWheelPoints[ 0] * math.sin(Heading) + BaseRightRearWheelPoints[ 1] * math.cos(Heading)
    _Temp[ 3] = BaseRightRearWheelPoints[ 2] * math.sin(Heading) + BaseRightRearWheelPoints[ 3] * math.cos(Heading)
    _Temp[ 5] = BaseRightRearWheelPoints[ 4] * math.sin(Heading) + BaseRightRearWheelPoints[ 5] * math.cos(Heading)
    _Temp[ 7] = BaseRightRearWheelPoints[ 6] * math.sin(Heading) + BaseRightRearWheelPoints[ 7] * math.cos(Heading)
    _Temp[ 9] = BaseRightRearWheelPoints[ 8] * math.sin(Heading) + BaseRightRearWheelPoints[ 9] * math.cos(Heading)
    _Temp[11] = BaseRightRearWheelPoints[10] * math.sin(Heading) + BaseRightRearWheelPoints[11] * math.cos(Heading)

    MoveableRightRearWheelPoints = _Temp.copy()

    # Set the Right Rear Wheel's Position
    MoveableRightRearWheelPoints[ 0] = (MoveableRightRearWheelPoints[ 0] + Position[0] - X_Offset) * Scale
    MoveableRightRearWheelPoints[ 2] = (MoveableRightRearWheelPoints[ 2] + Position[0] - X_Offset) * Scale
    MoveableRightRearWheelPoints[ 4] = (MoveableRightRearWheelPoints[ 4] + Position[0] - X_Offset) * Scale
    MoveableRightRearWheelPoints[ 6] = (MoveableRightRearWheelPoints[ 6] + Position[0] - X_Offset) * Scale
    MoveableRightRearWheelPoints[ 8] = (MoveableRightRearWheelPoints[ 8] + Position[0] - X_Offset) * Scale
    MoveableRightRearWheelPoints[10] = (MoveableRightRearWheelPoints[10] + Position[0] - X_Offset) * Scale

    MoveableRightRearWheelPoints[ 1] = (MoveableRightRearWheelPoints[ 1] + Position[1] + Y_Offset) * Scale * -1
    MoveableRightRearWheelPoints[ 3] = (MoveableRightRearWheelPoints[ 3] + Position[1] + Y_Offset) * Scale * -1
    MoveableRightRearWheelPoints[ 5] = (MoveableRightRearWheelPoints[ 5] + Position[1] + Y_Offset) * Scale * -1
    MoveableRightRearWheelPoints[ 7] = (MoveableRightRearWheelPoints[ 7] + Position[1] + Y_Offset) * Scale * -1
    MoveableRightRearWheelPoints[ 9] = (MoveableRightRearWheelPoints[ 9] + Position[1] + Y_Offset) * Scale * -1
    MoveableRightRearWheelPoints[11] = (MoveableRightRearWheelPoints[11] + Position[1] + Y_Offset) * Scale * -1


def DrawLeftFrontWheel():
    global MoveableLeftFrontWheelPoints
    # Draw the Race Car's Left Front Wheel
    # Set the Left Front Wheel's Chassis Heading
    _Temp = BaseLeftFrontWheelPoints.copy()

    _Temp[ 0] = BaseLeftFrontWheelPoints[ 0] * math.cos(Heading) - BaseLeftFrontWheelPoints[ 1] * math.sin(Heading)
    _Temp[ 2] = BaseLeftFrontWheelPoints[ 2] * math.cos(Heading) - BaseLeftFrontWheelPoints[ 3] * math.sin(Heading)
    _Temp[ 4] = BaseLeftFrontWheelPoints[ 4] * math.cos(Heading) - BaseLeftFrontWheelPoints[ 5] * math.sin(Heading)
    _Temp[ 6] = BaseLeftFrontWheelPoints[ 6] * math.cos(Heading) - BaseLeftFrontWheelPoints[ 7] * math.sin(Heading)
    _Temp[ 8] = BaseLeftFrontWheelPoints[ 8] * math.cos(Heading) - BaseLeftFrontWheelPoints[ 9] * math.sin(Heading)
    _Temp[10] = BaseLeftFrontWheelPoints[10] * math.cos(Heading) - BaseLeftFrontWheelPoints[11] * math.sin(Heading)
    
    _Temp[ 1] = BaseLeftFrontWheelPoints[ 0] * math.sin(Heading) + BaseLeftFrontWheelPoints[ 1] * math.cos(Heading)
    _Temp[ 3] = BaseLeftFrontWheelPoints[ 2] * math.sin(Heading) + BaseLeftFrontWheelPoints[ 3] * math.cos(Heading)
    _Temp[ 5] = BaseLeftFrontWheelPoints[ 4] * math.sin(Heading) + BaseLeftFrontWheelPoints[ 5] * math.cos(Heading)
    _Temp[ 7] = BaseLeftFrontWheelPoints[ 6] * math.sin(Heading) + BaseLeftFrontWheelPoints[ 7] * math.cos(Heading)
    _Temp[ 9] = BaseLeftFrontWheelPoints[ 8] * math.sin(Heading) + BaseLeftFrontWheelPoints[ 9] * math.cos(Heading)
    _Temp[11] = BaseLeftFrontWheelPoints[10] * math.sin(Heading) + BaseLeftFrontWheelPoints[11] * math.cos(Heading)

    MoveableLeftFrontWheelPoints = _Temp.copy()

    # Set the Left Front Wheel's Position
    MoveableLeftFrontWheelPoints[ 0] = (MoveableLeftFrontWheelPoints[ 0] + Position[0] - X_Offset) * Scale
    MoveableLeftFrontWheelPoints[ 2] = (MoveableLeftFrontWheelPoints[ 2] + Position[0] - X_Offset) * Scale
    MoveableLeftFrontWheelPoints[ 4] = (MoveableLeftFrontWheelPoints[ 4] + Position[0] - X_Offset) * Scale
    MoveableLeftFrontWheelPoints[ 6] = (MoveableLeftFrontWheelPoints[ 6] + Position[0] - X_Offset) * Scale
    MoveableLeftFrontWheelPoints[ 8] = (MoveableLeftFrontWheelPoints[ 8] + Position[0] - X_Offset) * Scale
    MoveableLeftFrontWheelPoints[10] = (MoveableLeftFrontWheelPoints[10] + Position[0] - X_Offset) * Scale

    MoveableLeftFrontWheelPoints[ 1] = (MoveableLeftFrontWheelPoints[ 1] + Position[1] + Y_Offset) * Scale * -1
    MoveableLeftFrontWheelPoints[ 3] = (MoveableLeftFrontWheelPoints[ 3] + Position[1] + Y_Offset) * Scale * -1
    MoveableLeftFrontWheelPoints[ 5] = (MoveableLeftFrontWheelPoints[ 5] + Position[1] + Y_Offset) * Scale * -1
    MoveableLeftFrontWheelPoints[ 7] = (MoveableLeftFrontWheelPoints[ 7] + Position[1] + Y_Offset) * Scale * -1
    MoveableLeftFrontWheelPoints[ 9] = (MoveableLeftFrontWheelPoints[ 9] + Position[1] + Y_Offset) * Scale * -1
    MoveableLeftFrontWheelPoints[11] = (MoveableLeftFrontWheelPoints[11] + Position[1] + Y_Offset) * Scale * -1


def DrawLeftRearWheel():
    global MoveableLeftRearWheelPoints
    # Draw the Race Car's Left Rear Wheel
    # Set the Left Rear Wheel's Chassis Heading
    _Temp = BaseLeftRearWheelPoints.copy()

    _Temp[ 0] = BaseLeftRearWheelPoints[ 0] * math.cos(Heading) - BaseLeftRearWheelPoints[ 1] * math.sin(Heading)
    _Temp[ 2] = BaseLeftRearWheelPoints[ 2] * math.cos(Heading) - BaseLeftRearWheelPoints[ 3] * math.sin(Heading)
    _Temp[ 4] = BaseLeftRearWheelPoints[ 4] * math.cos(Heading) - BaseLeftRearWheelPoints[ 5] * math.sin(Heading)
    _Temp[ 6] = BaseLeftRearWheelPoints[ 6] * math.cos(Heading) - BaseLeftRearWheelPoints[ 7] * math.sin(Heading)
    _Temp[ 8] = BaseLeftRearWheelPoints[ 8] * math.cos(Heading) - BaseLeftRearWheelPoints[ 9] * math.sin(Heading)
    _Temp[10] = BaseLeftRearWheelPoints[10] * math.cos(Heading) - BaseLeftRearWheelPoints[11] * math.sin(Heading)
    
    _Temp[ 1] = BaseLeftRearWheelPoints[ 0] * math.sin(Heading) + BaseLeftRearWheelPoints[ 1] * math.cos(Heading)
    _Temp[ 3] = BaseLeftRearWheelPoints[ 2] * math.sin(Heading) + BaseLeftRearWheelPoints[ 3] * math.cos(Heading)
    _Temp[ 5] = BaseLeftRearWheelPoints[ 4] * math.sin(Heading) + BaseLeftRearWheelPoints[ 5] * math.cos(Heading)
    _Temp[ 7] = BaseLeftRearWheelPoints[ 6] * math.sin(Heading) + BaseLeftRearWheelPoints[ 7] * math.cos(Heading)
    _Temp[ 9] = BaseLeftRearWheelPoints[ 8] * math.sin(Heading) + BaseLeftRearWheelPoints[ 9] * math.cos(Heading)
    _Temp[11] = BaseLeftRearWheelPoints[10] * math.sin(Heading) + BaseLeftRearWheelPoints[11] * math.cos(Heading)

    MoveableLeftRearWheelPoints = _Temp.copy()

    # Set the Left Rear Wheel's Position
    MoveableLeftRearWheelPoints[ 0] = (MoveableLeftRearWheelPoints[ 0] + Position[0] - X_Offset) * Scale
    MoveableLeftRearWheelPoints[ 2] = (MoveableLeftRearWheelPoints[ 2] + Position[0] - X_Offset) * Scale
    MoveableLeftRearWheelPoints[ 4] = (MoveableLeftRearWheelPoints[ 4] + Position[0] - X_Offset) * Scale
    MoveableLeftRearWheelPoints[ 6] = (MoveableLeftRearWheelPoints[ 6] + Position[0] - X_Offset) * Scale
    MoveableLeftRearWheelPoints[ 8] = (MoveableLeftRearWheelPoints[ 8] + Position[0] - X_Offset) * Scale
    MoveableLeftRearWheelPoints[10] = (MoveableLeftRearWheelPoints[10] + Position[0] - X_Offset) * Scale

    MoveableLeftRearWheelPoints[ 1] = (MoveableLeftRearWheelPoints[ 1] + Position[1] + Y_Offset) * Scale * -1
    MoveableLeftRearWheelPoints[ 3] = (MoveableLeftRearWheelPoints[ 3] + Position[1] + Y_Offset) * Scale * -1
    MoveableLeftRearWheelPoints[ 5] = (MoveableLeftRearWheelPoints[ 5] + Position[1] + Y_Offset) * Scale * -1
    MoveableLeftRearWheelPoints[ 7] = (MoveableLeftRearWheelPoints[ 7] + Position[1] + Y_Offset) * Scale * -1
    MoveableLeftRearWheelPoints[ 9] = (MoveableLeftRearWheelPoints[ 9] + Position[1] + Y_Offset) * Scale * -1
    MoveableLeftRearWheelPoints[11] = (MoveableLeftRearWheelPoints[11] + Position[1] + Y_Offset) * Scale * -1


def DrawTrack():
    # Draw the Track
    i = 0
    while(i < len(CenterlinePoints) - 1):
        # Centreline
        DrawDashedLine(CenterlinePoints[i][0],CenterlinePoints[i][1], CenterlinePoints[i+1][0], CenterlinePoints[i+1][1], 3, 'yellow', (255, 5))
        # Inside Line
        DrawLine(InsidePoints[i][0],InsidePoints[i][1], InsidePoints[i+1][0], InsidePoints[i+1][1], 3, 'black')
        # Outside Line
        DrawLine(OutsidePoints[i][0],OutsidePoints[i][1], OutsidePoints[i+1][0], OutsidePoints[i+1][1], 3, 'black')
        i += 1
    # Draw Start/Finish Line
    DrawDashedLine(OutsidePoints[0][0],OutsidePoints[0][1], InsidePoints[0][0], InsidePoints[0][1], 5, 'red', (255, 255))


def DrawCar():
    global m_Chassis, m_RightFrontWheel, m_LeftFrontWheel, m_RightRearWheel, m_LeftRearWheel
    # Draw the Race Car's Chassis
    DrawChassis()
    m_Chassis = m_Canvas.create_polygon(MoveableChassisPoints, outline='black', width=0.5, fill='red')
    DrawRightFrontWheel()
    m_RightFrontWheel = m_Canvas.create_polygon(MoveableRightFrontWheelPoints, width=0, fill='black')
    DrawRightRearWheel()
    m_RightRearWheel = m_Canvas.create_polygon(MoveableRightRearWheelPoints, width=0, fill='black')
    DrawLeftFrontWheel()
    m_LeftFrontWheel = m_Canvas.create_polygon(MoveableLeftFrontWheelPoints, width=0, fill='black')
    DrawLeftRearWheel()
    m_LeftRearWheel = m_Canvas.create_polygon(MoveableLeftRearWheelPoints, width=0, fill='black')


def Up_Pressed(event):
    global PositionIndex, Position, m_Chassis, m_RightFrontWheel, m_RightRearWheel, m_LeftFrontWheel, m_LeftRearWheel, Heading
    PositionIndex += 1
    if(PositionIndex == len(CenterlinePoints)):
        PositionIndex = PositionIndex - len(CenterlinePoints) + 1
    NextIndex = PositionIndex + 1
    if(NextIndex == len(CenterlinePoints)):
        NextIndex = NextIndex - len(CenterlinePoints) + 1
    if(CenterlinePoints[PositionIndex] == CenterlinePoints[NextIndex]):
        PositionIndex += 1
        NextIndex = PositionIndex + 1
    Position = CenterlinePoints[PositionIndex]
    NextPosition = CenterlinePoints[NextIndex]
    dx = NextPosition[0] - Position[0]
    dy = NextPosition[1] - Position[1]
    Heading = math.atan2(dy, dx) - math.pi / 2

    m_Canvas.delete(m_Chassis)
    m_Canvas.delete(m_RightFrontWheel)
    m_Canvas.delete(m_RightRearWheel)
    m_Canvas.delete(m_LeftFrontWheel)
    m_Canvas.delete(m_LeftRearWheel)
    DrawChassis()
    m_Chassis = m_Canvas.create_polygon(MoveableChassisPoints, outline='black', width=0.5, fill='red')
    DrawRightFrontWheel()
    m_RightFrontWheel = m_Canvas.create_polygon(MoveableRightFrontWheelPoints, width=0, fill='black')
    DrawRightRearWheel()
    m_RightRearWheel = m_Canvas.create_polygon(MoveableRightRearWheelPoints, width=0, fill='black')
    DrawLeftFrontWheel()
    m_LeftFrontWheel = m_Canvas.create_polygon(MoveableLeftFrontWheelPoints, width=0, fill='black')
    DrawLeftRearWheel()
    m_LeftRearWheel = m_Canvas.create_polygon(MoveableLeftRearWheelPoints, width=0, fill='black')
    m_Window.update()


def Down_Pressed(event):
    global PositionIndex, Position, m_Chassis, m_RightFrontWheel, m_RightRearWheel, m_LeftFrontWheel, m_LeftRearWheel, Heading
    PositionIndex -= 1
    if(PositionIndex == 0):
        PositionIndex = len(CenterlinePoints) - 1
    NextIndex = PositionIndex + 1
    if(NextIndex == len(CenterlinePoints)):
        NextIndex = NextIndex - len(CenterlinePoints) + 1
    if(CenterlinePoints[PositionIndex] == CenterlinePoints[NextIndex]):
        PositionIndex -= 1
        NextIndex = PositionIndex + 1
    Position = CenterlinePoints[PositionIndex]
    NextPosition = CenterlinePoints[NextIndex]
    dx = NextPosition[0] - Position[0]
    dy = NextPosition[1] - Position[1]
    Heading = math.atan2(dy, dx) - math.pi / 2

    m_Canvas.delete(m_Chassis)
    m_Canvas.delete(m_RightFrontWheel)
    m_Canvas.delete(m_RightRearWheel)
    m_Canvas.delete(m_LeftFrontWheel)
    m_Canvas.delete(m_LeftRearWheel)
    DrawChassis()
    m_Chassis = m_Canvas.create_polygon(MoveableChassisPoints, outline='black', width=0.5, fill='red')
    DrawRightFrontWheel()
    m_RightFrontWheel = m_Canvas.create_polygon(MoveableRightFrontWheelPoints, width=0, fill='black')
    DrawRightRearWheel()
    m_RightRearWheel = m_Canvas.create_polygon(MoveableRightRearWheelPoints, width=0, fill='black')
    DrawLeftFrontWheel()
    m_LeftFrontWheel = m_Canvas.create_polygon(MoveableLeftFrontWheelPoints, width=0, fill='black')
    DrawLeftRearWheel()
    m_LeftRearWheel = m_Canvas.create_polygon(MoveableLeftRearWheelPoints, width=0, fill='black')
    m_Window.update()


#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------
#TrackFile = "../tracks/China_track.csv"
TrackFile = "../tracks/Mexico_track.csv"
WindowWidth = 1920
WindowHeight = 1080

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
SetWheelPoints()
PositionIndex = 0
Position = CenterlinePoints[PositionIndex]
dx = CenterlinePoints[1][0] - Position[0]
dy = CenterlinePoints[1][1] - Position[1]
Heading = math.atan2(dy, dx) - math.pi / 2

m_Window.title("DeepRacer - Track Simulator")
m_Window.bind("<Up>", Up_Pressed)
m_Window.bind("<Down>", Down_Pressed)
m_Canvas = Canvas(m_Window, width=WindowWidth, height=WindowHeight, background='white')
m_Canvas.grid(row=0, column=0)
DrawTrack()
DrawCar()
m_Canvas.pack()
m_Window.mainloop()
