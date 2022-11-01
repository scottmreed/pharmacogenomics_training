import os
from dotenv import load_dotenv, find_dotenv
from server_connections import Serverconnection

load_dotenv(find_dotenv())

host = os.getenv('pharmaco_server_IP')
username = os.getenv('pharmaco_server_USER')
password = os.getenv('pharmaco_server_PASSWORD')

class Pharmacogenomics(Serverconnection):
    def __init__(self, host, username, password):
        super().__init__(host, username, password)


if __name__ == '__main__':
    fpocket_dir = os.path.join('/', 'home', 'boss', 'Fpocket', 'fpocket', 'bin')
    alpha_folder = os.path.join('/', 'home', 'boss', 'website_activity', 'tmp')
    fpocket_server = Pharmacogenomics(host=host, username=username, password=password)
    protein_folders, success = fpocket_server.run_command(f'ls {alpha_folder}')
    protein_list = protein_folders.split("\n")
    for protein in protein_list:
        fpocket_command = f'{fpocket_dir}/fpocket -f {alpha_folder}/{protein}'

        # fpocket_output, success = fpocket_server.run_command(fpocket_command)
        print(fpocket_output)

