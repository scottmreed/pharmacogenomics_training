# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests

from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import Draw

mol = Chem.MolFromSmiles("C1CC2=C3C(=CC=C2)C(=CN3C1)[C@H]4[C@@H](C(=O)NC4=O)C5=CNC6=CC=CC=C65")

logp = Descriptors.MolLogP(mol, includeHs=True)
print(logp)

# inchi_mol2 = Chem.MolFromInchi('InChI=1S/C9H8O4/c1-6(10)13-8-5-3-2-4-7(8)9(11)12/h2-5H,1H3,(H,11,12)')
response = requests.get('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/vioxx/property/InChI/TXT')
inchi_input = response.text.strip('\n')
inchi_mol = Chem.MolFromInchi(inchi_input)#, sanitize=False, removeHs=False)

logp = Descriptors.MolLogP(inchi_mol, includeHs=True)
print(logp)
mol_list = []
mol_list.append(inchi_mol)
# mol_list.append(inchi_mol2)
Draw.MolsToGridImage(mol_list)
img = Draw.MolsToGridImage(mol_list)
img.save('output.png')
