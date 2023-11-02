import os
import pandas as pd
import mysql.connector
import numpy as np
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from matplotlib import rcParams

load_dotenv()

username = os.getenv('pharmaco_server_USER')
password = os.getenv('pharmaco_server_PASSWORD')

host_IP = os.getenv('mysql_host')
db_user = os.getenv('mysql_user')
db_pw = os.getenv('mysql_pw')

pharmacogenomics_db = mysql.connector.connect(
    host=f'{host_IP}',
    user=f'{db_user}',
    password=f'{db_pw}'
)
print("Connection ID:", pharmacogenomics_db.connection_id)

sql_sel_database = "USE pharmacogenomics"
cursor = pharmacogenomics_db.cursor()
cursor.execute(sql_sel_database)

input_folder = os.path.join('..', '..',  'GTEXOME_analysis', 'ratio1toInf')

folders = os.listdir(f'{input_folder}')

plddt_list_combined = []
alphafold_suitable = 0
plddt_dict = {}
mutation_count_dict = {}
charge_change_dict = {}
disulfide_change_dict = {}
proline_change_dict = {}
hbond_change_dict = {}
salt_change_dict = {}
alphafold_suitable_dict = {}
rare_dict = {}

plddt_list_total = []
charge_change_total = 0
disulfide_change_total = 0
proline_change_total = 0
hbond_change_total = 0
salt_change_total = 0
alphafold_suitable_total = 0
rare_dict_total = 0
mutation_count_total = 0
gene_count = 0
repeat = 0
total_list = {}

for file in folders:
    if file.endswith('csv') == True:

        file_name = os.path.join(input_folder, file)
        protein_list = pd.read_csv(file_name)
        geneID = protein_list['Gene ID']
        gene_count += len(protein_list)
        plddt_list = []
        charge_change = 0
        mutation_count = 0
        disulfide_change = 0
        proline_change = 0
        hbond_change = 0
        salt_change = 0
        alphafold_suitable = 0
        rare = 0
        mutation_totals = {}
        file = file.replace('.csv', '')
        mutation_histogram = []

        duplicate_check = enumerate(geneID)
        for gene in duplicate_check:
            if gene[1] in total_list:
                print(gene[1], file, 'also in', total_list[f'{gene[1]}'])

            else:
                total_list[f'{gene[1]}'] = file

        for index, id in enumerate(geneID):
            sql = f"SELECT * FROM pharmacogenomics.gtexome_mutations WHERE geneID_CCID like '{geneID[index]}%';"
            cursor = pharmacogenomics_db.cursor(buffered=True)
            cursor.execute(sql)
            pharmacogenomics_db.commit()
            gtexome_mutations = cursor.fetchall()
            mutation_histogram.append(len(gtexome_mutations))
            try:
                for index, mutation in enumerate(gtexome_mutations):
                    plddt_list.append(float(gtexome_mutations[index][2]))
                    plddt_list_combined.append(float(gtexome_mutations[index][2]))
                    plddt_list_total.append(float(gtexome_mutations[index][2]))
                    mutation_count += 1
                    mutation_count_total += 1
                    if float(gtexome_mutations[index][1]) < 0.1:
                        rare += 1
                        rare_dict_total += 1
                    if (gtexome_mutations[index][3]) == 'No swap of positively and negatively charged residues.':
                        charge_change += 1
                        charge_change_total += 1
                    if (gtexome_mutations[index][4]) == 'No disulfides disrupted.':
                        disulfide_change += 1
                        disulfide_change_total += 1
                    if (gtexome_mutations[index][5]) == 'No cis proline removed':
                        proline_change += 1
                        proline_change_total += 1
                    if (gtexome_mutations[index][7]) == 'No buried side chain hydrogen bonds disrupted.':
                        hbond_change += 1
                        hbond_change_total += 1
                    if (gtexome_mutations[index][8]) == 'No buried salt bridges broken.':
                        salt_change += 1
                        salt_change_total += 1
                    if gtexome_mutations[index][9] == 'Alphafold structure suitable for modeling':
                        alphafold_suitable += 1
                        alphafold_suitable_total += 1

            except:
                print('exception')
        mutation_totals[f'{file}'] = mutation_histogram
        print('histogram input for ', file, ': ', mutation_totals[f'{file}'])
        if len(plddt_list) > 0:
            print(f'length of {file} is', mutation_count)
            print(f'mean for {file} is', np.mean(plddt_list))
            plddt_dict[f'{file}'] = np.mean(plddt_list)
            mutation_count_dict[f'{file}'] = mutation_count
            charge_change_dict[f'{file}'] = round(100-100*(charge_change/mutation_count))
            disulfide_change_dict[f'{file}'] = round(100-100*(disulfide_change/mutation_count))
            proline_change_dict[f'{file}'] = round(100-100*(proline_change/mutation_count))
            hbond_change_dict[f'{file}'] = round(100-100*(hbond_change/mutation_count))
            salt_change_dict[f'{file}'] = round(100-100*(salt_change/mutation_count))
            alphafold_suitable_dict[f'{file}'] = round(100*(alphafold_suitable/mutation_count))
            rare_dict[f'{file}'] = round(100-100*(rare/mutation_count))

            print(f'charge_change for {file} is', charge_change, round(100-100*(charge_change/mutation_count)), '%')
            print(f'disulfide_change for {file} is', disulfide_change, round(100-100*(disulfide_change/mutation_count)), '%')
            print(f'proline_change for {file} is', proline_change, round(100-100*(proline_change/mutation_count)), '%')
            print(f'hbond_change for {file} is', hbond_change, round(100-100*(hbond_change/mutation_count)), '%')
            print(f'salt_change for {file} is', salt_change, round(100-100*(salt_change/mutation_count)), '%')
            print(f'alphafold_suitable for {file} is', alphafold_suitable, round(100*(alphafold_suitable/mutation_count)), '%')
            print(f'rare for {file} is', rare, round(100-100*(rare/mutation_count)), '%')

    else:
        continue

