#!/usr/bin/python
import os
import sys
path = os.getcwd()
steps=0

if len(sys.argv) < 2:
    print("Don't know how many steps to go up")
else:
    steps = int(sys.argv[1])
    for step in range(steps):
        path=path +"/.."
try:
    print("Going to: "+ path) 
    os.chdir(path)
    print(os.getcwd())
except OSError:
    print("Some error occurred")
