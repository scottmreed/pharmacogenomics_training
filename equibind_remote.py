from server_connections import Pharmacogenomics
from dotenv import load_dotenv, find_dotenv
import os

# Caution: anything sent through run_command will excute on the server you are connected to as written.
# Look closely at these commands before executing them remotely.

load_dotenv(find_dotenv())

username = os.getenv('pharmaco_server_USER')
password = os.getenv('pharmaco_server_PASSWORD')

equibind_server = Pharmacogenomics(username=username, password=password)
alderaan_pharmaco_folder = os.path.join('/', 'home', 'reedsc', 'temp_file')
equibind_folder = os.path.join('/', 'home', 'reedsc', 'Equibind', 'EquiBind')

batch_file="""
#SBATCH --job-name=gpu
#SBATCH --partition=math-alderaan-gpu
#SBATCH --time=1-1:00:00
#SBATCH --ntasks=1
singularity exec ../equibind4_latest.sif python ./inference.py --config=configs_clean/inference.yml >& gpucode.log
"""
equibind_server.send_batch(alderaan_pharmaco_folder, batch_file)

def run_equibind():
    success = True
    try:
        equibind_command = f"sbatch {equibind_folder}/equibind_batch.sh {alderaan_pharmaco_folder}/pdb_temporary.txt"
        print(success)

        # with open('equibind_output.txt', 'w+') as f:
        #     f.write(equibind_output)
    except:
        success = False
        # set_PDB('ERROR')

    print('equibind run is done')
    return success


if __name__ == '__main__':
    # equibind_send_batch()
    run_equibind()
