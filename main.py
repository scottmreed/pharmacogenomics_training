import requests
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import Draw

"""
A script to explore using pubchem API
"""

# adding a new molecule
mol = Chem.MolFromSmiles("C1CC2=C3C(=CC=C2)C(=CN3C1)[C@H]4[C@@H](C(=O)NC4=O)C5=CNC6=CC=CC=C65")

logp = Descriptors.MolLogP(mol, includeHs=True)
print(logp)

response = requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/vioxx/property/InChI/TXT')
inchi_input = response.text.strip('\n')
inchi_mol = Chem.MolFromInchi(inchi_input)#, sanitize=False, removeHs=False)

logp = Descriptors.MolLogP(inchi_mol, includeHs=True)
print(logp)
mol_list = []
mol_list.append(inchi_mol)
Draw.MolsToGridImage(mol_list)
img = Draw.MolsToGridImage(mol_list)
img.save('output.png')

# use f string to try a new drug
drug_name = 'acetone'
response = requests.get(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{drug_name}/property/InChI/TXT')
inchi_input = response.text.strip('\n')
inchi_mol = Chem.MolFromInchi(inchi_input)#, sanitize=False, removeHs=False)