print('plddt_list_combined is ', len(plddt_list_combined), 'long. With mean of ', np.mean(plddt_list_combined))
print('alphafold_suitable is ', alphafold_suitable, 'out of ', len(plddt_list_combined))
print('mutation_count_total', mutation_count_total)

print('plddt_list_total', len(plddt_list_total), len(plddt_list_total)/mutation_count_total)
print('charge_change_total', charge_change_total, charge_change_total/mutation_count_total)
print('disulfide_change_total', disulfide_change_total, disulfide_change_total/mutation_count_total)
print('proline_change_total', proline_change_total, proline_change_total/mutation_count_total)
print('hbond_change_total', hbond_change_total, hbond_change_total/mutation_count_total)
print('salt_change_total', salt_change_total, salt_change_total/mutation_count_total)
print('alphafold_suitable_total', alphafold_suitable_total, alphafold_suitable_total/mutation_count_total)
print('rare_dict_total', rare_dict_total, rare_dict_total/mutation_count_total)

print('gene_count is: ', gene_count)

rcParams['figure.figsize'] = (7, 7)

save_name=str('Paper_figs')
plt.xticks(fontsize=9, rotation=90)
plt.bar(plddt_dict.keys(), plddt_dict.values())
plt.tight_layout()
plt.savefig(f'plddt_dict_{save_name}.png')
plt.clf()

mutation_count_dict.pop('Testis')
plt.xticks(fontsize=9, rotation=90)
plt.bar(mutation_count_dict.keys(), mutation_count_dict.values())
plt.tight_layout()
plt.savefig(f'mutation_count_dict{save_name}.png')
plt.clf()

plt.xticks(fontsize=9, rotation=90)
plt.bar(charge_change_dict.keys(), charge_change_dict.values())
plt.tight_layout()
plt.savefig(f'charge_change_dict{save_name}.png')
plt.clf()
#
# plt.xticks(fontsize=9, rotation=90)
# plt.bar(disulfide_change_dict.keys(), disulfide_change_dict.values())
# plt.tight_layout()
# plt.savefig(f'disulfide_change_dict{save_name}.png')
# plt.clf()

plt.xticks(fontsize=9, rotation=90)
plt.bar(proline_change_dict.keys(), proline_change_dict.values())
plt.tight_layout()
plt.savefig(f'proline_change_dict{save_name}.png')
plt.clf()

plt.xticks(fontsize=9, rotation=90)
plt.bar(hbond_change_dict.keys(), hbond_change_dict.values())
plt.tight_layout()
plt.savefig(f'hbond_change_dict{save_name}.png')
plt.clf()

plt.xticks(fontsize=9, rotation=90)
plt.bar(salt_change_dict.keys(), salt_change_dict.values())
plt.tight_layout()
plt.savefig(f'salt_change_dict{save_name}.png')
plt.clf()

plt.xticks(fontsize=9, rotation=90)
plt.bar(alphafold_suitable_dict.keys(), alphafold_suitable_dict.values())
plt.tight_layout()
plt.savefig(f'alphafold_suitable_dict{save_name}.png')
plt.clf()

plt.xticks(fontsize=9, rotation=90)
plt.bar(rare_dict.keys(), rare_dict.values())
plt.tight_layout()
plt.savefig(f'rare_dict{save_name}.png')
plt.clf()
