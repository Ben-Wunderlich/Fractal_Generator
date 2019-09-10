from datetime import datetime
import numpy as np
from imageio import imwrite
import keyboard
from random import randint, random
import random
from PIL import Image
from win10toast import ToastNotifier    
import sys#add command line args if argv > 1
import math
from math import sin,cos, tan
import glob

def timeDiff(startTime, endTime):
    deltaT = endTime-startTime
    secDiff=deltaT.seconds
    if secDiff==0:
        msTime=deltaT.microseconds//1000
        ratio = str(int(msTime/1000 *100))+"% of a second"
        
        return "it took {}ms, thats {}".format(msTime,ratio)

    hDiff=0
    minDiff=0
    while secDiff >= 3600:
        secDiff-=3600
        hDiff+=1
    while secDiff >= 60:
        secDiff-=60
        minDiff+=1

    return "{}h, {}m, {}s".format(hDiff,minDiff,secDiff)

def currTime():
    a = datetime.now()
    arr = []
    arr.extend((a.hour,a.minute,a.second))
    isPm="am"
    if arr[0] > 12:
        isPm="pm"
        arr[0] -= 12
    arr = [str(el) for el in arr]
    for i in range(1,3):#1,2
        while len(arr[i]) < 2:
            arr[i]="0"+arr[i]
    return ":".join(arr)+isPm

def isFloat(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

def loadFromArgs():
    args=[float(num) for num in sys.argv if isFloat(num)]
    args = [int(num) if int(num)==num else num for num in args ]
    julia(*args)#the *args expands the list

def rangeScale(val, Tmin, Tmax, Rmin, Rmax):
    res = (val-Rmin)/(Rmax-Rmin)
    return res*(Tmax-Tmin) + Tmin

def nameTaken(name):
    if name == 1:
        return True
    if "./"+name in glob.glob("./interestingResults/*"):
        print("++++++++\nCRISIS AVERTED\n++++++++")
        return True
    return False


def julia(c, width, height, max,xView, yView, fileName):
    arr = np.zeros((height, width, 3))
    print("""STARTING\nfileSize={}x{}, c={}
    max={}, view={}x{}""".format(width, height, c, max,xView,yView))
    print("operation started at", currTime())
    strtStore = datetime.now()
    print("\ncomputing {}...".format(fileName[19:-4]))

    for x in range(0, width):
 
        currX = rangeScale(x, -xView, yView, 0, width)
        for y in range(0, height):
            currY = rangeScale(y, -yView, yView, 0, height)
            arr[y,x]=juliaPixel(c, currX, currY, max)
        if keyboard.is_pressed("alt+ctrl+caps lock"):
            print("INTERRUPTED")
            break

    arr = arr / arr.max() #normalizing data in range 0 - 255
    arr = 255 * arr
    img = arr.astype(np.uint8)
    imwrite(fileName, img)

    print("\n...finished!\noperation ended at", currTime())
    print("it took {}".format(timeDiff(strtStore,datetime.now())))
    #toaster.show_toast("program is done","julia {}".format(c))

def juliaPixel(c, x, y,max):
    i=0
    while i<max and x**2 + y**2 < 4:
        xtemp = x**2 - y**2
        y = 2*x*y + c
        x = xtemp + c
        ############
        #x=(x%val)*(math.tan(x)*val_2+0.01)
        #y=(y%val)*(math.tan(y)*val_2+0.01)
        #if weirdCondition(x,y):

        i+=1
    #i=sin(i)
    i = int(round(rangeScale(i, 0, 255, 0, max)))

    #return(i,i,i)#white on black
    return(0,i//1.5,i)#light blue on black
    #return(0,i,255-i)# on blue

def main():
    i = 3
    while i > 0:
        fileName = "newSlices\\{}sliceJulia.png".format(i)
        max = round((5/i)**2, 5)
        julia(i, 360, 360, max, 2, 2, fileName)
        i = round(i-(i/10)**2, 5)
        if keyboard.is_pressed("alt+ctrl+caps lock"):
            print("INTERRUPTED")
            break


if __name__ == "__main__":
    main()
#pick 2 points on a rectangle, make line between them