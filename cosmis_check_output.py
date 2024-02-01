import json
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


with open('cosmis_output_dict_pdb_revised.json', 'r') as js_file:
    data_pdb = json.load(js_file)

print(len(data_pdb), 'is len pdb dict')
cosmis = list(data_pdb.values())
print('np.median(cosmis) for PDB: ', np.median(cosmis))
tot_cosmis = np.sum(cosmis)
mean_cosmis = tot_cosmis/len(cosmis)
print('mean_cosmis for PDB: ', mean_cosmis)

with open('cosmis_output_dict_AF_revised.json', 'r') as js_file:
    data_af = json.load(js_file)

print(len(data_af), 'is len AF dict')
cosmis = list(data_af.values())
print('np.median(cosmis) for AF: ', np.median(cosmis))
tot_cosmis = np.sum(cosmis)
mean_cosmis = tot_cosmis/len(cosmis)
print('mean_cosmis for AF: ', mean_cosmis)

count = 0
for key in data_af.keys():
    if key in data_pdb.keys():
        count += 1
print(count)

values = 0
for value in data_af.values():
    if value in data_pdb.values():
        values += 1
print(count)

data_combined = data_af.copy()
data_combined.update(data_pdb)
print(len(data_combined), 'is len AF dict')
cosmis = list(data_combined.values())
print('np.median(cosmis) for AF: ', np.median(cosmis))
tot_cosmis = np.sum(cosmis)
mean_cosmis = tot_cosmis/len(cosmis)
print('mean_cosmis for AF: ', mean_cosmis)
plt.hist(data_combined.values())
plt.savefig('histogram')