import os
import logging
import mysql.connector
from dotenv import load_dotenv, find_dotenv
from server_connections import Pharmacogenomics

# Caution: anything sent through run_command will execute on the server you are connected to, as written.
# Look closely at these commands before executing them remotely.

load_dotenv(find_dotenv())

biotransformer_folder = os.path.join('/', 'home', 'boss', 'biotransformerjar3','biotransformer3.0jar')

error_logger = logging.getLogger('bt.error')
info_logger = logging.getLogger('bt.info')

my_ip = os.popen('curl ipinfo.io/ip').read()

if my_ip.startswith('174.29.'):
    mysql_host = '192.168.0.20'
    host = '192.168.0.20'

elif my_ip.startswith('132.194'):
    mysql_host = 'pharmacogenomics.ddnsfree.com'
    host = 'pharmacogenomics.ddnsfree.com'

else:
    mysql_host = os.getenv('mysql_host')
mysql_user = os.getenv('mysql_user')
mysql_pw = os.getenv('mysql_pw')

pharmacogenomics_db = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_pw,
    db="pharmacogenomics_dev")

print("Connection ID:", pharmacogenomics_db.connection_id)

cursor = pharmacogenomics_db.cursor(buffered=False, dictionary=True)

sql = f"""
SELECT distinct drugID, SmileCode
FROM `precursors`"""
cursor = pharmacogenomics_db.cursor(buffered=True, dictionary=True)
cursor.execute(sql)
drugs = cursor.fetchall()
cursor.close()

print('drugs length is:', len(drugs))
drugs_short = drugs[0:1]
print(len(drugs_short))

username = os.getenv('pharmaco_server_USER')
password = os.getenv('pharmaco_server_PASSWORD')

biotransformer_server = Pharmacogenomics(username=username, password=password)

for line in drugs_short:
    cid = line['drugID']
    drug = str(cid)
    Smile_to_biotransform = line['SmileCode']
    smile_string = str(Smile_to_biotransform)
    temp_bt = 'test_file'
    batch_file = f'cd {biotransformer_folder} && java -jar BioTransformer3.0_20220615.jar -k pred -b allHuman -ismi \"{smile_string}\" -ocsv {temp_bt} -s 2'

    biotransformer_server.send_batch('paramiko_batch.sh', batch_file)

    biotransformer_command = './paramiko_batch.sh'
    bt_output, success = biotransformer_server.run_command(biotransformer_command)
    print(bt_output)
    less_command = f'less {biotransformer_folder}/temp_bt'
    bt_output, success = biotransformer_server.run_command(less_command)
    print(bt_output)
