import json
import pickle
import pandas as pd

with open("ENSG_PN_dictALL.pickle", 'rb') as input_file:
    new_dict = pickle.load(input_file)

json_obj = json.dumps(new_dict, indent=4)

with open('ENSG_PN_dict.json', 'w') as js_file:
    json.dump(new_dict, js_file, indent=4,
              separators=(',', ': '))