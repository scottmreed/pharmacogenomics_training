import csv
cosmis_averages_af = {}
cosmis_averages_pdb = {}

hydrophobic_aa = ('A', 'V', 'L', 'I', 'M', 'F', 'W', 'P')
hydrophilic_aa = ('R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'K', 'S', 'T', 'Y')

with open("cosmis_scores_alphafold.tsv", 'r') as tsv_file:
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

with open("cosmis_scores_pdb.tsv", 'r') as tsv_file:
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

average_scores = {key: sum(values) / len(values) if values else 0 for key, values in cosmis_averages.items()}

print("Hydrophobic Amino Acids")
for aa in hydrophobic_aa:
    if aa in average_scores:
        print(f"{aa}, {average_scores[aa]}")

print("Hydrophilic Amino Acids")
for aa in hydrophilic_aa:
    if aa in average_scores:
        print(f"{aa}, {average_scores[aa]}")