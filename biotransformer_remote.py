import paramiko
import os
import logging
import mysql.connector
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

biotransformer_folder = os.path.join('/', 'home', 'boss', 'biotransformerjar3','biotransformer3.0jar')

error_logger = logging.getLogger('bt.error')
info_logger = logging.getLogger('bt.info')

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

host = os.getenv('pharmaco_server_IP')
username = os.getenv('pharmaco_server_USER')
password = os.getenv('pharmaco_server_PASSWORD')
client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
connection = client.connect(host, username=username, password=password, look_for_keys=False)

transport = paramiko.Transport((host, 22))
transport.connect(username=username, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)

def run_command(command, client):
    _stdin, _stdout, _stderr = client.exec_command(command)
    stdout = _stdout.read().decode()
    stderr = _stderr.read().decode()
    success = True
    if len(stderr) > 0:
        success = False
        error_logger.error(stderr)
    return stdout, success

def send_batch(path, command, sftp):
    f = sftp.open(f'{path}', "wb")
    f.write(f'{command}')
    sftp.chmod(f'{path}', 0o775)
    f.close()

def retreive_results(folder, sftp):
    f = sftp.get(f'{folder}/temp_bt', 'output')
    print(f)

for line in drugs_short:
    cid = line['drugID']
    drug = str(cid)
    Smile_to_biotransform = line['SmileCode']
    smile_string = str(Smile_to_biotransform)
    batch_file = f'cd {biotransformer_folder} && java -jar BioTransformer3.0_20220615.jar -k pred -b allHuman -ismi \"{smile_string}\" -ocsv {temp_bt} -s 2'

    send_batch('paramiko_batch.sh', batch_file, sftp)

    biotransformer_command = './paramiko_batch.sh'
    bt_output, success = run_command(biotransformer_command, client)
    print(bt_output)
    less_command = f'less {biotransformer_folder}/temp_bt'
    bt_output, success = run_command(less_command, client)
    print(bt_output)
