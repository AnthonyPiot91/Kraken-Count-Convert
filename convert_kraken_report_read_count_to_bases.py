"""
Convert the number of reads attributed to each taxon in kraken2 report file
mpa-style to the number of sequenced bases.

Input files:
- kraken-inspect report file non-mpa style from used kraken2 databases
- kraken2 result file .report
- kraken2 result file .all

Usage:
	python normalize_kraken_results_per_bases.py
		path_to_kraken_result_folder
		kraken_results_prefix
		path_to_kraken-inspect_report_file
		path_to_output_files
"""

import os
import re
import sys
import json

# Define parameters
KRAKEN_PATH = sys.argv[1]
KRAKEN_PREFIX = sys.argv[2]
REPORT_PATH = f"{KRAKEN_PATH}/{KRAKEN_PREFIX}.report"
ALL_PATH = f"{KRAKEN_PATH}/{KRAKEN_PREFIX}.all"
KRAKEN_INSPECT_REPORT_FILE = sys.argv[3]
OUTPUT_DICT_PATH = sys.argv[4]
OUTPUT_DICT_FILE = f"{OUTPUT_DICT_PATH}/{KRAKEN_PREFIX}_bases.report"

# Create output path if it does not exist
if not os.path.exists(OUTPUT_DICT_PATH):
    os.makedirs(OUTPUT_DICT_PATH)

# Fill dictionary of base number per taxid
dict1 = {}
print("Computing number of sequenced bases per taxon...")
with open(ALL_PATH, "r") as KRAKEN_REPORT:
	for line in KRAKEN_REPORT:
		cols = line.split("\t")
		classfication = cols[0]
		read_id = cols[1]
		taxid = cols[2]
		read_length = int(cols[3])
		if taxid not in dict1:
			dict1[taxid] = read_length
		elif taxid in dict1:
			dict1[taxid] = dict1[taxid] + read_length
dict1 = dict(sorted(dict1.items()))
print("Number of sequenced bases per taxon calculated\n")

