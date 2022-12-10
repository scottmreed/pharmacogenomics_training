import os
from dotenv import load_dotenv, find_dotenv
from server_connections import Pharmacogenomics
from biopandas.mol2 import PandasMol2
from biopandas.pdb import PandasPdb

# Caution: anything sent through run_command will excute on the server you are connected to as written.
# Look closely at these commands before executing them remotely.

"""
runs qvina expecting the following arrangement in docking_dir
>input_proteins (folder)
    >first_protein(folder)
        >native_first_protein.pdb
            >org###mut_blah_protein.pdb (for snv)
>input_ligands (folder)
    >ligand(folder)
        >org_ligand.mol2
        >metblah_ligand.mol2 (for metabolite)
Adds:                  
>docking_output (folder)
    >protein1 (folder)
        >ligand1
"""

# you may want/need to change the docking_dir to your account where you have permissions
docking_dir = os.path.join('/', 'home', 'boss', 'pharmaco_withdrawndrugs_project')
qvina_path = os.path.join('/', 'home', 'boss', 'qvina')

load_dotenv(find_dotenv())
username = os.getenv('pharmaco_server_USER')
password = os.getenv('pharmaco_server_PASSWORD')

docking_server = Pharmacogenomics(username=username, password=password)

protein_folders, _ = docking_server.run_command(f'ls {docking_dir}/input_proteins')
protein_folders = protein_folders.split('\n')

start_size, _ = docking_server.run_command(f'du -sh {docking_dir}')
print(f'Space occupied is {start_size}')

pmol = PandasMol2()
ppdb = PandasPdb()

def ligand_centroid(mol2_path):
    ligandmol2 = pmol.read_mol2(mol2_path)
    ATOM = pmol.df
    x = ATOM['x'].mean()
    y = ATOM['y'].mean()
    z = ATOM['z'].mean()

    return x, y, z

def snv_coordinate_box(pdb_path, snv_number):
    proteinpdb = ppdb.read_pdb(pdb_path)
    ATOM = ppdb.df['ATOM']=ppdb.df['ATOM'][ppdb.df['ATOM']['residue_number'] == float(snv_number)]
    x = ATOM['x_coord'].mean()
    y = ATOM['y_coord'].mean()
    z = ATOM['z_coord'].mean()

    return x, y, z

for protein in protein_folders:
    protein_files, _ = docking_server.run_command(f'ls {docking_dir}/input_proteins/{protein}/*.pdbqt')
    _, success = docking_server.run_command(f'mkdir {docking_dir}/docking_output/{protein}')
    protein_files = protein_files.rstrip()
    protein_files = protein_files.split('\n')

    for protein_file in protein_files:
        protein_name = protein_file.split('/')[-1]
        if protein_name.startswith('native'):
            snv_x, snv_y, snv_z = snv_coordinate_box(protein_file_path, protein_file[14:-9])
            output_mkdir = f'mkdir {docking_dir}/docking_output/{protein_name[:-6]}'
            _, success = docking_server.run_command(output_mkdir)
            ligands_list, _ = docking_server.run_command(f'ls {docking_dir}/input_ligands')
            ligands_list = ligands_list.rstrip()
            ligands_list = ligands_list.split('\n')

            for ligand in ligands_list:
                output_ligand_dir = docking_dir + f'/docking_output/{protein_name[:-6]}/ligand'
                ligand_output = f'mkdir {docking_dir}/docking_output/{protein_name[:-6]}/ligand'
                _, _ = docking_server.run_command(ligand_output)
                ligand_list = f'ls {docking_dir}/input_ligands/*.pdbqt'
                ligand_files, _ = docking_server.run_command(ligand_list)
                ligand_files = ligand_files.rstrip()
                ligand_files = ligand_files.split('\n')

                for ligand_file in ligand_files:
                    ligand_file_path = docking_dir + '/input_ligands/' + ligand
                    ligandoutput_file = ligand_file[:-6] + '_output.pdbqt'
                    qvina_command = f'{qvina_path}/qvina-w --config {docking_dir}/temp_conf/conf.txt --ligand {ligand_file_path} --out {output_ligand_dir}/{ligandoutput_file}'
                    _, success = docking_server.run_command(qvina_command)

end_size, _ = docking_server.run_command(f'du -sh {docking_dir}')

print('folder size started at:\n', start_size, '\nand ended at:\n', end_size)