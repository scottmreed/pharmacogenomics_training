from server_connections import Pharmacogenomics, Alderaan, Kenari
from dotenv import load_dotenv, find_dotenv
import os

# Caution: anything sent through run_command will excute on the server you are connected to as written.
# Look closely at these commands before executing them remotely.

load_dotenv(find_dotenv())


username = os.getenv('Kenari_USER')
password = os.getenv('Kenari_PASSWORD')

equibind_server = Kenari(username=username, password=password)
kenari_sif_folder = os.path.join('/', 'singularity')
inference_folder = os.path.join('/', 'opt', 'EquiBind', 'EquiBind')


# username = os.getenv('ALDERAAN_USER')
# password = os.getenv('ALDERAAN_PASSWORD')
# equibind_server = Alderaan(username=username, password=password)
# equibind_pharmaco_folder = os.path.join('/', 'home', 'reedsc', 'temp_file')
# sif_folder = os.path.join('/', 'home', 'reedsc', 'Equibind')
# equibind_folder = os.path.join('/', 'home', 'reedsc', 'Equibind', 'EquiBind')


def run_equibind():
    success = True
    try:
        # equibind_command = f"sbatch {equibind_folder}/equibind_batch.sh {kenari_equibind_folder}/pdb_temporary.txt"
        # command_input = f'singularity exec {kenari_equibind_folder}/equibind4_latest.sif ls /home'
        # equibind_server.run_command(command_input)
        # command_input = f'ls {sif_folder}'
        # output, _ = equibind_server.run_command(command_input)
        # print(output)
        # command_input = f'singularity exec {sif_folder}/equibind4_latest.sif ls {kenari_equibind_folder}/configs_clean/'
        # output, _ = equibind_server.run_command(command_input)
        # print(output)
        # command_input = f'singularity exec {sif_folder}/equibind4_latest.sif python {kenari_equibind_folder}/inference.py --config={equibind_folder}/configs_clean/inference.yml'
        # output, _ = equibind_server.run_command(command_input)
        # print(output)
        command_input = f'ls {inference_folder}'
        output, _ = equibind_server.run_command(command_input)
        print(output)
        command_input = f'singularity exec {kenari_sif_folder}/equibind4_latest.sif ls /opt/conda'# {inference_folder}/configs_clean'
        output, _ = equibind_server.run_command(command_input)
        print(output)
        command_input = f'singularity exec {kenari_sif_folder}/equibind4_latest.sif python /opt/EquiBind/EquiBind/inference.py --config={inference_folder}/configs_clean/inference.yml'
        output, _ = equibind_server.run_command(command_input)
        print(output)
        # with open('equibind_output.txt', 'w+') as f:
        #     f.write(equibind_output)
    except:
        success = False
        # set_PDB('ERROR')

    print('equibind run is done')
    return success


run_equibind()
