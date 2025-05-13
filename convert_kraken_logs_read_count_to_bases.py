"""
Convert the number of reads outputed in kraken2 logs to a number of sequenced
bases

Input files:
- kraken2 log file .log
- kraken2 result file .all

Usage:
	python normalize_kraken_results_per_bases.py
		path_to_kraken_result_folder
		kraken_results_prefix
		path_to_output_files
"""

import os
import sys

# Define parameters
KRAKEN_PATH = sys.argv[1]
KRAKEN_PREFIX = sys.argv[2]
LOG_PATH = f"{KRAKEN_PATH}/{KRAKEN_PREFIX}.log"
ALL_PATH = f"{KRAKEN_PATH}/{KRAKEN_PREFIX}.all"
OUTPUT_DICT_PATH = sys.argv[3]
OUTPUT_DICT_FILE = f"{OUTPUT_DICT_PATH}/{KRAKEN_PREFIX}_bases.log"

# Create output path if it does not exist
if not os.path.exists(OUTPUT_DICT_PATH):
    os.makedirs(OUTPUT_DICT_PATH)

# Calculate the number of classified and unclassified bases
classified_bases = 0
unclassified_bases = 0

print("\nComputing number of classified and unclassified bases...")
with open(ALL_PATH, "r") as KRAKEN_ALL:
	for line in KRAKEN_ALL:
		cols = line.split("\t")
		classification = cols[0]
		read_length = int(cols[3])
		if classification == "C":
			classified_bases += read_length
		elif classification == "U":
			unclassified_bases += read_length

total_bases = classified_bases + unclassified_bases
print("Number of sequenced bases calculated\n")
print(f"Classified bases:\t{classified_bases}")
print(f"Unclassified bases:\t{unclassified_bases}")
print(f"Total bases:\t{total_bases}")

# Write dictionary to file
with open(OUTPUT_DICT_FILE, "w") as OUTPUT_DICT:
	OUTPUT_DICT.writelines(f"Classified bases:\t{classified_bases}\n")
	OUTPUT_DICT.writelines(f"Unclassified bases:\t{unclassified_bases}\n")
	OUTPUT_DICT.writelines(f"Total bases:\t{total_bases}\n")

print("\nDictionary of sequenced bases per taxon written to:")
print(f"{OUTPUT_DICT_FILE}\n")
