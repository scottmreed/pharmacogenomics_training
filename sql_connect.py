import mysql.connector
import os
from dotenv import load_dotenv

host_IP = os.getenv('host_IR')
user = os.getenv('host_IR')
pw = os.getenv('host_IR')
pharmacogenomics_db = mysql.connector.connect(
    host=host_IP,
    user=user,
    password=pw
)
print("Connection ID:", pharmacogenomics_db.connection_id)

sql_sel_database = "USE pharmacogenomics_dev"
cursor = pharmacogenomics_db.cursor()
cursor.execute(sql_sel_database)

unmapped_precursor_InChiKeys = []
sql = f"""
   SELECT count(*) FROM pharmacogenomics_dev.precursors;"""
cursor = pharmacogenomics_db.cursor(buffered=True)
cursor.execute(sql)
pharmacogenomics_db.commit()
unmapped_precursor_InChiKeys = cursor.fetchall()
print((unmapped_precursor_InChiKeys))