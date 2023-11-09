import pandas as pd
from dotenv import load_dotenv, find_dotenv
import mysql.connector
import json
import os


def get_Pnum(specificENSG):
    with open('./ENSG_PN_dict.json', 'rb') as uniprot_to_ensg:
        utpdict = json.load(uniprot_to_ensg)
        pnum = utpdict[f"{specificENSG}"]
    return pnum


def get_ENST(specificPnum): # get enst number from p number
    with open('./uniprot_to_enst.json', 'rb') as uniprot_to_enst:
        utpdict = json.load(uniprot_to_enst)
        enst = utpdict[f"{specificPnum}"]
        enst1 = enst[:100]
    return enst1


def get_COSMIS(cosmis_dict, specificENST):
    cosmis_pvalue = cosmis_dict[f'{specificENST[0]}']
    return cosmis_pvalue

df = pd.read_csv('cosmis_scores_alphafold.tsv', sep='\t')
cosmis_dict = dict(zip(df['enst_id'], df['cosmis']))


df = pd.read_csv('cosmis_scores_pdb.tsv', sep='\t')
cosmis_dict_pdb = dict(zip(df['enst_id'], df['cosmis']))


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

cosmis_list_pdb = {}
cosmis_list_AF = {}
no_match_AF = 0
no_match_PDB = 0

for index, mutation in enumerate(gtexome_mutations):

    ENSG = gtexome_mutations[index][0].split('_')[0]
    pnum = get_Pnum(ENSG)
    enst = get_ENST(pnum)
    try:
        cosmis = cosmis_dict[f'{enst[0]}']
        cosmis_list_AF[f'{mutation}'] = cosmis

    except:
        print('no match')
        no_match_AF += 1
    try:
        cosmis_pdb = cosmis_dict_pdb[f'{enst[0]}']
        cosmis_list_pdb[f'{mutation}'] = cosmis_pdb
    except:
        print('no match')
        no_match_PDB += 1

print(no_match_PDB, 'no_match_PDB')
print(no_match_AF, 'no_match_AF')

with open('cosmis_output_dict_pdb.json', 'w') as js_file:
    json.dump(cosmis_list_pdb, js_file, indent=4,
                  separators=(',', ': '))

with open('cosmis_output_dict_AF.json', 'w') as js_file:
    json.dump(cosmis_list_AF, js_file, indent=4,
                  separators=(',', ': '))
