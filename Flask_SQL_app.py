import pandas as pd
from sqlalchemy import create_engine
import json
from flask import Flask, jsonify
from flask_cors import CORS
from io import StringIO

# A simple flask based API creation example from Informatics class

input_data = StringIO("""
,compound,name,BP_C,BP_K,SMILES,MW
0,1,Methane,-162.2,110.95,C,16.043
1,2,Ethane,-88.6,184.55,CC,30.07
2,3,propane,-42.2,230.95,CCC,44.1
3,4,butane,-0.1,273.05,CCCC,58.12
4,5,2-methylpropane,-11.2,261.95,CC(C)C,58.12
5,6,pentane,36.1,309.25,CCCCC,72.15
6,7,2-methylbutane,27.0,300.15,CC(C)CC,72.15
7,8,"2,2-dimethylpropane",9.5,282.65,CC(C)(C)C,72.15
8,9,hexane,68.8,341.95,CCCCCC,86.18
9,10,2-methylpentane,60.9,334.05,CC(C)CCC,86.18
10,11,3-methylpentane,63.3,336.45,CC(CC)CC,86.18
11,12,"2,2-dimethylbutane",49.8,322.95,CC(C)(CC)C,86.18
12,13,"2,3-dimethylbutane",58.1,331.25,CC(C)C(C)C,86.18
13,14,heptane,98.5,371.65,CCCCCCC,100.2
14,15,3-ethylpentane,93.5,366.65,C(C)C(CC)CC,100.2
15,16,"2,2-dimethylpentane",79.2,352.35,CC(C)(CCC)C,100.2
16,17,"2,3-dimethylpentane",89.8,362.95,CC(C)C(CC)C,100.2
17,18,"2,4-dimethylpentane",80.6,353.75,CC(C)CC(C)C,100.2
18,19,2-methylhexane,90.1,363.25,CC(C)CCCC,100.205
19,20,3-methylhexane,91.8,364.95,CC(CC)CCC,100.2
20,21,octane,125.6,398.75,CCCCCCCC,114.23
21,22,3-methylheptane,118.9,392.05,CC(CC)CCCC,114.232
22,23,"2,2,3,3-tetramethylbutane",106.5,379.65,CC(C)(C(C)(C)C)C,114.23
23,24,"2,3,3-trimethylpentane",114.7,387.85,CC(C)C(CC)(C)C,114.23
24,25,"2,3,4-trimethylpentane",113.7,386.85,CC(C)C(C(C)C)C,114.23
25,26,"2,2,4-trimethylpentane",99.3,372.45,CC(C)(CC(C)C)C,114.23
26,27,nonane,150.7,423.85,CCCCCCCCC,128.25
27,28,2-methyloctane,143.0,416.15,CC(C)CCCCCC,128.259
28,29,decane,174.2,447.35,CCCCCCCCCC,142.28
29,30,2-methylnonane,166.9,440.05,CC(C)CCCCCCC,142.28
""")
df_bp = pd.read_csv(input_data, sep=",")

# more info:
# https://flask.palletsprojects.com/en/2.2.x/quickstart/
# https://docs.df_bp.org/en/14/intro.html

engine = create_engine('sqlite://', echo=False)
df_bp.to_sql('chemical', con=engine)

print(engine.execute("SELECT * FROM chemical WHERE chemical.name is 'Methane'").fetchall())
print(engine.execute("SELECT * FROM chemical WHERE chemical.BP_C is -0.1").fetchall())

def get_chemicals(bp_value, df_bp):
    # chemicals = {}
    engine = create_engine('sqlite://', echo=False)
    df_bp.to_sql('chemical', con=engine)
    col_names = ['index', 'compound_number', 'name', 'BP_C', 'BP_K', 'SMILES', 'MW']
    try:
        with engine.connect() as conn:
            conn = conn.execution_options(stream_results=True, max_row_buffer=100)
            result = conn.execute(f"SELECT * from chemical WHERE chemical.BP_C is {bp_value}")
            chemicals = {}
            for row in result:
                for x, y in enumerate(row):
                    try:
                        chemicals[col_names[x]] = y
                    except:
                        'a'
    except:
        print('nothing to return')
        chemicals = {}
    chemicals_out = json.dumps(dict(chemicals), separators=(',', ':'))

    return chemicals_out

bp_value = '-0.1'
print(get_chemicals(bp_value, df_bp))

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/chemical/<name>', methods=['GET','POST'])

def api_get_users(name):
    return jsonify(get_chemicals(name, df_bp))


app.run()

# run the following from a python terminal, another script, or postman
# import requests
# print(requests.post('http://127.0.0.1:5000/api/chemical/-0.1').text)
