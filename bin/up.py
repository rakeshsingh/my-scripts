#!/usr/bin/python
import os
import sys
from my_scripts.logger import setup_logger

logger = setup_logger()

path = os.getcwd()
steps=0

if len(sys.argv) < 2:
    logger.info("Don't know how many steps to go up")
else:
    steps = int(sys.argv[1])
    for step in range(steps):
        path=path +"/.."
try:
    logger.info("Going to: "+ path) 
    os.chdir(path)
    logger.info(os.getcwd())
except OSError:
    logger.info("Some error occurred")
