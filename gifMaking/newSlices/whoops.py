import os
import glob
import re


names = glob.glob("*.png*")
newOnes = []

def findName(val):
    for file in names:
        if val in file:
            return file
    print(val)
    assert(False)
    
for name in names:
    if "_" in name:
        name = name.split("_")[1]
    newName = re.match(r"[\.\d]+", name)
    newOnes.append(float(newName.group()))
    
newOnes.sort()

for i, num in enumerate(newOnes):
    theName = "{}_{}sliceJulia.png".format(i,num)
    oldName = findName(str(num))
    print(oldName, theName)
    os.rename(oldName, theName)
input()