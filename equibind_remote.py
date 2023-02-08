from server_connections import Pharmacogenomics, Alderaan, Kenari
from dotenv import load_dotenv, find_dotenv
import os

# Caution: anything sent through run_command will excute on the server you are connected to as written.
# Look closely at these commands before executing them remotely.

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

    alpha_folder = os.path.join('/', 'home', 'boss', 'website_activity', 'tmp')
    equibind_server = Pharmacogenomics(username=username, password=password)
    protein_folders, success = equibind_server.run_command(f'ls {alpha_folder}')
    protein_list = protein_folders.split("\n")
    for protein in protein_list[0]:

        batch_file = """
        ls -l 
        pwd >& test.log
        """
        equibind_server.send_batch('equibind_batch.sh', batch_file)
        equibind_server.send_chmod('equibind_batch.sh')
        output, _ = equibind_server.run_command('./equibind_batch.sh')
        command_input = 'cat test.log'
        output, _ = equibind_server.run_command(command_input)
        print(output)
