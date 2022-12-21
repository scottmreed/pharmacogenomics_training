from server_connections import Pharmacogenomics, Alderaan, Kenari
from dotenv import load_dotenv, find_dotenv
import os

# Caution: anything sent through run_command will excute on the server you are connected to as written.
# Look closely at these commands before executing them remotely.

load_dotenv(find_dotenv())

username = os.getenv('Kenari_USER')
password = os.getenv('Kenari_PASSWORD')

equibind_server = Kenari(username=username, password=password)

batch_file = """singularity exec ../../singularity/equibind7_latest.sif conda run -n equibind python \
/EquiBind/multiligand_inference.py --config=/EquiBind/configs_clean/inference.yml \
-o 'output' -r name1_protein.pdb -l ligands.sdf >& gpucode.log
"""

equibind_server.send_batch('equibind_batch.sh', batch_file)
equibind_server.send_chmod('equibind_batch.sh')
output, _ = equibind_server.run_command('./equibind_batch.sh')
command_input = 'cat gpucode.log'
output, _ = equibind_server.run_command(command_input)
print(output)

# username = os.getenv('ALDERAAN_USER')
# password = os.getenv('ALDERAAN_PASSWORD')
# equibind_server = Alderaan(username=username, password=password)
# equibind_pharmaco_folder = os.path.join('/', 'home', 'reedsc', 'temp_file')
# sif_folder = os.path.join('/', 'home', 'reedsc', 'Equibind')
# equibind_folder = os.path.join('/', 'home', 'reedsc', 'Equibind', 'EquiBind')
# kenari_sif_folder = os.path.join('/', 'singularity')
# inference_folder = os.path.join('/', 'opt', 'EquiBind', 'EquiBind')
#

# command_input = f'singularity exec {kenari_sif_folder}/equibind4_latest.sif python /opt/EquiBind/EquiBind/inference.py --config={inference_folder}/configs_clean/inference.yml'
# output, _ = equibind_server.run_command(command_input)
# print(output)
