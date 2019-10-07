from datetime import datetime
import numpy as np
from imageio import imwrite
import keyboard
from random import randint, random
from PIL import Image   
import sys#add command line args if argv > 1
import math
from math import sin,cos,erf, erfc, log
import glob

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
see julia for how they will be accepted
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
    expansion(int): how far spaced each value should be from default
    useMandel(bool): specifies whether to use mandelbrot set or julia set(true is use mandelbrot set)
    #NOTE that if useMandel is true the c value will not be used

"""
def julia(c, width, height, max,xView, yView, expansion, useMandel):
    arr = np.zeros((height, width, 3))
    fileName=1#so it starts
    while nameTaken(fileName):
        fileName = "interestingResults\\{}nuJulia{}.png".format(randint(1,999),c)
    
    print("""STARTING\nfileSize={}x{}, c={}
    max={}, view={}x{}""".format(width, height, c, max,xView,yView))
    print("operation started at", currTime())
    strtStore = datetime.now()
    print("\ncomputing {}...".format(fileName[19:]))

    for x in range(0, width):
        currX = rangeScale(x, -xView, xView, 0, width)
        for y in range(0, height):
            currY = rangeScale(y, -yView, yView, 0, height)
            arr[y,x]=juliaPixel(c, currX, currY, max, expansion, useMandel)
        if keyboard.is_pressed("caps lock"):
            print("INTERRUPTED")
            break

    arr = arr / arr.max() #normalizing data in range 0 - 255
    arr = 255 * arr
    img = arr.astype(np.uint8)
    imwrite(fileName, img)

    print("\n...finished!\noperation ended at", currTime())
    print("it took {}".format(timeDiff(strtStore,datetime.now())))

#START EXPERIMENTING HERE
"""
used for changing julia set with different functions, if you just 
return(x,y) it will be an unmodified julia set
"""
def getFunky(x,y):
    #y = erf(1-erf(y))
    #y=math.gamma(abs(y)+0.01)
    #x = cos(2**sin(x))
    if y > 0:
        y=log(y)
    return (x,y)

"""
determines what the value of a pixel at a given position 
should be
Parameters:
    c(int): specifies which slice of fractal space
    x(int): x position of pixel in image
    y(int): y position of pixel in image
    max(int): maximum value in image, higher is darker
    expansion(int): how far spaced each value should be from default
    useMandel(bool): specifies whether to use mandelbrot set or julia set(true is use mandelbrot set)
    #NOTE that if useMandel is true the c value will not be used
"""
def juliaPixel(c, x, y,max, expansion, useMandel):
    if useMandel:
        x0,y0 = x, y#only needed when doing mandelbrot
    
    i=0
    while i<max and x**2 + y**2 < 4:
        if useMandel: #MANDELBROT SET
            xtemp = x**2 - y**2 + x0 
            y = 2*x*y + y0
            x = xtemp
        else:        #JULIA
            xtemp = x**2 - y**2  
            y = 2*x*y + c
            x = xtemp + c

        
        x,y = getFunky(x,y)
        x*=expansion
        y*=expansion
        i+=1
    #i=cos(i)
    i = int(round(rangeScale(i, 0, 255, 0, max)))

    return(i,i,i)#white on black
    #return(0,i//1.5,i)#light blue on black
    #return(0,i,255-i)# green on blue

def main():
    dimensions = (400,400)
    #dimensions=(1000,1000)
    #dimensions = (4000, 2200)

    if len(sys.argv) > 1:
        loadFromArgs()
        return
    c=.5
    width=dimensions[0]
    height=dimensions[1]
    xView=1#full view is 2 2, interesting view is 1 1
    yView=0.55
    expansion=1
    useMandelbrotSet=False
    max=40#smaller is brighter#45
#pick 2 points on a rectangle, make line between them

    julia(c,width,height,max,xView,yView, expansion, useMandelbrotSet)

if __name__ == "__main__":
    main()
