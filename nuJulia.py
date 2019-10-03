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

"""
calculates the difference between 2 times
"""
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

"""
returns the current time as a string
"""
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

"""
returns true if given number is a float
"""
def isFloat(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

"""
function to be called from other files so that 
can be run based off command line args
"""
def loadFromArgs():
    args=[float(num) for num in sys.argv if isFloat(num)]
    args = [int(num) if int(num)==num else num for num in args ]
    julia(*args)#the *args expands the list


"""
scales an integer to between 2 other numbers
inputs:
    val(int): the value to be scaled
    Tmin(int): minimum val could be
    Tmax(int): maxumum val could be
    Rmin(int): minimum val should be after transform
    Rmax(int): maximum val should be after transform
"""
def rangeScale(val, Tmin, Tmax, Rmin, Rmax):
    res = (val-Rmin)/(Rmax-Rmin)
    return res*(Tmax-Tmin) + Tmin

"""
determines if name is already present in folder
returns true if already taken
"""
def nameTaken(name):
    if name == 1:
        return True
    if "./"+name in glob.glob("./interestingResults/*"):
        print("++++++++\nCRISIS AVERTED\n++++++++")
        return True
    return False

"""
depreciated since was not working reliable
made window to get attention when program finished
"""
def getAttention():
    from tkinter import Tk
    Tk().mainloop()

"""
handles output to command line and contruction of image
inputs:
    c(int): specifies which slice of fractal space
    width(int): the width of the image
    height(int): the height of the image
    max(int): the maximum value in the image(higher=darker)
    xView(int): x value for position of image in the slice of fractal space
    yView(int): y value for position of image in the slice of fractal space
"""
def julia(c, width, height, max,xView, yView):
    arr = np.zeros((height, width, 3))
    fileName=1#so it starts
    while nameTaken(fileName):
        fileName = "interestingResults\\{}nuJulia{}.png".format(randint(1,99),c)
    
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
"""
used for changing julia set with different functions, if you just return
(x,y) it will just be a julia set
"""
def getFunky(x,y):
    #y = erf(1-erf(y))
    #y=math.gamma(abs(y)+0.01)
    #x = cos(2**sin(x))
    return (x,y)

"""
determines what the value of a pixel at a given position 
should be
Parameters:
    c(int): specifies which slice of fractal space
    x(int): x position of pixel in image
    y(int): y position of pixel in image
    max(int): maximum value in image, higher is darker
"""
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
    c=.4
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
