# Sliq.py
# SENG 474
# Jeremy Ho & Helen Lin

import os
import sys
import string
import time
from sliq import *

def main():
    data = []
    print("Starting to read data...")
    # Read in the data from the csv file
    with open('data.csv', 'r') as f:
        for line in f:
            data.append(line.split(','))

    print("Finished reading data.")
    #print(data)

    # Process input
    startTime = time.time()
    sliqObj = sliq(data)
    endTime = time.time()
    # print CL.leaves
    print(sliqObj.displayTree())
    print("SLIQ took " + str(endTime - startTime) + " seconds" + " to run.")

if __name__ == '__main__':
    main()
