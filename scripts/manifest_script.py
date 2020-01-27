#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Creates a qiime2 manifest from a directory of FASTQ files generated in
Genome Quebec naming style
"""

# Built-in/Generic Imports
import os, sys, argparse
# Libs
import csv, re

__author__ = 'Mathew Richards'
__copyright__ = 'Copyright 2020, AAFC-AAC'
__credits__ = ['Rodrigo Ortega Polo']
__license__ = 'GPL'
__version__ = '3'
__maintainer__ = 'Mathew Richards'
__email__ = 'mathew.richards@canada.ca'
__status__ = 'Complete'

print("\n", "****Manifest Script****", "\n")

# argparse section for command line arguments
parser = argparse.ArgumentParser(description='Create a qiime2 manifest file')
parser.add_argument('directory',
            help='The directory path where your FASTQ files are located')
args = parser.parse_args()

try:
    dir_name = args.directory
    print("The entered directory is:", dir_name, "\n")
except:
    print('ERROR: Enter path to data in command line')

#check the number of arguments
#print("Num of arguments:", len(sys.argv), "arguments.", "\n")
#print("Argument list:", str(sys.argv), "\n")

csv_list = []

# read in the files and use RegEx on filenames to filter
for root, dirs, files in os.walk(dir_name):
    for filename in files:
        # print(filename)
        temp = re.search("(?<=FLD\d{4}).\w*.fastq.gz$", filename)
        sample_name = temp.group()
        sample_name = sample_name.replace('.','')
        sample_name = sample_name.replace('fastqgz','')
        sample_name = sample_name.replace('_R1','')
        sample_name = sample_name.replace('_R2','')
        #print(sampleName)
        abs_path = os.path.join(root, filename)
        direction = re.search("R\d", filename)
        if direction.group() == "R1":
            temp = "forward"
        else:
            temp = "backward"
        csv_list.append([sample_name, abs_path, temp])

#start the .csv document
print("Creating the .csv file in the PWD", "\n")
with open('manifest.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|',
        quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['sample-id', 'absolute-filepath', 'direction'])
    for i in range(len(csv_list)):
        filewriter.writerow(csv_list[i])

exit()
