#!/usr/bin/env python3

"""
Creates a qiime2 manifest from a directory of FASTQ files generated in
Genome Quebec naming style
"""

# Built-in/Generic Imports
import os
import sys
import argparse
# Libs
import csv
import re


__author__ = 'Mathew Richards'
__copyright__ = 'Copyright 2020, AAFC-AAC'
__credits__ = ['Mathew Richards', 'Rodrigo Ortega Polo']
__license__ = 'GPL'
__version__ = '3'
__maintainer__ = 'Mathew Richards'
__email__ = 'mathew.richards@canada.ca'
__status__ = 'Complete'

print("\n", "****Manifest Script****", "\n")


def setup():
    """Get the directory path from command line arg"""
    # argparse section for command line arguments
    parser = argparse.ArgumentParser(description='Create a qiime2 '
                                     'manifest file')
    parser.add_argument('directory',
                        help='The directory path where '
                        'your FASTQ files are located')
    args = parser.parse_args()

    try:
        dir_name = args.directory
        print("The entered directory is:", dir_name, "\n")
    except OSError:
        print('ERROR: Enter path to data in command line argument')

    return dir_name


# read in the files and use RegEx on file names to filter
def create_list_from_files(dir_name):
    """Using the directory name, create a list of the
    files and their info"""
    csv_list = []
    for root, dirs, files in os.walk(dir_name, followlinks=True):
        for _x in dirs:
            dirs.remove(_x)
        for _x in files:
            # print(filename)
            if re.search(r"(?<=FLD\d{4}).\w*.fastq.gz$", _x) is not None:
                sample_name = re.search(r"(?<=FLD\d{4}).\w*.fastq.gz$", _x).group()
                sample_name = sample_name.replace('.', '')
                sample_name = sample_name.replace('fastpfastqgz', '')
                sample_name = sample_name.replace('_R1', '')
                sample_name = sample_name.replace('_R2', '')
                sample_name = sample_name.replace('_', '-')
                cwd = os.getcwd()
                abs_path = cwd + '/' + os.path.join(root, _x)
                direction = re.search(r"R\d", _x)
                if direction.group() == "R1":
                    temp = "forward"
                else:
                    temp = "reverse"
                csv_list.append([sample_name, abs_path, temp])
            elif re.search(r'.*?_S\d*_L001_R\d', _x) is not None:
                sample_name = re.search(r'.*?_S', _x).group()
                sample_name = sample_name.replace('_S','')
                sample_name = sample_name.replace('_', '-')
                cwd = os.getcwd()
                abs_path = cwd + '/' + os.path.join(root, _x)
                direction = re.search(r'R\d', _x)
                if direction.group() == "R1":
                    temp = "forward"                    
                else:
                    temp = "reverse"
                csv_list.append([sample_name, abs_path, temp])
            else:
                print('no record created for: ', _x)
    csv_list.sort(key = lambda x: x[0])
    return csv_list


# start the .csv document
def create_csv_from_list(csv_list):
    """
    Create the csv file from the already created list of
    sample names, absolute paths, and strand direction
    """
    print("Creating the .csv file in the data folder", "\n")
    with open('00-data/manifest_pe.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        filewriter.writerow(['sample-id', 'absolute-filepath', 'direction'])
        for line in csv_list:
            filewriter.writerow(line)


# execute the functions
def main():
    """Run the other functions"""
    dir_name = setup()
    csv_list = create_list_from_files(dir_name)
    create_csv_from_list(csv_list)


if __name__ == "__main__":
    main()

sys.exit()
