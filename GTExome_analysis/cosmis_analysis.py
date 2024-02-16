from dotenv import load_dotenv, find_dotenv
import mysql.connector
import os
import csv
from Bio.SeqUtils import seq1
import json
from collections import defaultdict
import pandas as pd
import numpy as np

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def convert_three_to_one(three_letter_codes):
    """
    Convert three-letter amino acid codes to one-letter representations.
    :param three_letter_codes: List of three-letter amino acid codes.
    :return: List of corresponding one-letter representations.
    """
    one_letter_codes = [seq1(code) for code in three_letter_codes]
    return one_letter_codes


json_file_path_1 = os.path.join('GTExome_analysis', 'cosmis_output_dict_AF_revised.json')  # Replace with the path to your first JSON file
data_1 = read_json_file(json_file_path_1)
json_file_path_2 = os.path.join('GTExome_analysis', 'cosmis_output_dict_pdb_revised.json')  # Replace with the path to your second JSON file
data_2 = read_json_file(json_file_path_2)

# Merge data from both JSON files
data = {**data_1, **data_2}

# Dictionary to store COSMIS scores for each ENSG number
cosmis_scores = defaultdict(list)

# Dictionary to store native amino acid residues for each ENSG number
native_aa_residues = {}

# Iterate over each entry in the data
for key, cosmis_score in data.items():
    ensg_number = key.split('_')[0][2:]  # Extract the ENSG number
    native_aa = key.split('_')[1][2:5]  # Extract the native amino acid residue
    cosmis_scores[ensg_number].append(cosmis_score)  # Store the COSMIS score
    native_aa_residues[ensg_number] = native_aa  # Store the native amino acid residue

# Calculate average COSMIS value for each amino acid
average_cosmis_values = defaultdict(list)
for ensg_number, scores in cosmis_scores.items():
    avg_score = sum(scores) / len(scores)
    if native_aa_residues[ensg_number] is not None:
        average_cosmis_values[native_aa_residues[ensg_number]].append(avg_score)

# Print average COSMIS value for each amino acid
for aa, scores in average_cosmis_values.items():
    avg_score = sum(scores) / len(scores)
    one_letter_aa = convert_three_to_one([aa])[0]  # Convert three-letter code to one-letter representation
    print(f"Average COSMIS value for {one_letter_aa}: {avg_score}")

one_letter_aa = {three_letter: seq1(three_letter) for three_letter in average_cosmis_values.keys()}
average_gtexome_cosmis = {one_letter_aa[aa]: sum(scores) / len(scores) for aa, scores in average_cosmis_values.items()}
df_average_gtexome_cosmis = pd.DataFrame(average_gtexome_cosmis.items(), columns=['Amino Acid', 'Average GTExome COSMIS'])

load_dotenv(find_dotenv())

# sql user
mysql_user = os.getenv('mysql_user')
mysql_pw = os.getenv('mysql_pw')
mysql_host = os.getenv('mysql_host')

# connecting to mysql
pharmacogenomics_db = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_pw,
    db="pharmacogenomics_dev")

# checking connection id
print("Connection ID:", pharmacogenomics_db.connection_id)

cursor = pharmacogenomics_db.cursor(buffered=False, dictionary=True)

username = os.getenv('pharmaco_server_USER')
password = os.getenv('pharmaco_server_PASSWORD')
sql = f"SELECT * FROM pharmacogenomics_dev.gtexome_mutations;"
cursor = pharmacogenomics_db.cursor(buffered=True)
cursor.execute(sql)
pharmacogenomics_db.commit()
gtexome_mutations = cursor.fetchall()


def three_to_one(three_letter_code):
    return seq1(three_letter_code.capitalize())


cosmis_averages_af = {}
cosmis_averages_pdb = {}

