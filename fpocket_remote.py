import os
from dotenv import load_dotenv, find_dotenv
from server_connections import Pharmacogenomics
import re
import json

# Caution: anything sent through run_command will execute on the server you are connected to, as written.
# Look closely at these commands before executing them remotely.
load_dotenv(find_dotenv())

username = os.getenv('pharmaco_server_USER')
password = os.getenv('pharmaco_server_PASSWORD')

if __name__ == '__main__':
    # fpocket_dir = os.path.join('/', 'home', 'boss', 'Fpocket', 'fpocket', 'bin')
    alpha_folder = os.path.join('/', 'home', 'boss', 'website_activity', 'tmp')
    fpocket_dir = "/home/boss/Fpocket/fpocket/bin"
    # alpha_folder = "/home/jillhoffman2/website_activity/fpocket/tmp"
    fpocket_server = Pharmacogenomics(username=username, password=password)
    protein_folders, success = fpocket_server.run_command(f'ls {alpha_folder}')
    protein_list = protein_folders.split("\n")
    trimmed_list = [x for x in protein_list if x.startswith('AF')]
    for protein in trimmed_list:
        fpocket_command = f'{fpocket_dir}/fpocket -f {alpha_folder}/{protein}/{protein}.pdb'
        fpocket_output, success = fpocket_server.run_command(fpocket_command)
        fpocket_readout = f'cat {alpha_folder}/{protein}/{protein}_out/pockets/pocket1_atm.pdb'
        out_path = f"{alpha_folder}/{protein}/{protein}_out"#
        pockets_path = f"{alpha_folder}/{protein}/{protein}_out/pockets"
        fpocket_pocket, success = fpocket_server.run_command(fpocket_readout)
        info_file = f"{alpha_folder}/{protein}/{protein}_out/{protein}_info.txt"
        json_command = f"python /home/jillhoffman2/Fpocket.py '{pockets_path}' '{info_file}' '{protein}' '{out_path}'"
        fpocket_server.run_command(json_command)

        clean_command = f'rm {alpha_folder}/{protein}/{protein}_out/{protein}_out.pdb'
        _, _ = fpocket_server.run_command(clean_command)
        clean_command = f'rm {alpha_folder}/{protein}/{protein}_out/{protein}.pml'
        _, _ = fpocket_server.run_command(clean_command)
        clean_command = f'rm {alpha_folder}/{protein}/{protein}_out/{protein}_pockets.pqr'
        _, _ = fpocket_server.run_command(clean_command)
        clean_command = f'rm {alpha_folder}/{protein}/{protein}_out/{protein}_PYMOL.sh'
        _, _ = fpocket_server.run_command(clean_command)
        clean_command = f'rm {alpha_folder}/{protein}/{protein}_out/{protein}.tcl'
        _, _ = fpocket_server.run_command(clean_command)
        clean_command = f'rm {alpha_folder}/{protein}/{protein}_out/{protein}_VMD.sh'
        _, _ = fpocket_server.run_command(clean_command)


