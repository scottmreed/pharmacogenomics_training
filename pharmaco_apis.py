#please don't tie up the production server with large requests. I'm working on adding a token system.
import requests

url = 'https://pharmacogenomics.clas.ucdenver.edu/api/plddt-score'
my_data = ({
    "CCID": "p.Thr198Met",
    "gene_ID": "ENSG00000160882"
})
res = requests.post(url, data = my_data)
print(res.content)


url = 'https://pharmacogenomics.clas.ucdenver.edu/api/best-resolution'
my_data = ({
    "gene_ID": "ENSG00000042832",
    "CCID": "p.Met1028Val"
})
res = requests.post(url, data = my_data)
print(res.content)


url = "https://pharmacogenomics.clas.ucdenver.edu/api/faspr-prep"
my_data = ({
    "CCID": "p.Thr198Met",
    "gene_ID": "ENSG00000160882",
    "angstroms": "7",
    "toggleAlphaFoldOn": "False",
    "file_location": "Null",
    "chain_id": "A"
})
res = requests.post(url, json=my_data)
print(res.content)


url = "https://pharmacogenomics.clas.ucdenver.edu/api/metab-prep"
my_data = ({
    "smiles": "CCC"
})
res = requests.post(url, json=my_data)
print(res.content)

# url = "https://pharmacogenomics.clas.ucdenver.edu/api/faspr-run"
# res = requests.post(url)
# print(res.content)
