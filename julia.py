from datetime import datetime
import numpy as np
from imageio import imwrite
import keyboard
from random import randint, random
from PIL import Image
from win10toast import ToastNotifier    
import sys#add command line args if argv > 1

toaster = ToastNotifier()
dictPath = "storage\\my.secretdata"

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

def juliaPixel(c, x, y,max):
    #max=15#minimalist
    i=0
    while i<max and x**2 + y**2 < 4:
        xtemp = x**2 - y**2
        y = 2*x*y  + c
        x = xtemp + c
        i+=1
    i = int(round(rangeScale(i, 0, 255, 0, max)))

    #return(i,i,i)#white on black
    return(0,i//1.5,i)#light blue on black
    #return(0,i,255-i)# on blue


def julia(c, width=100, height=50, max=15,xView=1.5, yView=1.3):
    arr = np.zeros((height, width, 3))
    fileName = "interestingResults\\{}julia{}.png".format(randint(1,99),c)
    print("""STARTING\nfileSize={}x{}, c={}
max={}, view={}x{}""".format(width, height, c, max,xView,yView))
    print("operation started at", currTime())
    strtStore = datetime.now()
    print("\ncomputing {}...".format(fileName[19:-4]))

    for x in range(0, width):
 
        currX = rangeScale(x, -xView, xView, 0, width)
        for y in range(0, height):
            currY = rangeScale(y, -yView, yView, 0, height)
            arr[y,x]=juliaPixel(c, currX, currY, max)
        if keyboard.is_pressed("alt+ctrl+caps lock"):
            break

    arr = arr / arr.max() #normalizing data in range 0 - 255
    arr = 255 * arr
    img = arr.astype(np.uint8)
    imwrite(fileName, img)

    print("\n...finished!\noperation ended at", currTime())
    print("it took {}".format(timeDiff(strtStore,datetime.now())))
    toaster.show_toast("program is done","julia {}".format(c))

def main():
    if len(sys.argv) > 1:
        loadFromArgs()
        return
    c=-0.6
    width=100
    height=100
    xView=1.5
    yView=1.3
    max=15

    #julia(-0.55,1920,1080)
    #julia(0.349, 50,50)
    #julia(3,5,10)
    #julia(0.355,100,100)
    #julia(0.38,200,200)
    #julia(0.36, 1000, 1000)
    #julia(0.785, 700,500)
    #julia(0.489, 800, 500)

    #things to try when have time
    #julia(0.3842, 2000, 1500)#do overnight
    #julia(0.4, 1400, 800)#also overnight, do first
    #julia(0.35, 1000, 800)#super cool
    julia(c,width,height,max,xView,yView)

    #try negative numbers

if __name__ == "__main__":
    main()