# Match taxon names between ".report" and ".all" files
"""
There are taxonomic subranks (e.g., K1, K2, P1, P2) in the
".all" files that do not exist in the ".report" file.
The following loop retrieves the parent taxonomic ranks (e.g., K, P)
of these taxonomic subranks and replace them in the dictionary
"""
print("Replacing taxonomic sub ranks with parent ranks...")
for key in list(dict1):
	cols = key.split(" (taxid ")
	taxon = cols[0]
	taxid = cols[1].replace(")", "")
	with open(KRAKEN_INSPECT_REPORT_FILE, "r") as KRAKEN_INSPECT:
		for line in KRAKEN_INSPECT:
			cols2 = line.split("\t")
			rank = cols2[3]
			taxid_db = cols2[4]
			if rank == "R":
				parent_R_taxid_db = cols2[4]
				parent_R_taxon_db = cols2[5]
			elif rank == "D":
				parent_D_taxid_db = cols2[4]
				parent_D_taxon_db = cols2[5]
			elif rank == "K":
				parent_K_taxid_db = cols2[4]
				parent_K_taxon_db = cols2[5]
			elif rank == "P":
				parent_P_taxid_db = cols2[4]
				parent_P_taxon_db = cols2[5]
			elif rank == "C":
				parent_C_taxid_db = cols2[4]
				parent_C_taxon_db = cols2[5]
			elif rank == "O":
				parent_O_taxid_db = cols2[4]
				parent_O_taxon_db = cols2[5]
			elif rank == "F":
				parent_F_taxid_db = cols2[4]
				parent_F_taxon_db = cols2[5]
			elif rank == "G":
				parent_G_taxid_db = cols2[4]
				parent_G_taxon_db = cols2[5]
			elif rank == "S":
				parent_S_taxid_db = cols2[4]
				parent_S_taxon_db = cols2[5]
			elif taxid == taxid_db:
				if "R" in rank:
					parent_rank = "R"
					parent_taxon_db = parent_R_taxon_db
					parent_taxid_db = parent_R_taxid_db
				elif "D" in rank:
					parent_rank = "D"
					parent_taxon_db = parent_D_taxon_db
					parent_taxid_db = parent_D_taxid_db
				elif "K" in rank:
					parent_rank = "K"
					parent_taxon_db = parent_K_taxon_db
					parent_taxid_db = parent_K_taxid_db
				elif "P" in rank:
					parent_rank = "P"
					parent_taxon_db = parent_P_taxon_db
					parent_taxid_db = parent_P_taxid_db
				elif "C" in rank:
					parent_rank = "C"
					parent_taxon_db = parent_C_taxon_db
					parent_taxid_db = parent_C_taxid_db
				elif "O" in rank:
					parent_rank = "O"
					parent_taxon_db = parent_O_taxon_db
					parent_taxid_db = parent_O_taxid_db
				elif "F" in rank:
					parent_rank = "F"
					parent_taxon_db = parent_F_taxon_db
					parent_taxid_db = parent_F_taxid_db
				elif "G" in rank:
					parent_rank = "G"
					parent_taxon_db = parent_G_taxon_db
					parent_taxid_db = parent_G_taxid_db
				elif "S" in rank:
					parent_rank = "S"
					parent_taxon_db = parent_S_taxon_db
					parent_taxid_db = parent_S_taxid_db
				parent_taxon_db = parent_taxon_db.replace("    ", "").replace("\n", "")
				parent_taxon_db = re.sub(r"\A *", "", parent_taxon_db)
				print(f"{rank} {taxon} (taxid {taxid})")
				parent_taxon_taxid_db = f"{parent_taxon_db} (taxid {parent_taxid_db})"
				print(f"{parent_rank}  {parent_taxon_taxid_db}")
				print("")
				if parent_taxon_taxid_db not in dict1:
					dict1[parent_taxon_taxid_db] = dict1[key]
				elif parent_taxon_taxid_db in dict1:
					dict1[parent_taxon_taxid_db] = dict1[key] + dict1[parent_taxon_taxid_db]
				del dict1[key]
				break
print("Taxon replacement finished.\n")
dict1 = dict(sorted(dict1.items()))

# Add taxonomic arborescence to dict
print("Adding taxonomic arborescence to taxon names...")
dict2 = {}
for key, value in dict1.items():
	taxon = key.split(" (taxid ")[0]
	taxon = re.escape(taxon)
	result = "Not found"
	with open(REPORT_PATH, "r") as REPORT:
		for line in REPORT:
			cols = line.split("\t")
			taxonomy = cols[0]
			match = re.search(fr"{taxon}\Z", taxonomy)
			if match is not None:
				result = "Found"
				if taxonomy not in dict2:
					dict2[taxonomy] = value
				elif taxonomy in dict2:
					dict2[taxonomy] = dict2[taxonomy] + value
				split_taxonomy = taxonomy.split("|")
				n_ranks = len(split_taxonomy)
				for i in range(1, n_ranks):
					sub_taxonomy = "|".join(split_taxonomy[0:n_ranks-i])
					if sub_taxonomy not in dict2:
						dict2[sub_taxonomy] = value
					elif sub_taxonomy in dict2:
						dict2[sub_taxonomy] = dict2[sub_taxonomy] + value
				break
	if result == "Not found":
		if taxon not in ["root", "unclassified"]:
			print(f"No match found for: {key}")
dict2 = dict(sorted(dict2.items()))

# Write dictionary to file
with open(OUTPUT_DICT_FILE, "w") as OUTPUT_DICT:
       for key, value in dict2.items():
               OUTPUT_DICT.writelines(f"{key}\t{value}\n")
print("\nFinal file wrote to:")
print(f"{OUTPUT_DICT_FILE}\n")
