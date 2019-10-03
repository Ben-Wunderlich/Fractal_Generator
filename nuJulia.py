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
from math import sin,cos,erf
import glob

toaster = ToastNotifier()

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

def getAttention():
    from tkinter import Tk
    Tk().mainloop()

def julia(c, width=100, height=50, max=15,xView=1.5, yView=1.3):
    arr = np.zeros((height, width, 3))
    fileName=1#so it starts
    while nameTaken(fileName):
        #fileName = "interestingResults\\{}nuJulia{}.png".format(randint(1,99),c)
        fileName = "{}nuJulia{}.png".format(randint(1,99),c)
    
    print("""STARTING\nfileSize={}x{}, c={}
    max={}, view={}x{}""".format(width, height, c, max,xView,yView))
    print("operation started at", currTime())
    strtStore = datetime.now()
    print("\ncomputing {}...".format(fileName))

    for x in range(0, width):
        currX = rangeScale(x, -xView, xView, 0, width)
        for y in range(0, height):
            currY = rangeScale(y, -yView, yView, 0, height)
            arr[y,x]=juliaPixel(c, currX, currY, max)
        #if keyboard.is_pressed("alt+ctrl+caps lock"):
        #    print("INTERRUPTED")
        #    break

    arr = arr / arr.max() #normalizing data in range 0 - 255
    arr = 255 * arr
    img = arr.astype(np.uint8)
    imwrite(fileName, img)

    print("\n...finished!\noperation ended at", currTime())
    print("it took {}".format(timeDiff(strtStore,datetime.now())))
    #toaster.show_toast("program is done","julia {}".format(c))

#START EXPERIMENTING HERE
def getFunky(x,y):
    #y = erf(1-erf(y))
    #y=math.gamma(abs(y)+0.01)
    #x = cos(2**sin(x))
    return (x,y)

#only mess with this if you are feeling bold
def juliaPixel(c, x, y,max):
    x0,y0 = x, y#only needed when doind mandelbrot
    
    expansion=1.2
    i=0
    while i<max and x**2 + y**2 < 4:
        #JULIA
        xtemp = x**2 - y**2  
        y = 2*x*y + c
        x = xtemp + c
        #MANDELBROT
        '''xtemp = x**2 - y**2 + x0 
        y = 2*x*y + y0
        x = xtemp''' 
        
        x,y = getFunky(x,y)
        x*=expansion
        y*=expansion
        i+=1
    i=cos(i)
    i = int(round(rangeScale(i, 0, 255, 0, max)))

    #return(i,i,i)#white on black
    return(0,i//1.5,i)#light blue on black
    #return(0,i,255-i)# on blue

def main():
    dimensions = (400,400)
    #dimensions=(1000,1000)
    #dimensions = (1000, 2000)

    if len(sys.argv) > 1:
        loadFromArgs()
        return
    c=.25
    width=dimensions[0]
    height=dimensions[1]
    xView=1#full view is 2 2, interesting view is 1 1
    yView=1
    max=200#smaller is brighter#45
#pick 2 points on a rectangle, make line between them

    julia(c,width,height,max,xView,yView)
    #getAttention()

if __name__ == "__main__":
    main()
