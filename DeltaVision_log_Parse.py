#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import os
from tkinter.filedialog import askdirectory


lass LogExtraction:
    def __init__(self, path):
        # Define path
        self.path_to_log = path
        # Get file name from path
        self.file = self.path_to_log.split('/')
        self.file = self.file[-1]

    # Extract x, y, & z dimensions of image stack
    def dim_extract(self):
        with open(self.path_to_log, 'rb') as file:
            try:
                for line in file:
                    line = line.decode()
                    if (line.find("Pixel Size:") > -1):
                        self.pxsize = str(line)
                        self.pxsize = self.pxsize.split('\n')
                        self.pxsize = self.pxsize[0].split('\t')
                        self.pxsize = self.pxsize[-1]
                        self.pxsize = self.pxsize.split(' ')
                        self.pxsize = self.pxsize[-1]
            # Was getting error due to "./file.log" Files
            # Use Shell Script to remove "./file.log" Files
            except UnicodeDecodeError:
                print(
                    "'utf-8' codec can't decode byte 0xb0 in position 37: invalid start byte'")
                print(self.file)

    # Extract number of slices in image stack
    def numOfSlice(self):
        with open(self.path_to_log, 'rb') as file:
            try:
                for line in file:
                    line = line.decode()
                    if line.find("ZWT Dimensions (expected):") > -1:
                        self.num_slice = str(line)
                        self.num_slice = self.num_slice.split('\n')
                        self.num_slice = str(self.num_slice[0]).split('\t')
                        self.num_slice = self.num_slice[-1]
                        self.num_slice = self.num_slice.split('x')
                        self.num_slice = self.num_slice[0].split(' ')
                        self.num_slice = self.num_slice[0]
            # Was getting error due to "./file.log" Files
            # Use Shell Script to remove "./file.log" Files
            except UnicodeDecodeError:
                print(
                    "'utf-8' codec can't decode byte 0xb0 in position 37: invalid start byte'")
                print(self.file)

    def all(self):
        self.dim_extract()
        self.numOfSlice()
        # Return filename, z-step size, and number of slices
        return [self.file, self.pxsize, self.num_slice]


def log_parse_func(path):
    dict = {}  # dictionary for file information
    dict1 = {}  # dictionary for dictionary of files
    j = 0  # index number of dict1
    #loop through all files in directory that are .log files
    for i in os.listdir(path):
        if i.endswith(".log"):
            file_dir = path+i
            logex = LogExtraction(file_dir)  # initialise class
            dict = {}
            dict['File'] = (logex.all()[0])
            dict['Z-Step'] = (logex.all()[1])
            dict['NumOfSlices'] = (logex.all()[2])
            dict1[f'{j}'] = dict
            j += 1
    df = pd.DataFrame(dict1)
    df = df.transpose()
    #write df to csv in a location above the input directory
    path = path.replace('/log/', '/Output_Data/')
    df.to_csv(path+'metadata.csv')


def main():
    path = askdirectory()
    log_parse_func(path)
    print('Complete')  # in case no errors occur
    return


if __name__ == "__main__":
    main()
