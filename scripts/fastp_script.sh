#!/bin/bash

# from https://robertslab.github.io/sams-notebook/-
# -2019/12/18/TrimmingFastQCMultiQC-C.bairdi-RNAseq-FastQ-with-fastp-on-Mox.html
# Bash script attempt for running fastp on fastq.gz files

###### ORIGINAL DESCRIPTION ######
## C.bairdi RNAseq trimming using fastp.
# This script is called by 20191218_cbai_RNAseq_rsync.sh. That script transfers the FastQ files
# to the working directory from: https://owl.fish.washington.edu/nightingales/C_bairdi/

# Exit script if any command fails
set -e

# Paths to programs
### Is specifying the path really necessary? 
### If so it needs to be collected as a var or input
### will attempt without it for now
### -> YES IT IS REQUIRED. May need to set this once imported to another sys
fastp=/home/mathew/anaconda3/envs/fastp/bin/fastp

# may need to be changed depending on the application
threads=4

cd ~00-raw-data

## Inititalize arrays
fastq_array_R1=()
fastq_array_R2=()
R1_names_array=()
R2_names_array=()

# Create array of fastq R1 files
for fastq in *R1*.gz
do
  fastq_array_R1+=("${fastq}")
done

# Create array of fastq R2 files
for fastq in *R2*.gz
do
  fastq_array_R2+=("${fastq}")
done

# Create array of sample names
## Uses awk to parse out sample name from filename
for R1_fastq in *R1*.gz
do
  R1_names_array+=($(echo "${R1_fastq}" | awk -F"." '{print $1}'))
done

# Create array of sample names
## Uses awk to parse out sample name from filename
for R2_fastq in *R2*.gz
do
  R2_names_array+=($(echo "${R2_fastq}" | awk -F"." '{print $1}'))
done

# Create list of fastq files used in analysis
for fastq in *.gz
do
  echo "${fastq}" >> fastq.list.txt
done

# Run fastp on files
for index in "${!fastq_array_R1[@]}"
do
	timestamp=$(date +%Y%m%d)
	echo "${R1_names_array[index]}"
	echo "${R2_names_array[index]}"
  	R1_sample_name=$(echo "${R1_names_array[index]}")
	R2_sample_name=$(echo "${R2_names_array[index]}")
	${fastp} \
	--in1 "${fastq_array_R1[index]}" \
	--in2 "${fastq_array_R2[index]}" \
	--detect_adapter_for_pe \
	--thread ${threads} \
	--html ../~00-quality-control/fastp-files/"${R1_sample_name}".report.fastp.html \
	--json ../~00-quality-control/fastp-files/"${R1_sample_name}".report.fastp.json \
	--out1 ../00-data/"${R1_sample_name}".fastp.fastq.gz \
	--out2 ../00-data/"${R2_sample_name}".fastp.fastq.gz
done

# --json "${R1_sample_name}".fastp.report.json \