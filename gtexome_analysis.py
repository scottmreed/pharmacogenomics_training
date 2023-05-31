import os
import pandas as pd
import mysql.connector
import numpy as np
from dotenv import load_dotenv

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

for file in folders:
    file_name = os.path.join(input_folder, file)
    protein_list = pd.read_csv(file_name)
    protein_list.describe()
    geneID_CCID = protein_list['Gene ID']
    plddt_list = []
    charge_change = 0
    charge_change_count = 0
    for index, id in enumerate(geneID_CCID):
        sql = f"SELECT * FROM pharmacogenomics.gtexome_mutations WHERE geneID_CCID like '{geneID_CCID[index]}%';"
        cursor = pharmacogenomics_db.cursor(buffered=True)
        cursor.execute(sql)
        pharmacogenomics_db.commit()
        gtexome_mutations = cursor.fetchall()

        try:
            for index, mutation in enumerate(gtexome_mutations):
                plddt_list.append(float(gtexome_mutations[index][2]))
                if (gtexome_mutations[index][3]) == 'No swap of positively and negatively charged residues.':
                    charge_change += 1
                charge_change_count

        except:
            'a'
    if len(plddt_list) > 0:
        print(f'mean for {file} is', np.mean(plddt_list))
    frac_no_swap = 'No entry'
    try:
        frac_no_swap = (charge_change / charge_change_count)
    except:
        'a'
    print('charge_change fraction as no swap', frac_no_swap)
