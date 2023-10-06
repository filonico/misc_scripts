#!/bin/env python3

# Given a list file of SRA accession numbers, this script is intented to download the corresponding reads from NCBI.
# The final output would be a directory structured as follow:
#
# ./
# └── your_output_dir/
#     ├── 01_fastq/
#     |   └── {results of fastqc analysis}
#     ├── SRRXXXXXX1/
#     |   ├── SRRXXXXXX1_1_fastq.gz
#     |   └── SRRXXXXXX1_2_fastq.gz
#     ├── SRRXXXXXX2/
#     |   ├── SRRXXXXXX2_1_fastq.gz
#     |   └── SRRXXXXXX2_2_fastq.gz
#     ...
#     └── SRRXXXXXXN/
#         ├── SRRXXXXXXN_1_fastq.gz
#         └── SRRXXXXXXN_2_fastq.gz
#
#
# Written by:   Filippo Nicolini
# Last updated: 06/10/2023


import subprocess, argparse, sys

################################
#     Reading arguments in     #
################################

# Initialise the parser class
parser = argparse.ArgumentParser(description = 'Download reads from NCBI through the sra-tool and perform quality check')

# Define some options/arguments/parameters
parser.add_argument('-i', '--input', help = 'Path to input file. Note that it should be a list of SRA accession numbers')
parser.add_argument('-o', '--output_dir', help = 'Name of the output directory', default = "01_raw_reads")

# This line checks if the user gave no arguments, and if so then print the help
parser.parse_args(args = None if sys.argv[1:] else ['--help'])

# Collect the inputted arguments into a dictionary
args = parser.parse_args()


##########################################################################
#     Defining functions to download reads and perform quality check     #
##########################################################################


def download_reads_and_qc(accession):
    try:
        # Download SRA
        print(f"-- {accession} --")
        print("  Downloading the sra file")
        prefetch_process = subprocess.run(f"prefetch -O {output_dir}/ {accession}",
                                          shell = True,
                                          capture_output = True,
                                          text = True)

        # Download fastqs
        SRA_file = output_dir + "/" + accession + "/*sra*"
        fastq_output_dir = output_dir + "/" + accession

        print("  Downloading the fastq files")
        fastqdump_process = subprocess.run(f"fastq-dump --defline-seq '@$sn[_$rn]/$ri' --split-files {SRA_file} -O {fastq_output_dir}",
                                           shell = True,
                                           capture_output = True,
                                           text = True)
        

        # Quality check
        print("  Checking read quality")
        fastqc_process = subprocess.run(f"fastqc {fastq_output_dir}/*fastq -o {output_dir}/01_fastqc -f fastq",
                                        shell = True,
                                        capture_output = True,
                                        text = True)

        # Gzip fastq files
        print("  Gzipping fastq files")
        subprocess.run(f"gzip -9 {fastq_output_dir}/*fastq",
                       shell = True)
        
        # Remove sra files
        print("  Removing the sra file")
        subprocess.run(f"rm {SRA_file}",
                       shell = True)
        
        print(f"Done")
        print()


    except subprocess.CalledProcessError as err:
        print("An error occured:", err.stderr)


###############################
#     Reading SRA list in     #
###############################


SRA_list = []

# Create output direcotory
output_dir = args.output_dir
print()
print(f"Creating output directory in {output_dir}/")
subprocess.run(f"mkdir -p {output_dir}/01_fastqc", shell = True)

with open(args.input) as input_SRA:
    for line in input_SRA.readlines():
        SRA_list.append(line.strip())

print()
print(f"Reading in {len(SRA_list)} accession numbers")
print()


####################################################
#     Download reads and perform quality check     #
####################################################


for SRA in SRA_list:
    download_reads_and_qc(SRA)



