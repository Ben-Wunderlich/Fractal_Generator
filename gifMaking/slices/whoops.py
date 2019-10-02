'''import os
import glob

names = glob.glob("*.png*")
for name in names:
    newName = name.split("_")[0]
    print(newName)
    os.rename(name, newName)'''
input()