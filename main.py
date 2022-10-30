# Sliq.py
# SENG 474
# Jeremy Ho & Helen Lin

import os
import sys
import string
import time
from sliq import *

def main():
    input_file_name = 'data.csv'
    data = []
    print("Starting to read data...")
    # Read in the data from the csv file
    with open(input_file_name, 'r') as f:
        for line in f:
            data.append(line.split(','))

    print("Finished reading data.")
    #print(data)

    sliqObj = sliq(data)
    print(sliqObj.display())
    print("SLIQ Tree has been created.")

if __name__ == '__main__':
    main()
