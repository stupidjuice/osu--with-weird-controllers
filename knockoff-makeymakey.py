import tkinter as tker
import cv2
import numpy as np
import osuinput
import actions
import saveload
from time import sleep

#parameters (did i spell that right?)

mode = "GREEN" #set to "RED", "GREEN", or "BLUE" to set which channel the program checks against lol
threshold = 128 #threshold the color channel above needs to pass in order for the input to happen

#vars used in the code lol (dont fuck with this stuff its needed)
firstClickPt = []
releaseClickPt = []
mousedown = False
boxes = []
inprogressBox = []
colormodeToInt = { "RED": 2, "GREEN": 1, "BLUE": 0 }

def loadBoxes():
    global boxes
    boxes = saveload.readBoxes()

#ui
root = tker.Tk()
root.geometry("320x240")
root.title("options")
tker.Button(root, text="Save boxes", command=lambda:saveload.saveBoxes(boxes)).pack()
tker.Button(root, text="Load boxes", command=lambda:loadBoxes()).pack()
tker.Label(root, text="Input the action you want the next box you create\n does (check actions.txt for options)").pack()
textbox = tker.Text(root, height=1)
textbox.pack()
textbox.insert("end", "KEY_Z")

#open camera
cam = cv2.VideoCapture(0)
if not (cam.isOpened()):
    print("Could not open video device")

#allows user to draw boxes to select idk
def drawBox(event, x, y, flags, params):
    global firstClickPt, releaseClickPt, boxes, mousedown, inprogressBox
    if event == cv2.EVENT_LBUTTONDOWN:
        firstClickPt = [x, y]
        inprogressBox = firstClickPt
        mousedown = True
    
    if mousedown:
        if event == cv2.EVENT_MOUSEMOVE:
            inprogressBox = [x, y]

    if event == cv2.EVENT_LBUTTONUP:
        mousedown = False
        releaseClickPt = [x, y]
        if firstClickPt[0] == releaseClickPt[0] or firstClickPt[1] == releaseClickPt[1]:
            return
        boxes.append([firstClickPt, releaseClickPt, 0, textbox.get("1.0", "end-1c")])
        print(boxes)

while(True):
    #update ui
    root.update()
    #print(boxes)
    #read camera input
    result, image = cam.read()

    #------------WILL BE MOVED TO ITS OWN FUNCTION "SOON"------------
    #draw the current active box thats being dragged (if it exists)
    if mousedown and len(inprogressBox) > 0:
        minx = min(firstClickPt[0], inprogressBox[0])
        maxx = max(firstClickPt[0], inprogressBox[0])
        miny = min(firstClickPt[1], inprogressBox[1])
        maxy = max(firstClickPt[1], inprogressBox[1])
        for x in range(minx, maxx):
            image[maxy][x] = [0, 255, 0]
            image[miny][x] = [0, 255, 0]
        for y in range(miny, maxy):
            image[y][maxx] = [0, 255, 0]
            image[y][minx] = [0, 255, 0]
    
    #draw boxes and get the averages of their colors
    for i in boxes:
        currentAverage = 0
        minx = min(i[0][0], i[1][0])
        maxx = max(i[0][0], i[1][0])
        miny = min(i[0][1], i[1][1])
        maxy = max(i[0][1], i[1][1])
        xrange = maxx - minx
        yrange = maxy - miny
        for x in range(minx, maxx):
            image[maxy][x] = [0, 0, 255]
            image[miny][x] = [0, 0, 255]
        for y in range(miny, maxy):
            image[y][maxx] = [0, 0, 255]
            image[y][minx] = [0, 0, 255]
        #i am extremely sorry for this fucking awful double-for loop but its 1:00 AM please help me
        for x in range(minx, xrange + minx):
            for y in range(miny, yrange + miny):
                currentAverage += image[y][x][colormodeToInt[mode]] #again, im sorry for this
        currentAverage /= xrange * yrange
        i[2] = currentAverage
        
        if currentAverage > threshold:
            print("Exceeded threshold, executing: " + i[3])

            event = i[3]
            if event in actions.mouseMovementEvents:
                osuinput.mouseMovementEvent(event, 1)
            elif event in actions.clickEvents:
                osuinput.mouseClickEvent(event)
            
    #-----------------------------------------------------------------

    cv2.imshow('webcam', image)
    cv2.setMouseCallback('webcam', drawBox)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    sleep(0.033)

cam.release()
cv2.destroyAllWindows()