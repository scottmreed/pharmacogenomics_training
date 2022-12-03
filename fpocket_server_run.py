import os
from dotenv import load_dotenv, find_dotenv
from server_connections import Serverconnection

load_dotenv(find_dotenv())

host = os.getenv('pharmaco_server_IP')
username = os.getenv('pharmaco_server_USER')
password = os.getenv('pharmaco_server_PASSWORD')

class Pharmacogenomics(Serverconnection):
    """This is a subclass of Serverconnection
    which must be imported from server_connections
    Multiple subclassses can be prepared for different connections
    Each inherits the class functions like run_command
    but allow for a unique set of credentials to be passed.
    After this subclassing it will need to be instantiated below."""
    def __init__(self, host, username, password):
        super().__init__(host, username, password)


if __name__ == '__main__':
    # These are directories on the remote server
    fpocket_dir = os.path.join('/', 'home', 'boss', 'Fpocket', 'fpocket', 'bin')
    alpha_folder = os.path.join('/', 'home', 'boss', 'website_activity', 'tmp')
    # Instantiating the server
    fpocket_server = Pharmacogenomics(host=host, username=username, password=password)
    protein_folders, success = fpocket_server.run_command(f'ls {alpha_folder}')
    protein_list = protein_folders.split("\n")
    for protein in protein_list:
        fpocket_command = f'{fpocket_dir}/fpocket -f {alpha_folder}/{protein}/{protein}.pdb'
        fpocket_output, success = fpocket_server.run_command(fpocket_command)
        fpocket_readout = f'cat {alpha_folder}/{protein}/{protein}_out/pockets/pocket1_atm.pdb'
        fpocket_pocket, success = fpocket_server.run_command(fpocket_readout)
        print(fpocket_pocket)
        # clean_command = f'rm {alpha_folder}/{protein}/{protein}_out/{protein}_out.pdb'
        # _, _ = fpocket_server.run_command(clean_command)
        # clean_command = f'rm {alpha_folder}/{protein}/{protein}_out/{protein}.pml'
        # _, _ = fpocket_server.run_command(clean_command)
        # clean_command = f'rm {alpha_folder}/{protein}/{protein}_out/{protein}_pockets.pqr'
        # _, _ = fpocket_server.run_command(clean_command)
        # clean_command = f'rm {alpha_folder}/{protein}/{protein}_out/{protein}_PYMOL.sh'
        # _, _ = fpocket_server.run_command(clean_command)
        # clean_command = f'rm {alpha_folder}/{protein}/{protein}_out/{protein}.tcl'
        # _, _ = fpocket_server.run_command(clean_command)
        # clean_command = f'rm {alpha_folder}/{protein}/{protein}_out/{protein}_VMD.sh'
        # _, _ = fpocket_server.run_command(clean_command)


