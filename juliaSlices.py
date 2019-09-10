import datetime
import numpy as np
import imageio
import keyboard
from random import randint, random
from PIL import Image
import pyautogui as pyg
import subprocess
from win10toast import ToastNotifier


toaster = ToastNotifier()
#dictPath = "storage\\my.secretdata"


def currTime():
    a = datetime.datetime.now().time()
    a = str(a).split(":")
    isPm="am"
    if int(a[0]) > 12:
        isPm="pm"
        a[0] = int(a[0])-12
    a = [str(num) for num in a if len(str(num)) < 3]
    final = ":".join(a)+isPm #XXX test this
    return final


def rangeScale(val, Tmin, Tmax, Rmin, Rmax):
    res = (val-Rmin)/(Rmax-Rmin)
    res = (res*(Tmax-Tmin)) + Tmin
    return res

def juliaPixel(c, x, y):
    max=70
    detail = 1#smaller makes it go faster, smaller is more detail
    i=0
    while i<max and x**2 + y**2 < 4:
        xtemp = x**2 - y**2
        y = 2*x*y  + c
        x = xtemp + c
        i+=detail
    i = rangeScale(i, 0, 255, 0, max)

    #return(0,i,255-i)#nice and blue
    return(i,i,i)#black and white

def julia(c, width=100, height=50):
    arr = np.zeros((height, width, 3))
    startTime = currTime()
    #take off end bits of it so ends at minutes
    fileName = "newSlices\\{}julia.png".format(c)
    print("operation started at", startTime)
    print("\ncomputing fractal {}...".format(fileName))

    for x in range(0, width):
        #viewPort = (1.1, 1.4)#close
        viewPort = (1.3, 1.3)#wide
        currX = rangeScale(x, -viewPort[0], viewPort[0], 0, width)
        for y in range(0, height):
            currY = rangeScale(y, -viewPort[1], viewPort[1], 0, height)
            arr[y,x]=juliaPixel(c, currX, currY)
        if keyboard.is_pressed("alt+ctrl+caps lock"):
            return False
    endTime = currTime()
    imageio.imwrite(fileName, arr)
    print("operation ended at", endTime)
    return True
#you are talking about algorithms too broadly
#all biased?
#a mathmatition makes a program to compute prime numbers
#is that biased? should he be regulated?
#need more specific terms than all algoritms
#you are looking at social algorithms, programs that are about people
#weather prediction algorthm, not taking input from people

#I really liked highly rational yet deeply mysterious, fractal no 
#idea how it works

#privacy concerns, can see what other people post(like on assignment)
#those who didn't want their assignment to be seen can still be seen

def main():
    detail=0.001
    min = 0.3
    c=0.349
    nums = []
    nums.sort(reverse=True)

    if len(nums) > 0:
        for x in nums:
            julia(x,360,360)
    else:
        while c >= min:
            if not julia(c, 360, 360):
                break
            c = round(c-detail, 4)
    toaster.show_toast("julia result","program is done")
    #subprocess.call("slices\\gifSorter.py", shell=True)

 
if __name__ == "__main__":
    main()