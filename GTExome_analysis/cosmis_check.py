import pandas as pd
from dotenv import load_dotenv, find_dotenv
import mysql.connector
import json
import os
import numpy as np
import re
from Bio.SeqUtils import seq1


def three_to_one(three_letter_code):
    return seq1(three_letter_code.capitalize())


def get_Pnum(specificENSG):
    with open('ENSG_PN_dict.json', 'rb') as uniprot_to_ensg:
        utpdict = json.load(uniprot_to_ensg)
        pnum = utpdict[f"{specificENSG}"]
    return pnum


def get_ENST(specificPnum): # get enst number from p number
    with open('uniprot_to_enst.json', 'rb') as uniprot_to_enst:
        utpdict = json.load(uniprot_to_enst)
        enst = utpdict[f"{specificPnum}"]
        enst1 = enst[:100]
    return enst1


def get_COSMIS(cosmis_dict, specificENST):
    cosmis_pvalue = cosmis_dict[f'{specificENST[0]}']
    return cosmis_pvalue


df = pd.read_csv('cosmis_scores_alphafold.tsv', nrows=5000000, sep='\t')
cosmis_dict = dict(zip(df['enst_id'], [df['cosmis']]))
cosmis_af_df = df[['enst_id', 'cosmis', 'uniprot_aa', 'uniprot_pos']]


df = pd.read_csv('cosmis_scores_pdb.tsv', nrows=5000000, sep='\t')
cosmis_dict_pdb = dict(zip(df['enst_id'], df['cosmis']))
cosmis_pdb_df = df[['enst_id', 'cosmis', 'uniprot_aa', 'uniprot_pos']]

load_dotenv(find_dotenv())

mysql_user = os.getenv('mysql_user')
mysql_pw = os.getenv('mysql_pw')
mysql_host = os.getenv('mysql_host')

pharmacogenomics_db = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_pw,
    db="pharmacogenomics_dev")

print("Connection ID:", pharmacogenomics_db.connection_id)

cursor = pharmacogenomics_db.cursor(buffered=False, dictionary=True)

username = os.getenv('pharmaco_server_USER')
password = os.getenv('pharmaco_server_PASSWORD')
sql = f"SELECT * FROM pharmacogenomics_dev.gtexome_mutations;"
cursor = pharmacogenomics_db.cursor(buffered=True)
cursor.execute(sql)
pharmacogenomics_db.commit()
gtexome_mutations = cursor.fetchall()

cosmis_pdb_hits = {}
cosmis_af_hits = {}
no_match_af = 0
no_match_pdb = 0


for gtexome_index, mutation in enumerate(gtexome_mutations):

    ENSG = gtexome_mutations[gtexome_index][0].split('_')[0]
    pnum = get_Pnum(ENSG)
    enst_list = get_ENST(pnum)
    native_aa = three_to_one(gtexome_mutations[gtexome_index][0].split('_')[1][2:5])

    mutant_n = str(re.findall(r'\d+', gtexome_mutations[gtexome_index][0].split('_')[1]))
    mutation_str = mutant_n.strip("['']")
    mutation_position = int(mutation_str)

    for enst_index, enst_value in enumerate(enst_list):

        try:
            rows_pdb = cosmis_pdb_df.loc[cosmis_pdb_df['enst_id'] == f'{enst_list[enst_index]}']
            rows_pdb = rows_pdb.loc[rows_pdb['uniprot_aa'] == native_aa]
            rows_pdb = rows_pdb.loc[rows_pdb['uniprot_pos'] == mutation_position]

            if len(rows_pdb['cosmis']) > 1:
                print('len rows pdb long', len(rows_pdb['cosmis']))

            if len(rows_pdb['cosmis']) > 0:
                mean_cosmis = np.nanmean(rows_pdb['cosmis'])

            else:
                mean_cosmis = np.nan

            if not np.isnan(mean_cosmis):
                print(f'matched pdb for {ENSG} of {mean_cosmis}')
                cosmis_pdb_hits[f'{mutation}'] = np.nanmean(rows_pdb['cosmis'])

            elif mean_cosmis.size == 0:
                print('mean_cosmis.size == 0')

        except:
            print('no rows matched for cosmis_pdb_df')
            no_match_pdb += 1


        try:
            rows_af = cosmis_af_df.loc[cosmis_af_df['enst_id'] == f'{enst_list[enst_index]}']
            rows_af = rows_af.loc[rows_af['uniprot_aa'] == native_aa]
            rows_af = rows_af.loc[rows_af['uniprot_pos'] == mutation_position]


            if len(rows_af['cosmis']) > 1:
                print('len rows pdb long', len(rows_af['cosmis']))

            if len(rows_af['cosmis']) > 0:
                mean_cosmis = np.nanmean(rows_af['cosmis'])

            else:
                mean_cosmis = np.nan

            if not np.isnan(mean_cosmis):
                print(f'matched pdb for {ENSG} of {mean_cosmis}')
                cosmis_af_hits[f'{mutation}'] = np.nanmean(rows_af['cosmis'])

            elif mean_cosmis.size == 0:
                print('mean_cosmis.size == 0')

        except:
            print('no rows matched for cosmis_af_df')
            no_match_af += 1


print(no_match_pdb, 'no_match_PDB')
print(no_match_af, 'no_match_AF')

with open('cosmis_output_dict_pdb_revised.json', 'w') as js_file:
    json.dump(cosmis_pdb_hits, js_file, indent=4,
                  separators=(',', ': '))

with open('cosmis_output_dict_AF_revised.json', 'w') as js_file:
    json.dump(cosmis_af_hits, js_file, indent=4,
                  separators=(',', ': '))