hydrophobic_aa = ('A', 'V', 'L', 'I', 'M', 'F', 'W', 'P')
hydrophilic_aa = ('R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'K', 'S', 'T', 'Y')

with open(os.path.join('GTExome_analysis', 'cosmis_scores_alphafold.tsv'), 'r') as tsv_file:
    reader = csv.reader(tsv_file, delimiter='\t')
    next(reader)
    for row in reader:
        try:
            uniprot_aa = row[3]
            cosmis_score = float(row[4])

            if uniprot_aa not in cosmis_averages_af:
                cosmis_averages_af[uniprot_aa] = []
                cosmis_averages_af[uniprot_aa].append(cosmis_score)
            else:
                cosmis_averages_af[uniprot_aa].append(cosmis_score)
        except ValueError as e:
            print(f"value error")
            continue
        except IndexError as e:
            print(f"index error")
            continue

with open(os.path.join('GTExome_analysis', 'cosmis_scores_pdb.tsv'), 'r') as tsv_file:
    reader = csv.reader(tsv_file, delimiter='\t')
    next(reader)
    for row in reader:
        try:
            uniprot_aa = row[3]
            cosmis_score = float(row[4])

            if uniprot_aa not in cosmis_averages_pdb:
                cosmis_averages_pdb[uniprot_aa] = []
                cosmis_averages_pdb[uniprot_aa].append(cosmis_score)
            else:
                cosmis_averages_pdb[uniprot_aa].append(cosmis_score)
        except ValueError as e:
            print(f"value error")
            continue
        except IndexError as e:
            print(f"index error")
            continue

cosmis_averages = {key: cosmis_averages_af.get(key, []) + cosmis_averages_pdb.get(key, []) for key in set(cosmis_averages_af) | set(cosmis_averages_pdb)}
average_scores = {key: np.median(values) if values else 0 for key, values in cosmis_averages.items()}
one_letter_aa_average_scores = {three_letter: seq1(three_letter) for three_letter in average_scores.keys()}
df_average_scores = pd.DataFrame(average_scores.items(), columns=['Amino Acid', 'Average COSMIS'])


print("Hydrophobic Amino Acids")
for aa in hydrophobic_aa:
    if aa in average_scores:
        print(f"{aa}, {average_scores[aa]}")

print("Hydrophilic Amino Acids")
for aa in hydrophilic_aa:
    if aa in average_scores:
        print(f"{aa}, {average_scores[aa]}")

average_gtexome_scores = {convert_three_to_one([key])[0]: value for key, value in average_cosmis_values.items()}

merged_df = pd.merge(df_average_scores, df_average_gtexome_cosmis, on="Amino Acid", suffixes=('_Overall', '_GTExome'))
merged_df['Difference'] = merged_df['Average GTExome COSMIS'] - merged_df['Average COSMIS']
print("Comparison of Average COSMIS Scores:")
print(merged_df)

mean_cosmis_aa_values = {aa: sum(scores) / len(scores) for aa, scores in average_cosmis_values.items()}
mean_cosmis_values_by_ensg = []

# Iterate over each entry in gtexome_mutations
for mutation in gtexome_mutations:
    # Extract the native amino acid residue from the mutation data
    native_aa = mutation[0].split('_')[1][2:5]

    # Calculate the mean COSMIS value for the native amino acid residue
    mean_cosmis_value = mean_cosmis_aa_values.get(native_aa, 0)  # Default to 0 if native_aa not found

    # Append the mean COSMIS value to the list
    mean_cosmis_values_by_ensg.append(mean_cosmis_value)

# Calculate the mean of mean COSMIS values
mean_mean_cosmis = sum(mean_cosmis_values_by_ensg) / len(mean_cosmis_values_by_ensg)
median_mean_cosmis = np.median(mean_cosmis_values_by_ensg)

# Print the list containing mean COSMIS values for each ENSG number
print("Mean COSMIS Values by ENSG Number:")
print(mean_cosmis_values_by_ensg)

# Print the mean of mean COSMIS values
print("Mean of Mean COSMIS Values:", mean_mean_cosmis)

num_mutations = len(gtexome_mutations)

# Print the number of mutations
print("Number of mutations in gtexome_mutations:", num_mutations)