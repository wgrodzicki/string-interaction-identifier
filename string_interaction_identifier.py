# Takes a file with STRING-mapped proteins and retrieves all of their interactions
# above the given interaction threshold from a STRING interaction file.
# The output is a list of interactions converted to protein names based on the STRING mapping file.

import sys
from pathlib import Path

string_id_key = "string_id"
preffered_name_key = "preferred_name"

string_mapped_target_proteins_file_path = Path(sys.argv[1])
string_interactions_file_path = Path(sys.argv[2])

string_mapped_target_proteins = []

with open(string_mapped_target_proteins_file_path, "r") as file:
    mapped_proteins_lines = file.readlines()

    for line in mapped_proteins_lines[1:]:  # Skip header
        columns = line.strip().split("\t")
        string_mapped_target_proteins.append(
            {
                string_id_key: columns[2],
                preffered_name_key: columns[3],
            }
        )

interaction_threshold = -1

while interaction_threshold < 0 or interaction_threshold > 1:
    try:
        interaction_threshold = float(
            input("Enter interaction threshold (non-negative integer, between 0 and 1): ")
        )
    except:
        continue

target_protein_interactions = []
last_target_protein = ""
distinct_target_protein_count = 0

# Get all target proteins with thier interactions present in the STRING interaction file
with open(string_interactions_file_path, "r") as file:
    interaction_lines = file.readlines()

    for line in interaction_lines[1:]:  # Skip header
        columns = line.strip().split("\t")

        # Not the desired score, assuming score is in the last column
        if float(columns[-1]) < interaction_threshold:
            continue

        for string_mapped_target_protein in string_mapped_target_proteins:

            #  The interacting protein is not the target protein
            if columns[0] != string_mapped_target_protein[preffered_name_key]:
                continue

            target_protein_interactions.append(
                (
                    columns[0], # The target protein
                    columns[1], # The protein interacting with the target protein
                    float(columns[-1]), # Interaction score
                )
            )

            if last_target_protein != string_mapped_target_protein[preffered_name_key]:
                last_target_protein = string_mapped_target_protein[preffered_name_key]
                distinct_target_protein_count += 1


output_file_name = input("Enter the output file name: ")

with open(output_file_name, "w") as f:
    f.write(f"Distinct target proteins with interactions: {distinct_target_protein_count}\n")
    f.write("Target Protein\tInteracting Protein\tInteraction Score\n")

    for target_protein_interaction in target_protein_interactions:
        f.write(
            f"{target_protein_interaction[0]}\t{target_protein_interaction[1]}\t{target_protein_interaction[2]}\n"
        )
