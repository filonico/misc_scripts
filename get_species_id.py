#!/bin/env python3

# Given a list file of species, this script generate a tsv file with species ID.
#
# Species ID are build according to the following rule:
#   * first letter of the genus name + first three letters from the species epithet
#   * e.g.: Drosophila melanogaster -> Dmel; Tridacna squamosa -> Tsqu
#
# If desired, the script also checks for duplicates and try to generate unique identifiers
#
#
# Written by:   Filippo Nicolini
# Last updated: 16/10/2023

import subprocess, argparse, sys, os, csv

##########################################
#     Define arguments of the script     #
##########################################

# Initialise the parser class
parser = argparse.ArgumentParser(description = "Generate IDs for a list of species.")

# Define some options/arguments/parameters
parser.add_argument("-i", "--input_file",
                    required = True,
                    help = "A list of species names to be converted into species ID.")

parser.add_argument("-dup", "--allow_duplicates",
                    action = "store_true",
                    help = "Allow duplicated IDs. Default: \"False\"",
                    default = False)

parser.add_argument("-s", "--spacer",
                    help = "Specify the character used as a spacer in the input file. Default: \" \"",
                    default = " ")

parser.add_argument("-o", "--output_dir",
                    help = "Name of the output directory. Default: working directory",
                    default = "./")

# This line checks if the user gave no arguments, and if so then print the help
parser.parse_args(args = None if sys.argv[1:] else ["--help"])

# Collect the inputted arguments into a dictionary
args = parser.parse_args()


############################
#     Define functions     #
############################

# Function to generate species ID
def generate_species_id(species, redo):

    speciesID_alternatives = []

    # If the speciesID is not to be re-done, then just create it...
    if not redo:            
        # If the second word starts with a parenthesis (supposed genus sinonym), use the third word to generate species ID
        if species[1].startswith("("):
            speciesID = species[0][0] + species[2][0:3]
        else:
            speciesID = species[0][0] + species[1][0:3]

        return speciesID

    # ...else create a set different ones
    else:
        if species[1].startswith("("):
            for i in range(3, len(species[2])):
                speciesID_alternatives.append(species[0][0] + species[2][0:2] + species[2][i])
        else:
            for i in range(3, len(species[1])):
                speciesID_alternatives.append(species[0][0] + species[1][0:2] + species[1][i])

        # Return the list of alternative species ID without duplicates
        return list(dict.fromkeys(speciesID_alternatives))


# # Function to check for duplicates
# def check_duplicates(speciesID,speciesID_list):
#     is_duplicated = speciesID in speciesID_list

#     return is_duplicated


###########################
#     Read input file     #
###########################

# Create output direcotory
if not os.path.isdir(args.output_dir):
    print()
    print(f"Creating output directory in {args.output_dir}/")
    subprocess.run(f"mkdir {args.output_dir}", shell = True)

# Read in genome assembly accession list and store into a list object
print()
print(f"Reading {args.input_file}...")

species_list = []
with open(args.input_file) as input_acc:
    for line in input_acc.readlines():
        species_list.append(line.strip().split(args.spacer))

print(f"    {len(species_list)} species found")


################################
#     Generate species IDs     #
################################

# Generate species IDs
print()
print("Generating species IDs...")

problematic_species = []
duplicated_species = []
speciesID_list = []
for species in species_list:
    REDO = False

    # If the species is composed by only one word, do not generate speciesID and store the species in a dedicated list
    if len(species) == 1:
        problematic_species.append(species[0])
        continue

    # If duplicates are allowed then just generate species IDs...
    if args.allow_duplicates:
        speciesID_list.append([species, generate_species_id(" ".join(species), REDO)])

    # ...else generate non-duplicated IDs
    else:
        speciesID_toCheck = generate_species_id(species, REDO)

        if not any(speciesID_toCheck in subl for subl in speciesID_list):
            speciesID_list.append([" ".join(species), speciesID_toCheck])
        else:
            REDO = True
            duplicated_species.append(" ".join(species))
            speciesID_toCheck = generate_species_id(species, REDO)
            
            alternative_found = False
            for IDs in speciesID_toCheck:
                if not any(IDs in subl for subl in speciesID_list):
                    speciesID_list.append([" ".join(species), IDs])
                    alternative_found = True
                    break
            
            if not alternative_found:
                duplicated_species.append(" ".join(species))


############################################
#     Print results and write to files     #
############################################

print(f"    {len(speciesID_list)} IDs were successfully generated")
with open("species_ids_OUT.tsv","w+") as output_tsv:
    csvWriter = csv.writer(output_tsv, delimiter='\t')
    csvWriter.writerows(speciesID_list)
print("      Results written to species_ids_OUT.tsv")
print()

if problematic_species:
    print(f"    {len(problematic_species)} occurrences were composed by only one word, thus ID has not been generated for them")
    with open("problematic_species_OUT.ls","w+") as output_ls:
        output_ls.write('\n'.join(problematic_species))
    print("      Results written to problematic_species_OUT.ls")
    print()

if duplicated_species:
    print(f"    {len(duplicated_species)} occurrences were duplicated, you may want to check them")
    with open("duplicated_species_OUT.ls","w+") as output_ls:
        output_ls.write('\n'.join(duplicated_species))
    print("      Results written to duplicated_species_OUT.ls")
    print()