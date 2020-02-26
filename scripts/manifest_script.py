#!/usr/bin/env python3

"""
Creates a PROPER qiime2 manifest from a directory of FASTQ files generated in
Genome Quebec naming style OR from miSeq instruments
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
    """Using the directory name, create a list with the sample-id,
     forward-absolute-filepath, and reverse-absolute-filepath"""
    tsv_list = []
    for root, dirs, files in os.walk(dir_name, followlinks=True):
        for _x in dirs:
            dirs.remove(_x)
        for _x in files:
            # print(filename)
            if re.search(r"(?<=FLD\d{4}).\w*R1.fastq.gz$", _x) is not None:
                mode = 'GQ'
                sample_name = re.search(r'(?<=FLD\d{4}).\w*R1.fastq.gz$', _x).group()
                # sample_name = temp.group()
                r_abs_path = sample_name.replace('R1', 'R2')
                sample_name = sample_name.replace('.', '')
                sample_name = sample_name.replace('fastqgz', '')
                sample_name = sample_name.replace('_R1', '')
                # sample_name = sample_name.replace('_R2', '')
                f_abs_path = os.path.join(root, _x)
                r_abs_path = os.path.join(root, r_abs_path)
                tsv_list.append([sample_name, f_abs_path, r_abs_path])
            else:
                if re.search(r'.*?_S\d*_L001_R1', _x) is not None:
                    mode = "miseq"
                    sample_name = re.search(r'.*?_S', _x).group()
                    sample_name = sample_name.replace('_S','')
                    # print(sample_name)
                    f_abs_path = os.path.join(root, _x)
                    r_abs_path = os.path.join(root, _x)
                    r_abs_path = r_abs_path.replace('R1', 'R2')
                    tsv_list.append([sample_name, f_abs_path, r_abs_path])
    tsv_list.sort(key = lambda x: x[0])
    return tsv_list, mode


# SWITCH FOR PROPER MANIFEST LOCATION
def manifest_loc(mode): # RETURN AN ARRAY FROM LIST, HAS LIST AND STYLE OF FNAMES
    """determine the type of naming style needed"""
    if mode == 'GQ':
        location = '00-data/manifest_pe.tsv'
    else:
        location = '00-data/manifest_mseq.tsv'  
    return location


# start the .tsv document
def create_tsv_from_list(tsv_list, location):
    """
    Create the csv file from the already created list of
    sample names, absolute paths, and strand direction
    """
    print("Creating the .tsv file in the PWD", "\n")
    with open(location, 'w') as tsvfile:
        filewriter = csv.writer(tsvfile, delimiter='\t') 
        # quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['sample-id', 'forward-absolute-filepath', 'reverse-absolute-filepath'])
        for line in tsv_list:
            filewriter.writerow(line)


# execute the functions
def main():
    """Run the other functions"""
    dir_name = setup()
    result = create_list_from_files(dir_name)
    create_tsv_from_list(result[0], manifest_loc(result[1]))


if __name__ == "__main__":
    main()

sys.exit()